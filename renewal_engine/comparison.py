"""Independent comparison of retained observations and a frozen policy."""

from copy import deepcopy


def differences(old, new, path="$", result=None):
    result = [] if result is None else result
    if type(old) is not type(new):
        result.append({"path": path, "original": old, "candidate": new})
    elif isinstance(old, dict):
        for key in sorted(set(old) | set(new)):
            if key not in old or key not in new:
                result.append({"path": path + "." + key, "original_present": key in old,
                               "candidate_present": key in new, "original": old.get(key), "candidate": new.get(key)})
            else:
                differences(old[key], new[key], path + "." + key, result)
    elif isinstance(old, list):
        if len(old) != len(new):
            result.append({"path": path, "original": old, "candidate": new})
        else:
            for index, (a, b) in enumerate(zip(old, new)):
                differences(a, b, f"{path}[{index}]", result)
    elif old != new:
        result.append({"path": path, "original": old, "candidate": new})
    return result


def compare_case(case, original, candidate, policy):
    old, new = deepcopy(original), deepcopy(candidate)
    expected = {**policy["warning"], "lineno": policy["warning_lines"][case["mode"]]}
    observed_differences = []
    expected_changes = []
    for side, record in [("original", old), ("candidate", new)]:
        if set(record) != {"stdout", "exception", "warnings", "effects"}:
            observed_differences.append({"path": "$", "problem": side + " observation has a missing or extra top-level field"})
    if old.get("warnings") == [expected] and new.get("warnings") == []:
        expected_changes.append({"path": "$.warnings", "reason": policy["allowed_change"],
                                 "original": [expected], "candidate": []})
        old["warnings"] = []
    else:
        observed_differences.append({"path": "$.warnings", "problem": "frozen expected warning transition did not occur",
                                     "original": old.get("warnings"), "candidate": new.get("warnings")})
    observed_differences.extend(differences(old, new))
    return {"id": case["id"], "status": "REGRESSION" if observed_differences else "PASS",
            "original": original, "candidate": candidate, "differences": observed_differences,
            "expected_changes": expected_changes}
