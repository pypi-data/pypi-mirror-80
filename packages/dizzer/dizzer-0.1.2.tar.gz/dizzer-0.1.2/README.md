
[![PyPI version](https://img.shields.io/pypi/v/dizzer.svg)](https://pypi.python.org/pypi/dizzer/)
[![pipeline status](https://gitlab.com/kamichal/dizzer/badges/master/pipeline.svg)](https://gitlab.com/kamichal/dizzer/-/commits/master)
[![coverage report](https://gitlab.com/kamichal/dizzer/badges/master/coverage.svg)](https://gitlab.com/kamichal/dizzer/-/commits/master)
[![PyPI pyversion](https://img.shields.io/pypi/pyversions/DIZER.svg)](https://pypi.org/project/dizzer/)
[![PyPI license](https://img.shields.io/pypi/l/DIZZER.svg)](https://pypi.python.org/pypi/dizzer/)
[![PyPI status](https://img.shields.io/pypi/status/DIZZER.svg)](https://pypi.python.org/pypi/dizzer/)

### DIZZER

#### Bidirectional human-readable weird-text encoder/decoder.

For each original word in the original text, it leaves the first and last character of it in that
position, but shuffles (permutates) all the characters in the middle of the word. If possible,
the resulting “encoded” word is different than the original word.

Words shorter than 4 characters or with double letters inside - like: "keep", 
"seen", "moon"  cannot be scrambled - because swapping its characters has no effect.

#### Key features: 
- simple, straight-forward
- 100% translatable - back and fourth
- codec is lossless and doesn't need any additional data for translation 
- scrambles all numbers and slugs as well
- keeps other non-word text parts unchanged

Scrambling order is pseudo-random and different for each word.

### Usage
```python
import dizzer

original_text = """
Text can contain unlimited number of whitespaces, newlines etc.
Numbers like 12345, 1234567, 987654321 or 123456789 are also scrambled.
"""
encoded = dizzer.encode(original_text)

print(encoded)

# Txet can cnitaon umnitelid nmeubr of wtsehaecips, newniels etc.
# Numbres lkie 14325, 1346257, 967843251 or 143267859 are aslo scrmeabld.

# reverse operation:
decoded = dizzer.decode(encoded)

print(decoded)

# Text can contain unlimited number of whitespaces, newlines etc.
# Numbers like 12345, 1234567, 987654321 or 123456789 are also scrambled. 

```

### Installation
```bash
pip install dizzer
```
It has no dependencies and works in python 3.7, 3.8, 3.9 and pypy3.


### Interoperability check
There is non-zero probability, that the algorithm works 
different on sophisticated environments (i.e. when your python interpreter 
uses weird pseudo-random generator library).

At import time of `dizzer` package there is a self-check statement. 
It checks if this algorithm works in your environment. 
There is a snippet that raises an import error if a malfunction is detected.
In other words - if you are able to import dizzer - you can be sure, that your 
encoded text can be decoded on othr machines.

#### The self-check statement

```python
import dizzer


PROPER_TEXT = """
This sentence approves that dizzer can be used on your machine.
If this assertion is not raised - it means you can read and write messages
that are fully translatable on other machines.
"""

EXPECTED_ENCODING = """
Tihs senectne aepvorps taht dzzier can be uesd on yuor mhcaine.
If tihs aosirtsen is not risaed - it mneas you can raed and wtrie msesgeas
taht are fluly tbnslalatrae on oethr mhacneis.
"""

local_encoding = dizzer.encode(PROPER_TEXT)
back = dizzer.decode(local_encoding)

assert local_encoding == EXPECTED_ENCODING, "Failed to encode."
assert back == PROPER_TEXT, "Failed to decode."

```
