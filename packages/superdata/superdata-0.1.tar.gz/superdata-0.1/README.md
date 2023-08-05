# SuperData

A small python SUPERpackage to import common DATA science packages to the namespace.
That is, no need to `import numpy as np` in your code.

For example:
```
1 from superdata import *
2 a=np.array([1,2,3])
3 plt.plot(a)
```
For now, only covers:
```
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
```

## installation

Easy installation using pip: https://pypi.org/project/superdata/0.1/
