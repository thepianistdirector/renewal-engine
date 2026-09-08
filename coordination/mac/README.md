# Mac helper bridge

Paste [MAC-HELPER-PROMPT.md](MAC-HELPER-PROMPT.md) into a GPT-6 Astra task running
locally on Lucas's Mac. It instructs that task to create the actual native
15-minute schedule, run once immediately and keep checking
[requests.json](requests.json). The schedule has not been created on this VPS.
Its actual Mac ID/readback must arrive in the helper registration.

The remote owner writes requests on `codex/renewal-engine-0.1`. The Mac returns
public-safe registration/results on `codex/mac-helper-results`, following
[PROTOCOL.md](PROTOCOL.md). The local Mac registry can later hold other explicitly
approved feeds without mixing their repositories or permissions.

Initial work: helper setup, local Tanduna connection, native plan preparation
and assistance with the human maintainer walkthrough. Login and real participant
observations remain human actions. An unavailable scheduling tool must not block
independent one-time setup, connection checks or review preparation.

Current official scheduling guidance supports minute-based schedules inside an
existing task and requires the computer/app to remain available for local work:
[Scheduled tasks](https://learn.chatgpt.com/docs/automations?surface=app).
The destination must discover its actual scheduling tool schema and verify
creation; these files alone do not establish a running scheduled task.
