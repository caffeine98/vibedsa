# Writing style

The reader already codes. Teach the idea, not the language.

## Sentences
- Keep sentences under ~20 words. One idea per sentence.
- Use plain words. "Use", not "utilize". "Find", not "determine".
- Never write: *simply, just, obviously, clearly, trivially, easy, leverage, utilize, robust, powerful, delve*.
- Use active voice. "The loop visits each node", not "each node is visited".
- Define a term the first time it appears, or link to the lesson that does.

## Lessons
Every lesson uses these sections, in this order. Skip one only if it adds nothing.

1. **What it is.** 1–3 sentences. No history, no motivation essay.
2. **How it works.** One small worked example. Prefer a trace table.
3. **Pseudocode.** Follow the rules on the "How to read this site" page.
4. **Python.** Imported from `python/dsa/<topic>.py`. Never paste code into the page.
5. **Complexity.** A table. One short reason per row. Say which case: best, average, worst, amortized.
6. **Gotchas.** 2–4 bullets. Real mistakes, not trivia.
7. **In practice.** The Python built-in (if any) and when to use this.

## Examples
- Use the smallest example that shows the idea. Seven array items is usually enough.
- Use the same example through the whole page where possible.
- Data structures: build from scratch first. Then show the built-in in "In practice".

## Python code
- Python 3.12, standard library only.
- Type hints on function signatures. Short docstrings.
- Comments only where the code is not obvious.
- Readable beats clever. No one-liners that hide the idea.
- Keep lines in `python/dsa/` under 80 characters, so code blocks fit without scrolling.
- Every module has tests in `python/tests/`, including edge cases: empty input, one item, duplicates, not found.

## Complexity
- Every claim states its assumptions (e.g. "average case, assuming a good hash function").
- Don't round away important details. Python's `list.pop(0)` is O(n), not O(1).
