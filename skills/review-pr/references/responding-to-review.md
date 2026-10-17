## Answering pushback on your own PR

When a reviewer (human or an automated checker) flags something on a PR you wrote, agreeing and
fixing it is not enough — say why the objection was right with a concrete example (a runnable
snippet, the exact input that breaks, the exact assertion that would still pass for the wrong
reason), then fix it in a named follow-up commit. An assertion that only checks "some change
happened" is not pinning the bug; say so explicitly if that's what the pushback exposed.

Format for an outside contribution: **Problem** (quantified — the exact failure size, not "this is
slow") → **Fix** (name the upstream convention or existing pattern being followed) → **Testing**
(the exact command and its output, what stays unchanged). Name any faked, placeholder, or
not-yet-implemented content in the PR body before anyone can be misled by it.
