# clickgetcoords
Simple coordinate acquisition tool.
So simple that you can easily costomize as you want.

# Requirements
You need to install Pillow library.
```
pip install Pillow
```

# Usage
1. Save image files to figs.
1. `python clickgetcoords.py`
1. calibrated coordinates (maybe what you want) and original coordinates (in Display coordinate) will be saved to 'data' dir.
1. You can read saved data by `points=np.loadtxt(filepath, delimiter=' ')`.


# To be imporved...
- add exception handling.
- rearrange the input/output folder.
- add GUI(?)