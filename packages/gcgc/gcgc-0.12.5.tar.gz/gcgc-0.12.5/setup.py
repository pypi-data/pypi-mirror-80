# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcgc',
 'gcgc.data',
 'gcgc.tests',
 'gcgc.tests.fixtures',
 'gcgc.tests.tokenizer',
 'gcgc.tests.vocab',
 'gcgc.tokenizer']

package_data = \
{'': ['*'],
 'gcgc.data': ['splice/*'],
 'gcgc.tests.fixtures': ['PF12057/*',
                         'ecoli/*',
                         'globin_alignment/*',
                         'p53_human/*']}

install_requires = \
['pydantic>=1,<2']

extras_require = \
{'third_party': ['biopython>=1.78', 'transformers>=3', 'torch>=1.6']}

setup_kwargs = {
    'name': 'gcgc',
    'version': '0.12.5',
    'description': 'GCGC is a preprocessing library for biological sequence model development.',
    'long_description': '# GCGC\n\n> GCGC is a tool for feature processing on Biological Sequences.\n\n[![](https://github.com/tshauck/gcgc/workflows/Run%20Tests%20and%20Lint/badge.svg)](https://github.com/tshauck/gcgc/actions?query=workflow%3A%22Run+Tests+and+Lint%22)\n[![](https://img.shields.io/pypi/v/gcgc.svg)](https://pypi.python.org/pypi/gcgc)\n[![code style black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n## Installation\n\nGCGC is primarily intended to be used as part of a larger workflow inside\nPython.\n\nTo install via pip:\n\n```sh\n$ pip install gcgc\n```\n\nIf you\'d like to use code that helps gcgc\'s tokenizers integrate with common\nthird party libraries, either install those packages separately, or use gcgc\'s\nextras.\n\n```sh\n$ pip install \'gcgc[third_party]\'\n```\n\n## Documentation\n\nThe GCGC documentation is at [gcgc.trenthauck.com](http://gcgc.trenthauck.com),\nplease see it for examples.\n\n### Quick Start\n\nThe easiest way to get started is to import the kmer tokenizer, configure it,\nthen start tokenizing.\n\n```python\nfrom gcgc import KmerTokenizer\n\nkmer_tokenizer = KmerTokenizer(alphabet="unambiguous_dna")\nencoded = kmer_tokenizer.encode("ATCG")\nprint(encoded)\n```\n\nsample output:\n\n```\n[1, 6, 7, 8, 5, 2]\n```\n\nThis output includes the "bos" token, the "eos" token, and the three amino acid\ntokens in between.\n\nYou can go the other way and convert the integers to strings.\n\n```python\nfrom gcgc import KmerTokenizer\n\nkmer_tokenizer = KmerTokenizer(alphabet="unambiguous_dna")\ndecoded = kmer_tokenizer.decode(kmer_tokenizer.encode("ATCG"))\nprint(decoded)\n```\n\nsample output:\n\n```\n[\'>\', \'A\', \'T\', \'C\', \'G\', \'<\']\n```\n\nThere\'s also the vocab for the kmer tokenizer.\n\n```python\nfrom gcgc import KmerTokenizer\n\nkmer_tokenizer = KmerTokenizer(alphabet="unambiguous_dna")\nprint(kmer_tokenizer.vocab.stoi)\n```\n\nsample output:\n\n```\n{\'|\': 0, \'>\': 1, \'<\': 2, \'#\': 3, \'?\': 4, \'G\': 5, \'A\': 6, \'T\': 7, \'C\': 8}\n```\n\n### Transformers\n\nThe [Transformers](https://huggingface.co/transformers/) library has an\nidea of a tokenizer that is used for various modeling tasks.\n\nTo make it easier to use the Transformers library on biological sequences, gcgc\nhas a Transformers compatible tokenizer that can be created from the\nKmerTokenizer.\n\n```python\nfrom gcgc import KmerTokenizer\nfrom gcgc import third_party\n\nkmer_tokenizer = KmerTokenizer(\n  kmer_length=2, kmer_stride=2, alphabet="unambiguous_dna"\n)\n\ntt = third_party.GCGCTransformersTokenizer.from_kmer_tokenizer(\n    kmer_tokenizer\n)\n\nbatch = tt.batch_encode_plus(["ATGC", "GCGC"])\nprint(batch["input_ids"])\n```\n\nsample output:\n\n```\n[[1, 11, 8, 2], [1, 8, 8, 2]]\n```\n',
    'author': 'Trent Hauck',
    'author_email': 'trent@trenthauck.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://gcgc.trenthauck.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
