### DIZZER
Bidirectional human-readable weird-text encoder.

[![PyPI version](https://img.shields.io/pypi/v/dizzer.svg)](https://pypi.python.org/pypi/dizzer/)
[![pipeline status](https://gitlab.com/kamichal/dizzer/badges/master/pipeline.svg)](https://gitlab.com/kamichal/dizzer/-/commits/master)
[![coverage report](https://gitlab.com/kamichal/dizzer/badges/master/coverage.svg)](https://gitlab.com/kamichal/dizzer/-/commits/master)
[![PyPI pyversion](https://img.shields.io/pypi/pyversions/AIRIUM.svg)](https://pypi.org/project/dizzer/)
[![PyPI license](https://img.shields.io/pypi/l/AIRIUM.svg)](https://pypi.python.org/pypi/dizzer/)
[![PyPI status](https://img.shields.io/pypi/status/AIRIUM.svg)](https://pypi.python.org/pypi/dizzer/)


Key features: 
- simple, straight-forward
- equipped with decoder

### Installation
```bash
pip install dizzer
```

### Example
```python
PROPER_TEXT = """
This sentence approves that dizzer can be used on your machine.
If this assertion is not raised - it means you can read and write messages
that are fully translatable on other machines.
"""
import dizzer

local_encoding = dizzer.encode(PROPER_TEXT)

EXPECTED_ENCODING = """
Tihs senectne aepvorps taht dzzier can be uesd on yuor mhcaine.
If tihs aosirtsen is not risaed - it mneas you can raed and wtrie msesgeas
taht are fluly tbnslalatrae on oethr mhacneis.
"""

assert local_encoding == EXPECTED_ENCODING

back = dizzer.decode(local_encoding)
assert back == PROPER_TEXT

```
