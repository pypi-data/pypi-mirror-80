# IntrinsicAnalysis

IntrinsicAnalysis is a Python library for intrinsic analysis within one document for Armenian texts.
It uses stylometric features analysis to find suspicious fragments.
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install IntrinsicAnalysis.

```bash
pip install IntrinsicAnalysis
```

## Usage
To use library import _analyse_paragraphs_ as follows:
```python
from IntrinsicAnalysis.analyse import analyse_paragraphs
```
As input _analyse_paragraphs_ takes list of strings(paragraphs) of entire document and returns suspicious paragraphs.
```python
analyse_paragraphs(paragraphs)
```

## License
[MIT](https://choosealicense.com/licenses/mit/)