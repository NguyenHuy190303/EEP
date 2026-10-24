# A router or playbook skill

A skill whose job is to pick which other skill or playbook runs next.

## Why this is out of scope

The harness already routes: the model picks a skill by its description inside its own turn, at no
extra call. A router in front of that pays twice for the same decision, and every skill then needs
a second pointer kept in sync. EEP spends the effort on sharper descriptions instead (see
`engineer-mindset/modules/writing-for-agents`).

## Prior requests

None filed yet. Decided during the 2026-10-18 review of pstack's router/playbook layer.

## Instead

If a skill fires at the wrong time, file it with the session: that is a description bug EEP fixes.
For your own user-invoked skills, a short list in your `CLAUDE.md` does the routing.
