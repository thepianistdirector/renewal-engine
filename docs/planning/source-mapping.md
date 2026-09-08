# Preserved source-to-successor mapping

Generated from `project-plan.json` by `python3 tools/plan.py generate`. Do not edit this view. Canonical SHA-256: `7f8a3a6879964ea924aa7e33f693a8507fa14bc026ba78047769526ffd045827`.

The frozen repository files and downloaded native briefs are retained byte-for-byte. Revision 3 is a reviewed textual plan; it establishes no executed product. Fable fields remain historical bytes and are overridden for current execution by the owner’s Astra-only policy.

Original base `8af461149e2c4b6b3b17d54a10b3559168f8b32f` and briefing HEAD `f434e00913f5df6c78721300ca68625401d87a41` identify different states. No predecessor revision is invented when the source does not state one.

## renewal-engine:W1-T1

Platform: [tsk_17cb9d58845743cb4d031739f78f3ab1](https://tanduna.com/p/renewal-engine/tasks/tsk_17cb9d58845743cb4d031739f78f3ab1/brief), saved revision 3, status READY.

Frozen publication hash: `d09143e713849a2c76cd094a97971d8d325efe091f87a180ee5be89a8d0c26e8`. Brief SHA-256: `0fe355eb34a4636d8c08997c42d3c5c2915dc977825ecaf33db02cf152dc1dd9`.

Treatment: **split**. Preserve maintained upstream fixture requirement; original fixture is a separately approved narrow 0.1 proposal.

Repository structured prerequisites: None recorded.

Native structured prerequisites: Not configured.

Textual prerequisites: None recorded.

Additional textual-only prerequisites: None recorded.

Successors: renewal-engine:N01-01, renewal-engine:N01-02, renewal-engine:N01-03, renewal-engine:N01-04, renewal-engine:N01-05, renewal-engine:N01-06, renewal-engine:N01-07, renewal-engine:N01-08, renewal-engine:N01-09, renewal-engine:N01-10, renewal-engine:N02-09, renewal-engine:N07-02

Original acceptance and successor coverage:

- **Original:** Record licensing, source revisions, supported runtime and the specific migration objective. **Mapped outcomes:** renewal-engine:N01-02, renewal-engine:N01-03, renewal-engine:N01-04, renewal-engine:N01-05, renewal-engine:N01-10, renewal-engine:N07-02. **Historical acceptance state:** NOT TESTED.
- **Original:** List behavior that must remain stable and areas that are intentionally out of scope. **Mapped outcomes:** renewal-engine:N01-05, renewal-engine:N02-09. **Historical acceptance state:** NOT TESTED.

## renewal-engine:W1-T2

Platform: [tsk_a35bd15aa7b3e4318c5552b4cc3e82b3](https://tanduna.com/p/renewal-engine/tasks/tsk_a35bd15aa7b3e4318c5552b4cc3e82b3/brief), saved revision 3, status READY.

Frozen publication hash: `d09143e713849a2c76cd094a97971d8d325efe091f87a180ee5be89a8d0c26e8`. Brief SHA-256: `ad0318622381e4cff09f7f5809d50a089f2d974a45151aa17677f0459302b674`.

Treatment: **split**. Expand the original outcome into falsifiable new scopes without waiving frozen acceptance or prerequisite history.

Repository structured prerequisites: renewal-engine:W1-T1

Native structured prerequisites: tsk_17cb9d58845743cb4d031739f78f3ab1

Textual prerequisites: renewal-engine:W1-T1

Additional textual-only prerequisites: None recorded.

Successors: renewal-engine:N02-01, renewal-engine:N02-02, renewal-engine:N02-03, renewal-engine:N02-04, renewal-engine:N02-05, renewal-engine:N02-06, renewal-engine:N02-07, renewal-engine:N02-08, renewal-engine:N02-09, renewal-engine:N02-10, renewal-engine:N04-08, renewal-engine:N09-01, renewal-engine:N09-02, renewal-engine:N09-03, renewal-engine:N09-04, renewal-engine:N09-05, renewal-engine:N09-06, renewal-engine:N09-07, renewal-engine:N09-08, renewal-engine:N10-01, renewal-engine:N10-02, renewal-engine:N10-03, renewal-engine:N10-04, renewal-engine:N10-05, renewal-engine:N10-06, renewal-engine:N10-07, renewal-engine:N10-08, renewal-engine:N12-04

Original acceptance and successor coverage:

- **Original:** Fixtures run against the original application and fail for a deliberate behavioral regression. **Mapped outcomes:** renewal-engine:N02-08, renewal-engine:N04-08, renewal-engine:N09-08. **Historical acceptance state:** NOT TESTED.
- **Original:** Sensitive or nondeterministic values are handled explicitly rather than silently ignored. **Mapped outcomes:** renewal-engine:N02-09, renewal-engine:N10-01, renewal-engine:N10-07, renewal-engine:N12-04. **Historical acceptance state:** NOT TESTED.

## renewal-engine:W2-T1

Platform: [tsk_17179248999bbb2086133ef8ed4cb216](https://tanduna.com/p/renewal-engine/tasks/tsk_17179248999bbb2086133ef8ed4cb216/brief), saved revision 3, status READY.

Frozen publication hash: `d09143e713849a2c76cd094a97971d8d325efe091f87a180ee5be89a8d0c26e8`. Brief SHA-256: `e84edf23e5d7643683aef682b7d1a7366e4386ebc71fcca9563aa9b55434076d`.

Treatment: **split**. Expand the original outcome into falsifiable new scopes without waiving frozen acceptance or prerequisite history.

Repository structured prerequisites: renewal-engine:W1-T1, renewal-engine:W1-T2

Native structured prerequisites: tsk_17cb9d58845743cb4d031739f78f3ab1, tsk_a35bd15aa7b3e4318c5552b4cc3e82b3

Textual prerequisites: renewal-engine:W1-T1, renewal-engine:W1-T2

Additional textual-only prerequisites: None recorded.

Successors: renewal-engine:N03-01, renewal-engine:N03-02, renewal-engine:N03-03, renewal-engine:N03-04, renewal-engine:N03-05, renewal-engine:N03-06, renewal-engine:N03-07, renewal-engine:N03-08, renewal-engine:N03-09, renewal-engine:N03-10, renewal-engine:N08-01, renewal-engine:N08-02, renewal-engine:N08-03, renewal-engine:N08-04, renewal-engine:N08-05, renewal-engine:N08-06, renewal-engine:N08-07, renewal-engine:N08-08, renewal-engine:N16-01, renewal-engine:N16-02, renewal-engine:N16-03, renewal-engine:N16-04, renewal-engine:N16-05, renewal-engine:N16-06, renewal-engine:N16-07, renewal-engine:N16-08

Original acceptance and successor coverage:

- **Original:** The map links each proposed edit to a concrete migration requirement. **Mapped outcomes:** renewal-engine:N03-01, renewal-engine:N08-06. **Historical acceptance state:** NOT TESTED.
- **Original:** Uncertain or unsupported patterns are surfaced for human review. **Mapped outcomes:** renewal-engine:N03-03, renewal-engine:N03-04, renewal-engine:N08-05. **Historical acceptance state:** NOT TESTED.

## renewal-engine:W2-T2

Platform: [tsk_a9e192b7ec0fa463c48c7b7b3aea4386](https://tanduna.com/p/renewal-engine/tasks/tsk_a9e192b7ec0fa463c48c7b7b3aea4386/brief), saved revision 3, status READY.

Frozen publication hash: `d09143e713849a2c76cd094a97971d8d325efe091f87a180ee5be89a8d0c26e8`. Brief SHA-256: `020caa84d2c10cf0814b510b25eedcc0cd240ca8728d0d6ede91cc07c82c6d17`.

Treatment: **split**. Expand the original outcome into falsifiable new scopes without waiving frozen acceptance or prerequisite history.

Repository structured prerequisites: renewal-engine:W1-T1, renewal-engine:W1-T2, renewal-engine:W2-T1

Native structured prerequisites: tsk_17cb9d58845743cb4d031739f78f3ab1, tsk_a35bd15aa7b3e4318c5552b4cc3e82b3, tsk_17179248999bbb2086133ef8ed4cb216

Textual prerequisites: renewal-engine:W1-T1, renewal-engine:W1-T2, renewal-engine:W2-T1

Additional textual-only prerequisites: None recorded.

Successors: renewal-engine:N03-01, renewal-engine:N03-02, renewal-engine:N03-03, renewal-engine:N03-04, renewal-engine:N03-05, renewal-engine:N03-06, renewal-engine:N03-07, renewal-engine:N03-08, renewal-engine:N03-09, renewal-engine:N03-10, renewal-engine:N07-01, renewal-engine:N07-02, renewal-engine:N07-03, renewal-engine:N07-04, renewal-engine:N07-05, renewal-engine:N07-06, renewal-engine:N07-07, renewal-engine:N07-08, renewal-engine:N11-01, renewal-engine:N11-02, renewal-engine:N11-03, renewal-engine:N11-04, renewal-engine:N11-05, renewal-engine:N11-06, renewal-engine:N11-07, renewal-engine:N11-08, renewal-engine:N16-01, renewal-engine:N16-02, renewal-engine:N16-03, renewal-engine:N16-04, renewal-engine:N16-05, renewal-engine:N16-06, renewal-engine:N16-07, renewal-engine:N16-08, renewal-engine:N22-01, renewal-engine:N22-02, renewal-engine:N22-03, renewal-engine:N22-04, renewal-engine:N22-05, renewal-engine:N22-06, renewal-engine:N22-07, renewal-engine:N22-08

Original acceptance and successor coverage:

- **Original:** The recipe produces a reviewable patch without unrelated rewrites. **Mapped outcomes:** renewal-engine:N03-06, renewal-engine:N03-08. **Historical acceptance state:** NOT TESTED.
- **Original:** Repeated application is stable or explicitly refuses an already migrated source. **Mapped outcomes:** renewal-engine:N03-09, renewal-engine:N03-10. **Historical acceptance state:** NOT TESTED.

## renewal-engine:W3-T1

Platform: [tsk_89e135a4cdda5620e7737ed426e59e3c](https://tanduna.com/p/renewal-engine/tasks/tsk_89e135a4cdda5620e7737ed426e59e3c/brief), saved revision 3, status READY.

Frozen publication hash: `d09143e713849a2c76cd094a97971d8d325efe091f87a180ee5be89a8d0c26e8`. Brief SHA-256: `b58016a7405fc8802d1aa3e841ad4c15ac592d1bc0e3fd8a526aa0d5abd91620`.

Treatment: **split**. Trusted 0.1 subprocess execution is narrower than the frozen isolated-environment requirement; enforced isolation remains later.

Repository structured prerequisites: renewal-engine:W2-T1, renewal-engine:W2-T2

Native structured prerequisites: tsk_17179248999bbb2086133ef8ed4cb216, tsk_a9e192b7ec0fa463c48c7b7b3aea4386

Textual prerequisites: renewal-engine:W2-T1, renewal-engine:W2-T2

Additional textual-only prerequisites: None recorded.

Successors: renewal-engine:N04-01, renewal-engine:N04-02, renewal-engine:N04-03, renewal-engine:N04-04, renewal-engine:N04-05, renewal-engine:N04-06, renewal-engine:N04-07, renewal-engine:N04-08, renewal-engine:N04-09, renewal-engine:N04-10, renewal-engine:N09-01, renewal-engine:N09-02, renewal-engine:N09-03, renewal-engine:N09-04, renewal-engine:N09-05, renewal-engine:N09-06, renewal-engine:N09-07, renewal-engine:N09-08, renewal-engine:N10-01, renewal-engine:N10-02, renewal-engine:N10-03, renewal-engine:N10-04, renewal-engine:N10-05, renewal-engine:N10-06, renewal-engine:N10-07, renewal-engine:N10-08, renewal-engine:N14-01, renewal-engine:N14-02, renewal-engine:N14-03, renewal-engine:N14-04, renewal-engine:N14-05, renewal-engine:N14-06, renewal-engine:N14-07, renewal-engine:N14-08, renewal-engine:N16-01, renewal-engine:N16-02, renewal-engine:N16-03, renewal-engine:N16-04, renewal-engine:N16-05, renewal-engine:N16-06, renewal-engine:N16-07, renewal-engine:N16-08

Original acceptance and successor coverage:

- **Original:** Reports distinguish expected changes, regressions and unmeasured behavior. **Mapped outcomes:** renewal-engine:N04-06, renewal-engine:N04-07, renewal-engine:N04-09, renewal-engine:N14-08. **Historical acceptance state:** NOT TESTED.
- **Original:** The deliberately wrong transformation is detected. **Mapped outcomes:** renewal-engine:N04-08, renewal-engine:N04-10. **Historical acceptance state:** NOT TESTED.

## renewal-engine:W3-T2

Platform: [tsk_7e9f19f4a3e6ff05eb357075dac35818](https://tanduna.com/p/renewal-engine/tasks/tsk_7e9f19f4a3e6ff05eb357075dac35818/brief), saved revision 3, status READY.

Frozen publication hash: `d09143e713849a2c76cd094a97971d8d325efe091f87a180ee5be89a8d0c26e8`. Brief SHA-256: `07e3f475efa8ed0c37ddf92360fe6ee2cfda4803634fa608c74480be0ee50fe9`.

Treatment: **split**. Narrow source retention and offline review now; selective rejection, data restoration and maintainer observation remain distinct later outcomes.

Repository structured prerequisites: renewal-engine:W2-T1, renewal-engine:W2-T2, renewal-engine:W3-T1

Native structured prerequisites: tsk_17179248999bbb2086133ef8ed4cb216, tsk_a9e192b7ec0fa463c48c7b7b3aea4386, tsk_89e135a4cdda5620e7737ed426e59e3c

Textual prerequisites: renewal-engine:W2-T1, renewal-engine:W2-T2, renewal-engine:W3-T1

Additional textual-only prerequisites: None recorded.

Successors: renewal-engine:N05-01, renewal-engine:N05-02, renewal-engine:N05-03, renewal-engine:N05-04, renewal-engine:N05-05, renewal-engine:N05-06, renewal-engine:N05-07, renewal-engine:N05-08, renewal-engine:N05-09, renewal-engine:N05-10, renewal-engine:N11-01, renewal-engine:N11-02, renewal-engine:N11-03, renewal-engine:N11-04, renewal-engine:N11-05, renewal-engine:N11-06, renewal-engine:N11-07, renewal-engine:N11-08, renewal-engine:N18-06, renewal-engine:N19-01, renewal-engine:N19-02, renewal-engine:N19-03, renewal-engine:N19-04, renewal-engine:N19-05, renewal-engine:N19-06, renewal-engine:N19-07, renewal-engine:N19-08, renewal-engine:N24-04, renewal-engine:N25-01, renewal-engine:N25-02, renewal-engine:N25-03, renewal-engine:N25-04, renewal-engine:N25-05, renewal-engine:N25-06, renewal-engine:N25-07, renewal-engine:N25-08

Original acceptance and successor coverage:

- **Original:** A maintainer can reject individual changes and reproduce the comparison. **Mapped outcomes:** renewal-engine:N11-05, renewal-engine:N25-01, renewal-engine:N24-04. **Historical acceptance state:** NOT TESTED.
- **Original:** Document how to return to the prior source and data state within the bounded migration. **Mapped outcomes:** renewal-engine:N05-04, renewal-engine:N18-06, renewal-engine:N19-08. **Historical acceptance state:** NOT TESTED.

## renewal-engine:W4-T1

Platform: [tsk_79615ef58d4b13fae68ef7d5e7314eeb](https://tanduna.com/p/renewal-engine/tasks/tsk_79615ef58d4b13fae68ef7d5e7314eeb/brief), saved revision 3, status READY.

Frozen publication hash: `d09143e713849a2c76cd094a97971d8d325efe091f87a180ee5be89a8d0c26e8`. Brief SHA-256: `e734e0c6b76c797040ab6e0a6013fdf6604d0151effa1408814e665c80ddd3eb`.

Treatment: **split**. Independent recipe kit and second maintainer authorship remain later, not prerequisites for the narrow CLI.

Repository structured prerequisites: renewal-engine:W3-T1, renewal-engine:W3-T2

Native structured prerequisites: tsk_89e135a4cdda5620e7737ed426e59e3c, tsk_7e9f19f4a3e6ff05eb357075dac35818

Textual prerequisites: renewal-engine:W3-T1, renewal-engine:W3-T2

Additional textual-only prerequisites: None recorded.

Successors: renewal-engine:N06-01, renewal-engine:N06-02, renewal-engine:N06-03, renewal-engine:N06-04, renewal-engine:N06-05, renewal-engine:N06-06, renewal-engine:N06-07, renewal-engine:N06-08, renewal-engine:N07-01, renewal-engine:N07-02, renewal-engine:N07-03, renewal-engine:N07-04, renewal-engine:N07-05, renewal-engine:N07-06, renewal-engine:N07-07, renewal-engine:N07-08, renewal-engine:N13-01, renewal-engine:N13-02, renewal-engine:N13-03, renewal-engine:N13-04, renewal-engine:N13-05, renewal-engine:N13-06, renewal-engine:N13-07, renewal-engine:N13-08, renewal-engine:N15-01, renewal-engine:N15-02, renewal-engine:N15-03, renewal-engine:N15-04, renewal-engine:N15-05, renewal-engine:N15-06, renewal-engine:N15-07, renewal-engine:N15-08

Original acceptance and successor coverage:

- **Original:** A second maintainer can author and run a recipe using only the documented interfaces. **Mapped outcomes:** renewal-engine:N13-07, renewal-engine:N13-08. **Historical acceptance state:** NOT TESTED.
- **Original:** Unsupported versions stop with an explicit reason. **Mapped outcomes:** renewal-engine:N06-02, renewal-engine:N13-03. **Historical acceptance state:** NOT TESTED.

## renewal-engine:W4-T2

Platform: [tsk_57ea7445d8928fcd6b0c9890b459a98a](https://tanduna.com/p/renewal-engine/tasks/tsk_57ea7445d8928fcd6b0c9890b459a98a/brief), saved revision 3, status READY.

Frozen publication hash: `d09143e713849a2c76cd094a97971d8d325efe091f87a180ee5be89a8d0c26e8`. Brief SHA-256: `63af8db5a807104abc28af4b640312b2d738d0dc2a0b38eb7d8b4531aeba454f`.

Treatment: **split**. Split trusted local no-upload 0.1 from full private-code isolation and optional-provider scopes.

Repository structured prerequisites: renewal-engine:W3-T1, renewal-engine:W3-T2

Native structured prerequisites: tsk_89e135a4cdda5620e7737ed426e59e3c, tsk_7e9f19f4a3e6ff05eb357075dac35818

Textual prerequisites: renewal-engine:W3-T1, renewal-engine:W3-T2

Additional textual-only prerequisites: None recorded.

Successors: renewal-engine:N05-01, renewal-engine:N05-02, renewal-engine:N05-03, renewal-engine:N05-04, renewal-engine:N05-05, renewal-engine:N05-06, renewal-engine:N05-07, renewal-engine:N05-08, renewal-engine:N05-09, renewal-engine:N05-10, renewal-engine:N12-01, renewal-engine:N12-02, renewal-engine:N12-03, renewal-engine:N12-04, renewal-engine:N12-05, renewal-engine:N12-06, renewal-engine:N12-07, renewal-engine:N12-08, renewal-engine:N14-01, renewal-engine:N14-02, renewal-engine:N14-03, renewal-engine:N14-04, renewal-engine:N14-05, renewal-engine:N14-06, renewal-engine:N14-07, renewal-engine:N14-08, renewal-engine:N22-01, renewal-engine:N22-02, renewal-engine:N22-03, renewal-engine:N22-04, renewal-engine:N22-05, renewal-engine:N22-06, renewal-engine:N22-07, renewal-engine:N22-08

Original acceptance and successor coverage:

- **Original:** A run can complete without uploading source to a hosted service. **Mapped outcomes:** renewal-engine:N12-02, renewal-engine:N12-08. **Historical acceptance state:** NOT TESTED.
- **Original:** Any optional model request shows its data boundary and requires explicit configuration. **Mapped outcomes:** renewal-engine:N12-05, renewal-engine:N22-02, renewal-engine:N22-03. **Historical acceptance state:** NOT TESTED.

## renewal-engine:W5-T1

Platform: [tsk_e68f1340d670a17234cd0e91c5691fc1](https://tanduna.com/p/renewal-engine/tasks/tsk_e68f1340d670a17234cd0e91c5691fc1/brief), saved revision 3, status READY.

Frozen publication hash: `d09143e713849a2c76cd094a97971d8d325efe091f87a180ee5be89a8d0c26e8`. Brief SHA-256: `4b8cae28e28b5ed3338b36c29ce49e10447cbe0ad94ae84665a6ac3bc6b9d2bc`.

Treatment: **expanded and deferred**. Expand the original outcome into falsifiable new scopes without waiving frozen acceptance or prerequisite history.

Repository structured prerequisites: renewal-engine:W4-T1, renewal-engine:W4-T2

Native structured prerequisites: tsk_79615ef58d4b13fae68ef7d5e7314eeb, tsk_57ea7445d8928fcd6b0c9890b459a98a

Textual prerequisites: renewal-engine:W4-T1, renewal-engine:W4-T2

Additional textual-only prerequisites: None recorded.

Successors: renewal-engine:N17-01, renewal-engine:N17-02, renewal-engine:N17-03, renewal-engine:N17-04, renewal-engine:N17-05, renewal-engine:N17-06, renewal-engine:N17-07, renewal-engine:N17-08

Original acceptance and successor coverage:

- **Original:** A staged fixture demonstrates old/new compatibility during the transition. **Mapped outcomes:** renewal-engine:N17-02, renewal-engine:N17-04, renewal-engine:N17-08. **Historical acceptance state:** NOT TESTED.
- **Original:** An unsafe ordering is rejected or clearly marked as requiring coordinated downtime. **Mapped outcomes:** renewal-engine:N17-03, renewal-engine:N17-05. **Historical acceptance state:** NOT TESTED.

## renewal-engine:W5-T2

Platform: [tsk_5d9c9f4b35e62de3e818ee428565ce91](https://tanduna.com/p/renewal-engine/tasks/tsk_5d9c9f4b35e62de3e818ee428565ce91/brief), saved revision 3, status READY.

Frozen publication hash: `d09143e713849a2c76cd094a97971d8d325efe091f87a180ee5be89a8d0c26e8`. Brief SHA-256: `71b43023664a455da90197f3e39d45d1380fc0190592d8191211cf0303649530`.

Treatment: **expanded and deferred**. Expand the original outcome into falsifiable new scopes without waiving frozen acceptance or prerequisite history.

Repository structured prerequisites: renewal-engine:W4-T1, renewal-engine:W4-T2, renewal-engine:W5-T1

Native structured prerequisites: tsk_79615ef58d4b13fae68ef7d5e7314eeb, tsk_57ea7445d8928fcd6b0c9890b459a98a, tsk_e68f1340d670a17234cd0e91c5691fc1

Textual prerequisites: renewal-engine:W4-T1, renewal-engine:W4-T2, renewal-engine:W5-T1

Additional textual-only prerequisites: None recorded.

Successors: renewal-engine:N18-01, renewal-engine:N18-02, renewal-engine:N18-03, renewal-engine:N18-04, renewal-engine:N18-05, renewal-engine:N18-06, renewal-engine:N18-07, renewal-engine:N18-08, renewal-engine:N19-01, renewal-engine:N19-02, renewal-engine:N19-03, renewal-engine:N19-04, renewal-engine:N19-05, renewal-engine:N19-06, renewal-engine:N19-07, renewal-engine:N19-08

Original acceptance and successor coverage:

- **Original:** The chosen migration demonstrates recovery from an interrupted data step. **Mapped outcomes:** renewal-engine:N18-03, renewal-engine:N18-06. **Historical acceptance state:** NOT TESTED.
- **Original:** The report distinguishes reversible source changes from irreversible data loss risks. **Mapped outcomes:** renewal-engine:N18-07, renewal-engine:N19-01, renewal-engine:N19-05. **Historical acceptance state:** NOT TESTED.

## renewal-engine:W6-T1

Platform: [tsk_c5c45d54c7d504d440dc18fdd697b84a](https://tanduna.com/p/renewal-engine/tasks/tsk_c5c45d54c7d504d440dc18fdd697b84a/brief), saved revision 3, status READY.

Frozen publication hash: `d09143e713849a2c76cd094a97971d8d325efe091f87a180ee5be89a8d0c26e8`. Brief SHA-256: `16cb73759a934b74333a16ef9b5d8155eb39263399e3de7ba2edfb73ce637764`.

Treatment: **expanded and deferred**. A narrow external 0.1 user observation does not satisfy full volunteer pilot adoption after original W5 dependencies.

Repository structured prerequisites: renewal-engine:W5-T1, renewal-engine:W5-T2

Native structured prerequisites: tsk_e68f1340d670a17234cd0e91c5691fc1, tsk_5d9c9f4b35e62de3e818ee428565ce91

Textual prerequisites: renewal-engine:W5-T1, renewal-engine:W5-T2

Additional textual-only prerequisites: None recorded.

Successors: renewal-engine:N05-01, renewal-engine:N05-02, renewal-engine:N05-03, renewal-engine:N05-04, renewal-engine:N05-05, renewal-engine:N05-06, renewal-engine:N05-07, renewal-engine:N05-08, renewal-engine:N05-09, renewal-engine:N05-10, renewal-engine:N24-01, renewal-engine:N24-02, renewal-engine:N24-03, renewal-engine:N24-04, renewal-engine:N24-05, renewal-engine:N24-06, renewal-engine:N24-07, renewal-engine:N24-08

Original acceptance and successor coverage:

- **Original:** Report accepted, rejected and revised patches without treating patch generation as adoption. **Mapped outcomes:** renewal-engine:N24-04, renewal-engine:N24-05. **Historical acceptance state:** NOT TESTED.
- **Original:** Capture missed behavior and incorporate it into fixtures. **Mapped outcomes:** renewal-engine:N24-06, renewal-engine:N24-08. **Historical acceptance state:** NOT TESTED.

## renewal-engine:W6-T2

Platform: [tsk_4094a1ff51d72e4a7b4a14420a3f3c48](https://tanduna.com/p/renewal-engine/tasks/tsk_4094a1ff51d72e4a7b4a14420a3f3c48/brief), saved revision 3, status READY.

Frozen publication hash: `d09143e713849a2c76cd094a97971d8d325efe091f87a180ee5be89a8d0c26e8`. Brief SHA-256: `02d311a65fa6136a9ce6fe8bdf3a20648818057e43fab5882f08dc6c791005ce`.

Treatment: **expanded and deferred**. Expand the original outcome into falsifiable new scopes without waiving frozen acceptance or prerequisite history.

Repository structured prerequisites: renewal-engine:W5-T1, renewal-engine:W5-T2, renewal-engine:W6-T1

Native structured prerequisites: tsk_e68f1340d670a17234cd0e91c5691fc1, tsk_5d9c9f4b35e62de3e818ee428565ce91, tsk_c5c45d54c7d504d440dc18fdd697b84a

Textual prerequisites: renewal-engine:W5-T1, renewal-engine:W5-T2, renewal-engine:W6-T1

Additional textual-only prerequisites: None recorded.

Successors: renewal-engine:N20-01, renewal-engine:N20-02, renewal-engine:N20-03, renewal-engine:N20-04, renewal-engine:N20-05, renewal-engine:N20-06, renewal-engine:N20-07, renewal-engine:N20-08, renewal-engine:N21-01, renewal-engine:N21-02, renewal-engine:N21-03, renewal-engine:N21-04, renewal-engine:N21-05, renewal-engine:N21-06, renewal-engine:N21-07, renewal-engine:N21-08, renewal-engine:N23-01, renewal-engine:N23-02, renewal-engine:N23-03, renewal-engine:N23-04, renewal-engine:N23-05, renewal-engine:N23-06, renewal-engine:N23-07, renewal-engine:N23-08, renewal-engine:N26-01, renewal-engine:N26-02, renewal-engine:N26-03, renewal-engine:N26-04, renewal-engine:N26-05, renewal-engine:N26-06, renewal-engine:N26-07, renewal-engine:N26-08

Original acceptance and successor coverage:

- **Original:** A changed dependency that invalidates a recipe is caught by a reproducible check. **Mapped outcomes:** renewal-engine:N23-03. **Historical acceptance state:** NOT TESTED.
- **Original:** Maintainers can see the last verified versions and remaining gaps. **Mapped outcomes:** renewal-engine:N20-05, renewal-engine:N23-02, renewal-engine:N23-07. **Historical acceptance state:** NOT TESTED.
