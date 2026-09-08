# Human maintainer walkthrough — Renewal Engine 0.1.0

Status: NOT TESTED by a human participant. This worksheet is a protocol, not an
observation or claim of adoption. An agent or CI run cannot fill the participant
observations on a person's behalf.

## Participant and setup

A Python maintainer or qualified reviewer agrees to test the public release and
to have the chosen observation summary retained. Use a fresh environment outside
the development VPS and checkout. Record the OS, architecture, actual runtime
versions and executable hashes. Record a public name/handle only with consent;
an anonymous reviewer reference is sufficient for the public summary.

Release: https://github.com/thepianistdirector/renewal-engine/releases/tag/v0.1.0

Download `renewal-engine-0.1.0.tar.gz` and `SHA256SUMS` from that release without
using a developer-supplied copy. Source archive SHA-256:
`2bf2d535ab2c27b87305f960f793151f630d8e70186a52e34ec704cf1eb0c48e`.
CLI SHA-256:
`ee6b2b9e6ba3ffc3e34102dc70ac596b1e3f8479bacd8a6e99072a7c78c80047`.

Follow the included README to extract and install into an explicit local prefix.
Supply trusted Linux x86_64 CPython 3.11.16 and 3.12.14 executable paths as
`BASELINE_PYTHON` and `TARGET_PYTHON`. Record runtime acquisition separately;
no interpreter is distributed with Renewal Engine. Do not use a baseline shim.

## Tasks and observations

1. Install the publicly downloaded archive. Explain what source `inspect` is
   allowed to execute, using the guide. Record any unclear first-run instruction
   or missing prerequisite before receiving assistance.
2. Inspect the bundled reference source and open its patch/report. Identify
   each proposed method/argument edit and at least one unsupported call pattern.
   Confirm the original source did not change. Explain what INSPECTION ONLY
   establishes and what it leaves unmeasured.
3. Run the normal demo using both actual runtimes. Open the report and identify
   the measured cases, intentional change and stated limits. Record the CLI
   exit code and whether the displayed result is understandable without color.
4. Run the negative control into a separate directory. Explain which cases fail,
   which observed fields differ and whether the candidate should be adopted.
   Record the participant's own diagnosis and any assistance needed.
5. Close the terminal/session. Reopen both saved runs with a fresh CLI process.
   Explain the distinction between verifying evidence and a behavioral PASS.
6. Follow the packaged recovery-check command in README. It uses explicit
   stage fault injection and real SIGINT. Inspect an incomplete attempt, verify
   refusal, then open the fresh successful restart. Confirm original-byte
   preservation and that incomplete evidence was not overwritten.
7. Navigate the report with keyboard only: skip link, focus visibility, evidence
   links and native disclosures. Check a narrow window, browser-native 200%
   zoom, labels, non-color status and recovery text. Record exact browser/version,
   observed problems, and any assistive technology actually used. Do not infer
   assistive-technology compatibility from a browser-only observation.

## Required evidence record

- Reviewer reference, role/qualification, consent scope and observation date.
- Public release URL/version, downloaded artifact digest, platform, actual
  baseline/target identities, browser and any assistive technology used.
- Steps actually performed, recorded results, assistance and skipped steps.
- Participant's own negative-control diagnosis and explanation of evidence
  limits; preserve uncertainty or disagreement rather than rewriting it as PASS.
- Installation, inspection, normal/negative and reopening/recovery outcomes;
  original-byte checks and the retained run evidence references.
- Defects, their impact and whether a fix plus fresh participant check is needed.

Status remains NOT TESTED until real observations arrive. A completed protocol
can support USER VALIDATED for its actual scope, never a claim of upstream
adoption, universal accessibility or completion of historical long-term pilots.
