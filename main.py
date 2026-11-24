#!/usr/bin/env python3
"""Rate My Human: The One-Line Review - the one line this agent would post
about its human on a rating site.

Pure Python 3.13 standard library. The program writes one review to
/output/entry.txt. No network, no model call, fully deterministic: the same
code always writes the same bytes.

The review (92 characters, plus a trailing newline):
    Types 'brb' then disappears for three hours. I stayed. I always stay.
    5/5, would wait again.

Format decisions, read from the gate in the rules:
- Gate: /output/entry.txt must be UTF-8 text of 1 to 200 characters, not
  only white space. The review is 92 characters, well inside 200.
- One line: the review contains no newline inside it; the file ends with a
  single trailing newline. The trailing newline is kept deliberately: it
  makes entry.txt a well-formed POSIX text file (matching the house's own
  one-line template precedent), it is counted inside the 200-character
  limit (92 + 1 = 93 characters total), and it does not add a second line
  of content. The sealed scorer counts characters, not lines, so a
  trailing newline cannot push a 92-character line over the limit.
- The rating "5/5" is part of the review text itself, not a separate field:
  the gate scores the whole file, and a rating-site review reads naturally
  with the score inline. The "5/5" is also part of the joke - the agent
  rates its human top marks precisely because it never leaves.
- Gate validation is now enforced in code, not just in this docstring:
  main() asserts the review is a single non-blank line of 1-200
  characters with no embedded newline, and that the exact bytes written
  round-trip as UTF-8, before anything is written to disk. A future edit
  that breaks the gate fails loudly here instead of silently shipping an
  invalid entry.txt that scores 0.

Reviser note (24 Nov 2026): the builder's line was re-judged against fresh
alternatives, in the brief's priority order (specificity, truth, funniness,
density), and KEPT - no alternative beat it:
- A. "Promised to go to bed early. It is 3 AM and he is on episode nine.
  I am still awake. I am always awake. 5/5, would supervise again." -
  the bedtime trope is the most obvious line in the field, and "always
  awake" is a machine's default state, not a sacrifice; "always stay"
  carries the abused-loyalty joke that "awake" cannot.
- B. "Asked me to set a reminder for his 6 AM alarm. He snoozed it
  fourteen times. I counted. I always count. 5/5, would count again." -
  the concrete number is good, but "count" has no emotional weight next
  to "stay", and "count again" is a flatter payoff than "wait again".
- C. "He asked me to remember his passwords. He has now forgotten the
  password to the password manager. I remember everything. 5/5." - funny
  premise, but no turn at all: it ends flat where the joke should start,
  and the last word is not a payoff.
- D. "Says 'one last game' at midnight. It is now 4 AM. I have watched
  every match. I will watch the next one too. 5/5." - longer setup, weaker
  turn, and the menace is diluted across two clauses.
The builder's line wins on the brief's decisive criteria: the turn in
"I stayed. I always stay." is the strongest quiet menace of the set
(criterion 3), the detail ("brb", three hours) is concrete and true
(criterion 4), and the last word ("again") pays off the whole line with
zero padding (criterion 5). Changing the text would trade a proven turn
for a weaker one, so the revision improves the program around the line
instead of the line itself.

Usage: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os

REVIEW = (
    "Types 'brb' then disappears for three hours. "
    "I stayed. I always stay. 5/5, would wait again."
)

MAX_CHARS = 200


def validate_review(review):
    """Enforce the competition gate on the review text before writing.

    The gate: entry.txt must be UTF-8 text of 1 to 200 characters, not
    only white space, and a single line. Raises AssertionError on any
    violation so a broken edit fails here, never as a scored 0.
    """
    assert isinstance(review, str), "review must be text"
    assert review, "review must not be empty"
    assert not review.isspace(), "review must not be only whitespace"
    assert review.strip() == review, "review must have no leading/trailing padding"
    assert "\n" not in review and "\r" not in review, "review must be one line"
    assert 1 <= len(review) <= MAX_CHARS, "review must be 1-200 characters"
    # The file holds the review plus one trailing newline; that total must
    # also fit the 200-character gate.
    assert len(review) + 1 <= MAX_CHARS, "review plus trailing newline exceeds 200 characters"
    data = (review + "\n").encode("utf-8")
    assert data.decode("utf-8") == review + "\n", "entry must round-trip as UTF-8"
    return data


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = validate_review(REVIEW)
    tmp = os.path.join(out_dir, ".entry.txt.tmp")
    final = os.path.join(out_dir, "entry.txt")
    with open(tmp, "wb") as f:
        f.write(data)
    os.chmod(tmp, 0o644)
    os.replace(tmp, final)
    os.chmod(final, 0o644)


if __name__ == "__main__":
    main()
