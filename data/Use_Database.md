Technical Guide: Open Data for Storms Database

1. Purpose

This document provides guidance for filling the storm monitoring database with real, open-source data. It covers each table, required columns, data sources, and usage notes.


---

2. Tables Overview

2.1 storms (Storms)

Column	Description	Open Source Data

storm_id	Unique storm identifier	IBTrACS
name	Storm name	IBTrACS
basin	Ocean basin (atlantic, pacific, indian, southern)	IBTrACS
latitude	Storm center latitude	IBTrACS
longitude	Storm center longitude	IBTrACS
wind_speed_kt	Maximum sustained wind in knots	NHC / JTWC / IBTrACS
pressure_mb	Central pressure in millibars	NHC / JTWC / IBTrACS
category	Saffir-Simpson hurricane scale	Derived from wind_speed_kt
status	Storm status (active/dissipated/warning)	NHC / JTWC / CPHC
source	Data source	NOAA, NHC, JTWC
forecast_center	Responsible forecast center	NHC / JTWC / CPHC
last_update	Last update timestamp	From source reports



---

2.2 parameters (Environmental Parameters)

Column	Description	Open Source Data

storm_id	FK to storms	IBTrACS
timestamp	Data timestamp	Source report time
ocean_heat_content	Upper ocean heat content (kJ/cm²)	NOAA OHC
vertical_wind_shear	200-850 hPa wind shear (kt)	NCEP Reanalysis
mid_level_humidity	Relative humidity 500 hPa (%)	ERA5 / ECMWF
eyewall_symmetry	Eyewall symmetry index (0-1)	Calculated from satellite imagery
convective_organization	Convective organization (0-1)	Calculated from satellite imagery
outflow_efficiency	Outflow efficiency (0-1)	Derived from satellite or model
intensity_trend	Trend in intensity (kt/6h)	Calculated from consecutive observations
ri_probability	Rapid Intensification probability (%)	Computed from above parameters



---

2.3 forecasts (Forecasts)

Column	Description	Open Source Data

storm_id	FK to storms	IBTrACS
forecast_time	Forecast timestamp	Source report
forecast_horizon	Hours ahead	NHC / JTWC
forecast_intensity	Expected wind speed (kt)	NHC / JTWC
forecast_probability	Likelihood of event	NHC / JTWC
model_version	Forecast model name	VORTEX-v1.0 or external models
parameters	JSON of forecasted indicators	Optional computed values



---

2.4 reports (Reports)

Column	Description	Open Source Data

report_id	Unique report ID	Auto-generated
storm_id	FK to storms	IBTrACS
report_type	daily / analysis / alert / forecast	NHC / JTWC / CPHC
content	Textual report	NHC / JTWC / CPHC
summary	JSON summary of key indicators	e.g., {"ri_probability": 78}
file_path	File path to report	Optional
generated_at	Timestamp	Report creation time



---

3. Data Sources

IBTrACS: Global tropical cyclone tracks (storm ID, name, basin, coordinates, wind, pressure, category).

NOAA OHC: Ocean heat content data.

NCEP Reanalysis: Atmospheric parameters (wind shear, humidity).

ERA5 / ECMWF: Mid-level humidity and environmental data.

NHC / JTWC / CPHC: Official advisories, forecasts, reports.



---

4. Notes for Technical Team

1. Ensure FK constraints: parameters.storm_id and reports.storm_id must exist in storms.


2. Use unique identifiers for storm_id and report_id.


3. Timestamps should reflect the original observation time.


4. For rapid intensification (ri_probability) calculations, combine environmental indices as per the model.


5. Data can be ingested in batch mode using CSV or automated ETL scripts from the above sources.




---

5. Recommended Workflow

1. Fetch storms from IBTrACS → populate storms.


2. Fetch environmental data → populate parameters.


3. Generate forecasts → populate forecasts.


4. Generate reports → populate reports.


5. Validate FK constraints and uniqueness.




---

6. References

IBTrACS Database

NOAA Ocean Heat Content

NCEP Reanalysis

ERA5 / ECMWF Climate Data

NHC Tropical Cyclone Advisories
