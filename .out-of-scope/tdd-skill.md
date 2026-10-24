# A TDD loop skill

A skill that drives red-green(-refactor) test-first development.

## Why this is out of scope

The test-first loop depends on the language, framework and test runner, and the candidate upstream
skill is TypeScript-shaped and contradicts its own README on whether refactoring is part of the
loop. EEP already holds the parts that transfer: `investigate` requires a red loop before any
theory, and `review-pr` follows the change into its tests.

## Prior requests

None filed yet. Decided during the 2026-10-18 review of mattpocock/skills (`tdd`).

## Instead

Use a TDD skill made for your stack (the README's companion list names one), or write the loop
your repo uses in its `CLAUDE.md`.
