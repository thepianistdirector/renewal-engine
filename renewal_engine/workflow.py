"""Trusted-reference workflow. No API accepts a user repository command."""

from __future__ import annotations

from importlib.resources import files
import json
from pathlib import Path

from . import __version__
from .artifacts import atomic_json, new_run
from .comparison import compare_case, differences
from .discovery import discover
from .execution import run_process, runtime_identity, validate_capture, validate_runtime_record
from .report import render
from .transformation import digest, patch, transform


def resource_bytes(name):
    return files("renewal_engine").joinpath(name).read_bytes()


def trusted_assets():
    assets = {name: resource_bytes("reference/" + name)
              for name in ("program.py", "harness.py", "cases.json", "trust.json", "policy.json")}
    trust = json.loads(assets["trust.json"])
    for name, expected in [("program.py", trust["program_hashes"]["original"]),
                           ("harness.py", trust["harness_sha256"]), ("cases.json", trust["cases_sha256"])]:
        if digest(assets[name]) != expected:
            raise ValueError("trusted reference hash mismatch: " + name)
    return assets, trust


def demo(destination: Path, baseline: Path, target: Path, negative_control=False):
    destination = destination.absolute()
    assets, trust = trusted_assets()
    cases = json.loads(assets["cases.json"])
    policy = json.loads(assets["policy.json"])
    new_run(destination)
    try:
        reference = destination / "reference"
        reference.mkdir()
        for name, content in assets.items():
            (reference / name).write_bytes(content)
            (reference / name).chmod(0o444)
        identities = {"original": runtime_identity(baseline, policy["baseline"], destination),
                      "candidate": runtime_identity(target, policy["target"], destination)}
        discovery = discover(assets["program.py"])
        expected_key = "negative_control" if negative_control else "candidate"
        rows = [{"path": "program.py", "source_sha256": trust["program_hashes"]["original"],
                 "candidate_sha256": trust["program_hashes"][expected_key], "changed": True, **discovery.json()}]
        original_dir = destination / "original"
        original_dir.mkdir()
        (original_dir / "program.py").write_bytes(assets["program.py"])
        (original_dir / "program.py").chmod(0o444)
        original_dir.chmod(0o555)
        candidate = destination / "candidate/program.py"
        if negative_control:
            rows[0]["negative_control"] = "Independent fault: replace the explicit diagnostic source with WRONG.ini"
        manifest = {"schema": 1, "tool_version": __version__, "mode": "trusted-reference",
                    "negative_control": negative_control, "recipe": "configparser-local-prefix-v1",
                    "recipe_sha256": digest(resource_bytes("discovery.py") + resource_bytes("transformation.py")),
                    "comparator_sha256": digest(resource_bytes("comparison.py")),
                    "policy_sha256": digest(assets["policy.json"]), "fixture_sha256": trust,
                    "runtimes": identities, "files": rows,
                    "execution": {"isolation": "scrubbed subprocess with resource limits; not an OS sandbox",
                                  "timeout_seconds": 10, "output_limit_bytes": 131072,
                                  "environment_keys": ["LANG", "LC_ALL", "TZ", "TMPDIR"]}}
        atomic_json(destination / "manifest.json", manifest)
        (destination / "manifest.json").chmod(0o444)
        atomic_json(destination / "state.json", {"stage": "CHARACTERIZING ORIGINAL", "complete": False})
        observed = {"original": {}, "candidate": {}}
        for side, interpreter in [("original", baseline), ("candidate", target)]:
            if side == "candidate":
                # Baseline observations and frozen identities exist before any
                # candidate bytes are created. The transformer cannot change
                # those observations or the independent expected source hash.
                atomic_json(destination / "state.json", {"stage": "BASELINE RECORDED", "complete": False})
                transformed = transform(assets["program.py"], discovery)
                if digest(transformed) != trust["program_hashes"]["candidate"]:
                    raise ValueError("transformation disagrees with independently frozen expected candidate")
                if negative_control:
                    transformed = transformed.replace(b"source=source", b'source="WRONG.ini"')
                if digest(transformed) != trust["program_hashes"][expected_key]:
                    raise ValueError("candidate identity mismatch")
                candidate.parent.mkdir()
                candidate.write_bytes(transformed)
                (destination / "changes.patch").write_text(patch(assets["program.py"], transformed, "program.py"), encoding="utf-8")
                atomic_json(destination / "state.json", {"stage": "CANDIDATE READY", "complete": False})
            for case in cases:
                cwd = destination / "observations" / side / case["id"]
                cwd.mkdir(parents=True)
                source = destination / side / "program.py"
                process = run_process([str(interpreter.resolve()), "-I", "-S", "-B", "-X", "utf8",
                                       str(reference / "harness.py"), str(source)], cwd,
                                      json.dumps(case, ensure_ascii=False).encode("utf-8"))
                atomic_json(cwd / "process.json", process)
                if process["failure"] or process["returncode"] != 0 or process["stderr"]:
                    raise ValueError("trusted case execution failed; retained " + side + "/" + case["id"] + "/process.json")
                observation = json.loads(process["stdout"])
                # Collect declared filesystem effects independently of fixture
                # instrumentation, before saving observation evidence itself.
                file_effects = {}
                for path in sorted(cwd.iterdir()):
                    if path.name == "process.json":
                        continue
                    if not path.is_file() or path.is_symlink():
                        raise ValueError("trusted fixture produced an undeclared file type")
                    data = path.read_bytes()
                    file_effects[path.name] = {"sha256": digest(data), "size": len(data)}
                observation["effects"]["files"] = file_effects
                atomic_json(cwd / "observation.json", observation)
                observed[side][case["id"]] = observation
                atomic_json(destination / "state.json", {"stage": "OBSERVING", "complete": False,
                                                         "last_case": case["id"], "side": side})
        atomic_json(destination / "state.json", {"stage": "COMPARING", "complete": False})
        comparisons = [compare_case(case, observed["original"][case["id"]], observed["candidate"][case["id"]], policy)
                       for case in cases]
        regressions = sum(c["status"] == "REGRESSION" for c in comparisons)
        result = {"status": "REGRESSION" if regressions else "PASS", "behavior_measured": True,
                  "files": rows, "cases": comparisons, "regressions": regressions,
                  "expected_changes": sum(len(c["expected_changes"]) for c in comparisons),
                  "negative_control": negative_control,
                  "limitations": ["Only the original, reviewed reference fixture was executed.",
                                  "Evidence applies only to the declared cases and exact Linux CPython runtime identities.",
                                  "Traceback stacks, exception chaining, import hooks, concurrent code and arbitrary external effects are unmeasured.",
                                  "Process limits and a scrubbed environment are not an OS sandbox.",
                                  "Passing cases do not establish general equivalence, human validation or maintainer adoption."]}
        atomic_json(destination / "results.json", result)
        (destination / "report.html").write_text(render(result, manifest), encoding="utf-8")
        atomic_json(destination / "state.json", {"stage": "COMPARED", "complete": True,
                                                "result": result["status"], "behavior_measured": True})
        return result
    except BaseException:
        atomic_json(destination / "state.json", {"stage": "INCOMPLETE", "complete": False,
                                                "recovery": "Keep all evidence and restart into a new directory."})
        raise


def verify_saved(directory: Path):
    """Reopen retained evidence; never execute a source file or interpreter."""
    manifest = json.loads((directory / "manifest.json").read_text())
    state = json.loads((directory / "state.json").read_text())
    if not state.get("complete"):
        raise ValueError("run is incomplete; retain it and restart")
    result = json.loads((directory / "results.json").read_text())
    if result.get("files") != manifest.get("files"):
        raise ValueError("result file identities differ from the manifest")
    expected_patch = ""
    for row in manifest["files"]:
        for side, key in [("original", "source_sha256"), ("candidate", "candidate_sha256")]:
            path = Path(row["path"])
            if path.is_absolute() or ".." in path.parts:
                raise ValueError("invalid manifest member path")
            if digest((directory / side / path).read_bytes()) != row[key]:
                raise ValueError(side + " source changed since the run")
        expected_patch += patch((directory / "original" / path).read_bytes(),
                                (directory / "candidate" / path).read_bytes(), row["path"])
    if (directory / "changes.patch").read_bytes() != expected_patch.encode("utf-8"):
        raise ValueError("saved patch differs from retained source snapshots")
    if manifest["mode"] == "inspection":
        if (result.get("status") != "INSPECTION ONLY" or result.get("behavior_measured") is not False
                or state.get("stage") != "INSPECTED" or state.get("behavior_measured") is not False
                or manifest.get("runtimes") is not None):
            raise ValueError("inspection evidence cannot claim measured behavior or a passing comparison")
    elif manifest["mode"] == "trusted-reference":
        negative = manifest.get("negative_control")
        if type(negative) is not bool or type(result.get("negative_control")) is not bool or result["negative_control"] != negative:
            raise ValueError("negative-control labels are inconsistent")
        expected_key = "negative_control" if negative else "candidate"
        if (len(manifest["files"]) != 1 or manifest["files"][0]["path"] != "program.py"
                or manifest["files"][0]["candidate_sha256"] != manifest["fixture_sha256"]["program_hashes"][expected_key]):
            raise ValueError("candidate identity contradicts the negative-control label")
        if digest(resource_bytes("comparison.py")) != manifest["comparator_sha256"]:
            raise ValueError("reopen this run with the matching comparator version")
        if state.get("stage") != "COMPARED" or state.get("behavior_measured") is not True:
            raise ValueError("comparison state is incomplete or inconsistent")
        for name, expected in [("harness.py", manifest["fixture_sha256"]["harness_sha256"]),
                               ("program.py", manifest["fixture_sha256"]["program_hashes"]["original"])]:
            if digest((directory / "reference" / name).read_bytes()) != expected:
                raise ValueError("saved reference source changed: " + name)
        policy_data = (directory / "reference/policy.json").read_bytes()
        if digest(policy_data) != manifest["policy_sha256"]:
            raise ValueError("saved policy changed")
        cases_data = (directory / "reference/cases.json").read_bytes()
        if digest(cases_data) != manifest["fixture_sha256"]["cases_sha256"]:
            raise ValueError("saved case inputs changed")
        policy, cases = json.loads(policy_data), json.loads(cases_data)
        retained_trust = json.loads((directory / "reference/trust.json").read_text())
        if retained_trust != manifest["fixture_sha256"]:
            raise ValueError("retained fixture trust record differs from the manifest")
        for side, version_key in [("original", "baseline"), ("candidate", "target")]:
            validate_runtime_record(manifest["runtimes"][side], policy[version_key])
        recomputed = []
        for case in cases:
            if not isinstance(case.get("id"), str) or Path(case["id"]).name != case["id"] or case["id"] in {".", ".."}:
                raise ValueError("invalid saved case identity")
            records = []
            for side in ("original", "candidate"):
                cwd = directory / "observations" / side / case["id"]
                process = json.loads((cwd / "process.json").read_text())
                validate_capture(process)
                instrumented = json.loads(process["stdout"])
                record = json.loads((cwd / "observation.json").read_text())
                file_effects = {}
                for path in sorted(cwd.iterdir()):
                    if path.name in {"process.json", "observation.json"}:
                        continue
                    if not path.is_file() or path.is_symlink():
                        raise ValueError("saved effect has an unexpected file type")
                    data = path.read_bytes()
                    file_effects[path.name] = {"sha256": digest(data), "size": len(data)}
                instrumented["effects"]["files"] = file_effects
                if instrumented != record:
                    raise ValueError("saved observation differs from process output or filesystem effects")
                if (cwd / "input.ini").read_bytes() != case["content"].encode("utf-8"):
                    raise ValueError("saved input differs from the frozen characterization case")
                records.append(record)
            recomputed.append(compare_case(case, *records, policy))
        if differences(recomputed, result["cases"]):
            raise ValueError("saved comparison no longer matches retained observations")
        count = sum(c["status"] == "REGRESSION" for c in recomputed)
        expected_status = "REGRESSION" if count else "PASS"
        if (result.get("status") != expected_status or state.get("result") != expected_status
                or result.get("behavior_measured") is not True or result.get("regressions") != count
                or result.get("expected_changes") != sum(len(c["expected_changes"]) for c in recomputed)):
            raise ValueError("saved comparison summary differs from recomputed evidence")
    else:
        raise ValueError("unknown saved evidence mode")
    return {"status": "VERIFIED SAVED EVIDENCE", "result": result["status"],
            "behavior_measured": result["behavior_measured"]}
