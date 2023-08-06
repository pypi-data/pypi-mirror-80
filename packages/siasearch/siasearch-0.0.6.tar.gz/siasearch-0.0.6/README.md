# SiaSearch API SDK 

# How to use it?
As an example, this is how you would use the API to query for the velocity of a KITTI drive during a lane change:

```python
from siasearch import auth

sia = auth("user@example.com", "password", "https://kitti.merantix.de")
results = sia.query("dataset_name = 'kitti' AND is_lane_change = 'True'")
segments = results.segments
velocity_level = segments[0].get_metadata("velocity_level")
```

## Documentation generation
To generate simple Sphinx documentation you need to install Sphinx package  
```bash
 pip install -U Sphinx
 pip install sphinx-rtd-theme
```
and run: 
```bash
sphinx-build -b html docs/source docs/build
```
from the package root folder.  
And you would get build html documentation in `docs/build` folder.  
You can serve it running `python -m http.server` from `docs/build` folder.  
