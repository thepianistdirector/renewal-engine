# Decision 004: public release and external reproduction

State: owner approved the exact GitHub publication packet on September 8, 2026.
Publication completed under the existing `thepianistdirector` account. Tag
`v0.1.0` points to `737dc0867d5b4e6c8f3ba29f04fade8573ff683d`. The approved CLI,
source archive and SHA256SUMS were uploaded; public readback and anonymous
artifact downloads match their exact digests. See `docs/evidence/public-release.json`.

The approval packet's next action is fresh external reproduction of the
publicly obtained release. Use a standard `ubuntu-24.04` GitHub-hosted runner
in this public repository: GitHub documents standard hosted execution for public
repositories as free. No paid runner, artifact storage, third-party action,
checkout, user credential, repository write token, sudo or shared host change
is used. Job permissions are empty; timeout is 25 minutes; compilation is
bounded to two jobs at a time. This is external agent runtime evidence, not
human observation or adoption.

The dedicated `codex/renewal-engine-public-verification` branch contains only
an additional verification workflow over the released commit. It preserves
the release tag and assets; it does not merge into main. Its verified local
worktree belongs to this same repository at
`.local/worktrees/public-verification`. Workflow commit:
`400f269d780fd7dd720eb0947939454dba0845d5`.

Execution downloads the public source archive anonymously and checks its
approved SHA-256, installs the bundled CLI and verifies its exact hash. It builds
both real interpreters in its disposable project workspace from official PSF
source, without redistributing binaries, then runs the packaged verification
script. Normal/negative observations, idempotence, two real SIGINT stages and
fresh restart must all pass. Retained observations go to the workflow log as a
bounded compressed evidence record; build logs and developer paths are excluded.
Failure remains visible and is not normalized or relabeled as success.

Sources:

- https://docs.github.com/en/billing/concepts/product-billing/github-actions
- https://www.python.org/downloads/release/python-31116/
- https://www.python.org/downloads/release/python-31214/

Official source XZ hashes:

- 3.11.16: `91bcdebfdde239a003ae93738a7fce0f9230fee5c4bc2b86f6e6e8c6f98aabe8`
- 3.12.14: `5c8462af5790baf43a321a1559dbe0db06d1be4300fb85fb53c40060668e548a`

The baseline source/PSF notices were reviewed before the original project-local
build. The target is the already approved 3.12.14 matrix version; this check uses
its official source in the external environment. No production dependency graph
or supported-version promise is expanded by this verification setup.

A consenting maintainer still needs to perform the separate protocol in
`docs/publication/maintainer-walkthrough.md`. Native Tanduna publication still
requires its supported connection, exact proposal approval and public readback.
