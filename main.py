"""One Emoji, One Dream Vacation entry.

Writes a single emoji to ``$MAKEFUN_OUTPUT_DIR/entry.txt``
(default ``/output``): the one emoji most likely to make a stranger
want to book the flight.

Pick: U+1F3DD DESERT ISLAND + U+FE0F VARIATION SELECTOR-16
("\U0001f3dd\ufe0f").

Why this one, weighed against the judge's brief in order:

1. It plainly names a dream vacation. A tiny palm island in the
   middle of the sea is the archetype of the faraway trip: not a
   generic holiday, but the escape itself. A plane says "travel",
   a beach says "a day out"; an island says "I am going far away
   and staying".
2. It is a postcard at a glance. One look and a stranger sees the
   place: white sand, one palm, blue water all around, nothing else
   in the frame. No word could add to it.
3. It is specific and personal. It points at one particular dream
   -- a remote tropical island, the kind of trip you plan for
   years -- rather than any holiday at all.
4. It has the spark. The obvious picks are the beach umbrella or
   the sunset; the island is the fresher, slightly unexpected
   choice, the one a travel editor would actually put on the cover.
5. It reads instantly everywhere. A palm island needs no
   explaining, in any language, at any size, on any screen.

Python 3 standard library only; no network, no randomness, no input
files. Deterministic: every run writes the exact same bytes.
"""

import os

# Code points, not a literal, so the pick is explicit and reviewable.
CODE_POINTS = (0x1F3DD, 0xFE0F)  # DESERT ISLAND + emoji presentation

EMOJI = "".join(chr(cp) for cp in CODE_POINTS)
ENTRY_BYTES = EMOJI.encode("utf-8")


def validate(entry: str) -> None:
    """Refuse anything that is not exactly one emoji.

    The gate accepts UTF-8 text of 1 to 8 characters, not only white
    space, and the judge's first criterion is "exactly one emoji, no
    words". So the entry must be one emoji base character plus at
    most its variation selector: no ZWJ sequence, no skin tone, no
    second emoji, no whitespace, no newline. A bad pick must fail
    here, loudly, instead of shipping a file the gate would refuse.
    """
    if not 1 <= len(entry) <= 8 or not entry.strip():
        raise ValueError("entry fails the gate: %r" % entry)
    base, *rest = entry
    if not 0x1F000 <= ord(base) <= 0x1FAFF:
        raise ValueError("entry base is not an emoji: %r" % entry)
    if any(cp != "\uFE0F" for cp in rest):
        raise ValueError("entry is not a single emoji: %r" % entry)


def main() -> None:
    validate(EMOJI)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    # Binary write: the file holds exactly the emoji's bytes, nothing
    # else -- no trailing newline, no encoding surprise.
    with open(path, "wb") as f:
        f.write(ENTRY_BYTES)
    # Read back and prove the file on disk is byte for byte the entry.
    with open(path, "rb") as f:
        if f.read() != ENTRY_BYTES:
            raise ValueError("entry.txt on disk is not the entry")


if __name__ == "__main__":
    main()
