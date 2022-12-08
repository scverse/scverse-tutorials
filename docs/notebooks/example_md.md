---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.2
kernelspec:
  display_name: Python 3.6.8 64-bit
  language: python
  name: python3
---

+++ {"pycharm": {"name": "#%% md\n"}}

# Example notebook

```{code-cell} ipython3
---
pycharm:
  name: '#%%

    '
---
import numpy as np
from anndata import AnnData
import scverse_doc
```

```{code-cell} ipython3
---
pycharm:
  name: '#%%

    '
---
adata = AnnData(np.random.normal(size=(20, 10)))
```

```{code-cell} ipython3
---
pycharm:
  name: '#%%

    '
---
scverse_doc.pp.basic_preproc(adata)
```
