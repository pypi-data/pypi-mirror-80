![PyPI status](https://img.shields.io/pypi/status/livelossplot.svg)
![MIT license - PyPI](https://img.shields.io/pypi/l/livelossplot.svg)
![Python version - PyPI](https://img.shields.io/pypi/pyversions/livelossplot.svg)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/stared/livelossplot/Python%20package)](https://github.com/stared/livelossplot/actions)

## Installation
```bash
pip install realtimeplt
```
realtimeplt is a Python library made by VisionBrain which foucuses on getting the Live training loss plot in Jupyter Notebook for Keras, PyTorch and TensorFlow.Our main objective is to bring the ability to  visualize the data hyperparameters in real time.


## Most Noticeable changes:
-Runs on the latest version of python
-Runs on the latest version of keras
-Runs on the latest version of pytorch
-Runs on the latest version of tensorflow



## Use 
The major dependency of realtimeplt is livelossplot
```python
from livelossplot import PlotLossesKeras
model.fit(X_train, Y_train,
          epochs=10,
          validation_data=(X_test, Y_test),
          callbacks=[PlotLossesKeras()],
          verbose=0)
```

## Supported DataScience Libraries
Note*** Better results when used with Jupyter Notebook.

- Matplotlib
- Seaborn
- SciPy
- Bokeh

## Created by [Lead Developer ](https://aryan05.github.io/) & the VisionBrain team, MNNIT Allahabad. Thanks for using our library. 

## Note*** realtimeplt is a faster and accurate version of [liveplot](https://github.com/PhilReinhold/liveplot) & in no manner VisionBrain is trying to coppy liveplot.




