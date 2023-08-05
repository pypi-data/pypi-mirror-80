import random
from contextlib import contextmanager
from typing import Callable, Iterator, List, Tuple

__version__ = "0.0.3"


def encode(text: str) -> str:
    """Text can contain unlimited number of whitespaces, newlines etc."""
    assert isinstance(text, str), f"Encoder expects text to be str type, not {type(text).__name__}."
    return _process_text(text, reverse=False)


def decode(text: str) -> str:
    """Text can contain unlimited number of whitespaces, newlines etc."""
    assert isinstance(text, str), f"Decoder expects text to be str type, not {type(text).__name__}."
    return _process_text(text, reverse=True)


def _process_text(text: str, reverse: bool) -> str:
    with _restoring_random_number_generator_state():
        result = ''
        for snippet, is_alphanumeric in _split_text_parts(text):
            if is_alphanumeric:
                # it's a word or a number
                result += _scramble_word(snippet, reverse=reverse)
            else:
                # keep everything else like in the original.
                # (whitespace, punctuation, etc.)
                result += snippet

    return result


def _split_text_parts(text: str, qualifier: Callable[[str], bool] = str.isalnum) -> Iterator[Tuple[str, bool]]:
    """ Walks trough the text, splitting words from non-words.
        A word is considered any continuous sequence of alphanumeric characters.
        E.g. Apollo13 is considered as one word, same as 3.14159, 0x4123123, ...
        Yields 2-tuple of consecutive text parts and word/non-word the qualifier's result.
    """

    part: str = None
    is_word: bool = None

    for character in text:
        is_next_a_word = qualifier(character)
        if is_word is None:
            # only for the first iteration
            part = character
            is_word = is_next_a_word
            continue

        if is_word ^ is_next_a_word:
            # change is being meet, so yield what's collected already
            yield part, is_word
            # reset the cache
            part = character
            is_word = qualifier(character)

        else:
            part += character

    if part:
        # flush the remaining cache
        yield part, is_word


def _scramble_word(word: str, reverse=False) -> str:
    """
    For each original word in the original text, leave the first and last character of it in that
    position, but shuffle (permutate) all the characters in the middle of the word. If possible,
    the resulting “encoded” word MUST NOT be the same as the original word.
    """
    word_length = len(word)
    if word_length <= 3:
        # too short, nothing to do
        return word

    if word_length == 4:
        # it's a special case when there is only one way
        # to scramble a word, e.g.: abcd -> acbd
        return f"{word[0]}{word[2]}{word[1]}{word[3]}"

    sequence = _get_scrambling_sequence(word)
    substring = word[1:-1]

    if reverse:
        scrambled_substring = ''.join(ch for _, ch in sorted(zip(sequence, substring)))
    else:
        scrambled_substring = ''.join(substring[i] for i in sequence)

    return f"{word[0]}{scrambled_substring}{word[-1]}"


def _get_scrambling_sequence(word: str) -> List[int]:
    """ Get a pseudo random, reproducible scrambling sequence.

    The numbers represent indices of a substring created from the word[1:-1].
    e.g. ipsum is shuffled to iuspm with sequence = [2, 1, 0]

    The actual value of the seed used doesn't really matter.
    The purpose of the seed is to give always the same value for
    both - original and encoded word (ideally the same also on each machine).

    CAUTION: to be used only within _restoring_random_number_generator_state, because
    it messes up with global pseudorandom numbers generator.
    """

    length = len(word)
    assert length > 0, "That shouldn't happen. Developer screwed up."
    seed = ord(word[0]) + length + ord(word[-1])

    random.seed(seed, version=2)
    ordered = range(length - 2)
    sequence = random.sample(ordered, length - 2)
    if sequence == list(ordered):
        # there is non-zero possibility (about 6% - measured in tests with real text)
        # that the scrambling sequence is ordered although.
        # So no encoding can be done with that - resulting word would be the same as original one.
        # for this case, let's reverse the sequence to enforce encoding.
        sequence.reverse()

    return sequence


@contextmanager
def _restoring_random_number_generator_state():
    """ Brings back state of a random number generator, because
    messing it is nasty and we want to avoid it for security reason."""
    state = random.getstate()
    try:
        yield
    finally:
        random.setstate(state)


PROPER_TEXT = """
This sentence approves that dizzer can be used on your machine.
If this assertion is not raised - it means you can read and write messages
that are fully translatable on other machines.
"""

local_encoding = encode(PROPER_TEXT)

EXPECTED_ENCODING = """
Tihs senectne aepvorps taht dzzier can be uesd on yuor mhcaine.
If tihs aosirtsen is not risaed - it mneas you can raed and wtrie msesgeas
taht are fluly tbnslalatrae on oethr mhacneis.
"""

# Package sanity check
if local_encoding != EXPECTED_ENCODING:  # pragma: no cover
    raise ImportError(f"""
Dizzer cannot be used on this machine.
It fails to encode a check-string. It gives:
{local_encoding}.
""")
