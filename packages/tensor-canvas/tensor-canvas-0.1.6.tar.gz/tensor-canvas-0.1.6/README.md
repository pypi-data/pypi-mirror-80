.. image:: https://badge.fury.io/py/eagerpy.svg
   :target: https://badge.fury.io/py/eagerpy

# Tensor Canvas 🎨
----------------
A 2D graphics library for drawing directly onto tensors.  
Uses [eagerpy](https://github.com/jonasrauber/eagerpy) to support a uniform API for pytorch, tensorflow, jax, and numpy backends.
Tensor Canvas uses SDF representations for easy implementation in gpu-accelerated frameworks.  
Highly inefficient compared to standard gpu rendering, but much better than matplotlib. Integration with ML frameworks also means it is fully-differentiable.

### Example
```python
import tensorcanvas as tc
import torch
import tensorflow as tf
import numpy as np



```

### Notebook Example