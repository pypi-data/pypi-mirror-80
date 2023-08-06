# nvcl_kit: A simple module used to read Australian NVCL borehole data

[![pipeline status](https://gitlab.com/csiro-geoanalytics/python-shared/nvcl_kit/badges/master/pipeline.svg)](https://gitlab.com/csiro-geoanalytics/python-shared/nvcl_kit/commits/master)
[![coverage report](https://gitlab.com/csiro-geoanalytics/python-shared/nvcl_kit/badges/master/coverage.svg)](https://gitlab.com/csiro-geoanalytics/python-shared/nvcl_kit/commits/master)


1. **An introduction is below**
2. **There is a rough demonstration script [here](https://gitlab.com/csiro-geoanalytics/python-shared/nvcl_kit/-/blob/master/demo.py)**
3. **API documentation can be found [here](https://csiro-geoanalytics.gitlab.io/python-shared/nvcl_kit)**

## How to extract NVCL borehole data

**1. Instantiate class**

```python
from nvcl_kit.reader import NVCLReader 
from types import SimpleNamespace
param = SimpleNamespace()

# URL of the GeoSciML v4.1 BoreHoleView Web Feature Service
param.WFS_URL = "http://blah.blah.blah/nvcl/geoserver/wfs"

# URL of NVCL service
param.NVCL_URL = "https://blah.blah.blah/nvcl/NVCLDataServices"

# Optional bounding box to search for boreholes using WFS, default units are EPSG:4326 degrees
param.BBOX = {"west": 132.76, "south": -28.44, "east": 134.39, "north": -26.87 }

# Optional maximum number of boreholes to fetch, default is no limit
param.MAX_BOREHOLES = 20

# Instantiate class and search for boreholes
reader = NVCLReader(param)
```

**2. Check if 'wfs' is not 'None' to see if this instance initialised properly**

```python
if not reader.wfs:
    print("ERROR!")
```

**3. Call get_boreholes_list() to get list of WFS borehole data for NVCL boreholes**

```python
# Returns a list of python dictionaries
# Each dict has fields from GeoSciML v4.1 BoreholeView
bh_list = reader.get_boreholes_list()
```

**4. Call get_nvcl_id_list() to get a list of NVCL borehole ids**

```python
nvcl_id_list = reader.get_nvcl_id_list()
```

**5. Using an NVCL borehole id from previous step, call get_imagelog_data()
     to get the NVCL log ids**

```python
# Get list of NVCL log ids
nvcl_id_list = reader.get_nvcl_id_list()

# Get NVCL log id for first borehole in list
nvcl_id = nvcl_id_list[0]

# Get image log data for first borehole
imagelog_data_list = reader.get_imagelog_data(nvcl_id)
for ild in imagelog_data_list:
    print(ild.log_id,
          ild.log_name,
          ild.log_type,
          ild.algorithmout_id)
```

**6. Using image log data, call get_borehole_data() to get borehole data**

```python
# Analysis class has 2 parts:
# 1. Min1,2,3 = 1st, 2nd, 3rd most common mineral
#    OR Grp1,2,3 = 1st, 2nd, 3rd most common group of minerals
# 2. uTSAV = visible light, uTSAS = shortwave IR, uTSAT = thermal IR
#
# These combine to give us a class name such as 'Grp1 uTSAS'
#
# Here we extract data for log type '1' and 'Grp1 uTSAS'
HEIGHT_RESOLUTION = 20.0
ANALYSIS_CLASS = 'Grp1 uTSAS'
LOG_TYPE = '1'
for ild in imagelog_data_list:
    if ild.log_type == LOG_TYPE and ild.log_name == ANALYSIS_CLASS:
        bh_data = reader.get_borehole_data(ild.log_id, HEIGHT_RESOLUTION, ANALYSIS_CLASS)
        # Print out the colour, mineral and class name at each depth
        for depth in bh_data:
            print("At ", depth, "my class, mineral, colour is", bh_data[depth].className,
                  bh_data[depth].classText, bh_data[depth].colour)
```

**7. Using the NVCL ids from Step 5, you can also call get_spectrallog_data() and get_profilometer_data()**

```python
spectrallog_data_list = reader.get_spectrallog_data(nvcl_id)
for sld in spectrallog_data_list:
    print(sld.log_id,
          sld.log_name,
          sld.wavelength_units,
          sld.sample_count,
          sld.script,
          sld.script_raw,
          sld.wavelengths)

profilometer_data_list = reader.get_profilometer_data(nvcl_id)
for pdl in profilometer_data_list:
    print(pdl.log_id,
          pdl.log_name,
          pdl.max_val,
          pdl.min_val,
          pdl.floats_per_sample,
          pdl.sample_count)
```

**8. Option: get a list of dataset ids**

```python
datasetid_list = reader.get_datasetid_list(nvcl_id)
```

**9. Option: Get a list of datasets**

```python
dataset_list = reader.get_dataset_list(nvcl_id)
for ds in dataset_list:
    print(ds.dataset_id,
          ds.dataset_name,
          ds.borehole_uri,
          ds.tray_id,
          ds.section_id,
          ds.domain_id)
```


**10. Using an element from 'datasetid_list' in Step 8 or 'ds.dataset_id' from Step 9, can retrieve log data**

``` python
# Scalar log data
log_list = reader.get_scalar_logs(ds.dataset_id)
for log in log_list:
    print(log.log_id,
          log.log_name,
          log.is_public,
          log.log_type,
          log.algorithm_id)
```


``` python
# Different types of image log data
ilog_list = reader.get_all_imglogs(ds.dataset_id)
ilog_list = reader.get_mosaic_imglogs(ds.dataset_id)
ilog_list = reader.get_tray_thumb_imglogs(ds.dataset_id)
ilog_list = reader.get_tray_imglogs(ds.dataset_id)
ilog_list = reader.get_imagery_imglogs(ds.dataset_id)

for ilog in ilog_list:
    print(ilog.log_id,
          ilog.log_name,
          ilog.sample_count)
```


**11. Using the scalar log ids, can get scalar data and plots of scalar data**

```python
# Scalar data in CSV format
log_id_list = [l.log_id for l in log_list]
data = reader.get_scalar_data(log_id_list)

# Sampled scalar data in JSON (or CSV) format
samples = reader.get_sampled_scalar_data(log.log_id,
                                         outputformat='json',
                                         startdepth=0,
                                         enddepth=2000,
                                         interval=100)

# A data plot in PNG
plot_data = reader.plot_scalar_png(log_id)

# Data plots in HTML, only plots the first 6 log ids
plot_data = reader.plot_scalars_html(log_id_list)

```


**12. Using the image log ids can produce images of NVCL cores**

```python
ilog_list = reader.get_mosaic_imglogs(ds.dataset_id)
for ilog in ilog_list:
    img = reader.get_mosaic_image(ilog.log_id)

ilog_list = reader.get_tray_thumb_imglogs(ds.dataset_id)
for ilog in ilog_list:
    # Either HTML or JPG
    img = reader.get_tray_thumb_html(ds.dataset_id, ilog.log_id)
    img = reader.get_tray_thumb_jpg(ilog.log_id)

# Use either 'get_tray_thumb_imglogs()' or 'get_tray_imglogs()'
ilog_list = reader.get_tray_thumb_imglogs(ds.dataset_id)
ilog_list = reader.get_tray_imglogs(ds.dataset_id)
for ilog in ilog_list:
    depth_list = reader.get_tray_depths(ilog.log_id)
    for depth in depth_list:
        print(depth.sample_no,
              depth.start_value,
              depth.end_value)

```
