#!/usr/bin/env python3
"""Excuse writer: the almost-believable reason for skipping work.

EXCUSE is the whole program's payload. It is checked by a table of
(test, complaint) pairs in TESTS, in table order, and written to
/output/entry.txt only when every test is happy. The joke depends on
what the excuse never says, so one test forbids naming the game.
"""

import sys

EXCUSE = "My internet is down and the technician cannot come until Friday. I will be completely offline all week."
CHAR_MAX = 140
WORD_MAX = 20
OUT_FILE = "/output/entry.txt"
FINISHERS = (".", "!", "?")
MARK_SET = set(".,!?;:'\"-() ")


def die(message):
    print(f"invalid excuse: {message}", file=sys.stderr)
    raise SystemExit(1)


def exists(line):
    return bool(line and line.strip())


def short_enough(line):
    return len(line) <= CHAR_MAX


def few_enough_words(line):
    return len(line.split()) <= WORD_MAX


def no_control_chars(line):
    return all(ord(c) >= 32 for c in line)


def tidy(line):
    return line == line.strip() and "  " not in line and "\n" not in line


def has_letters(line):
    return any(c.isalpha() for c in line)


def not_only_punctuation(line):
    return not all(c in MARK_SET for c in line)


def not_only_digits(line):
    return not line.strip().isdigit()


def ends_with_punctuation(line):
    return line.rstrip().endswith(FINISHERS)


def never_names_the_game(line):
    return "GTA" not in line and "game" not in line.lower()


def never_links_out(line):
    # An excuse that links somewhere is not an excuse, it is a redirect.
    lowered = line.lower()
    return "http://" not in lowered and "https://" not in lowered and "www." not in lowered


TESTS = [
    (exists, "excuse is empty"),
    (short_enough, "excuse is over the 140 character limit"),
    (few_enough_words, "excuse is over the 20 word limit"),
    (no_control_chars, "excuse has control characters"),
    (tidy, "excuse has leading/trailing/double spaces or a newline"),
    (has_letters, "excuse has no letters"),
    (not_only_punctuation, "excuse is only punctuation"),
    (not_only_digits, "excuse is only digits"),
    (ends_with_punctuation, "excuse must end with punctuation"),
    (never_names_the_game, "the excuse must not name the game, that is the joke"),
    (never_links_out, "the excuse must not contain a link"),
]


def validate(line):
    for test, complaint in TESTS:
        if not test(line):
            die(complaint)


def main():
    validate(EXCUSE)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(EXCUSE + "\n")


if __name__ == "__main__":
    main()
