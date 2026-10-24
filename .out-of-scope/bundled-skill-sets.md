# Bundling another skill set into EEP

Shipping another author's whole skill set inside EEP, or making an EEP skill depend on one being
installed.

## Why this is out of scope

Every model-invoked skill keeps its description in context on every turn. Bundling a set of about 15
skills would add that cost for every EEP user and give two skills the same trigger (grilling, code
review), so which one fires becomes a coin flip. EEP takes individual techniques instead, keeps the
upstream licence beside them and names the source in the CHANGELOG.

## Prior requests

None filed yet. Decided during the 2026-10-18 review of mattpocock/skills.

## Instead

Install the other set yourself; where two skills cover the same job (the README's companion list
notes a few), disable one side so routing stays predictable. A technique worth
porting is a normal issue: cite the session where EEP's version failed.
