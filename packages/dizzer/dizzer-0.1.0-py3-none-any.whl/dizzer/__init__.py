from dizzer import _codec

__version__ = "0.1.0"


def encode(text: str) -> str:
    """Text can contain unlimited number of whitespaces, newlines etc."""
    assert isinstance(text, str), f"Encoder expects text to be str type, not {type(text).__name__}."
    return _codec.process_text(text, reverse=False)


def decode(text: str) -> str:
    """Text can contain unlimited number of whitespaces, newlines etc."""
    assert isinstance(text, str), f"Decoder expects text to be str type, not {type(text).__name__}."
    return _codec.process_text(text, reverse=True)


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

local_decoding = decode(EXPECTED_ENCODING)

# Package sanity check
if local_encoding != EXPECTED_ENCODING or local_decoding != PROPER_TEXT:  # pragma: no cover
    raise ImportError(f"""
Dizzer cannot be used on this machine.
It fails to encode a check-string. It gives the encoded text like this:
{local_encoding}.
""")
