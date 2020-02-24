# Online archive data retrieval

Two external web resources have been identified that can provide information relevant to this investigation.

## Wind turbine records

Orkney Renewable Energy Forum ([OREF](http://www.oref.co.uk/)) have a domestic wind turbine that logs its output to a public website:  
https://www.sunnyportal.com/Templates/PublicPageOverview.aspx?plant=7c8677c0-4e37-42d6-a115-d356f13a3120

A python script `quarryhouse.py` has been written that sytematically accesses the webpage view of each month's readings and logs it to an sqlite3 database.
Explanation of the data structure and the methods used to retrieve the information are described in the Jupyter notebook - [Quarryhouse.ipynb](./Quarryhouse.ipynb)

## Historical weather records

[weatherhq](https://www.weatherhq.co.uk/weather-station/kirkwall-airport)([Vackertvader](https://www.vackertvader.se/v%C3%A4derstation/kirkwall-airport)) logs Met Office readings for many sites including Kirkwall Airport (site_id= 3017), at a higher resolution and with a larger free archive than supplied by the Met Office directly in their observations service ([DataPoint API](https://www.metoffice.gov.uk/datapoint/product/uk-hourly-site-specific-observations/detailed-documentation)), which only provides hourly observations for the last 24 hours.

Initially, a python script `vackerWeather.py` was written to retrieve historical readings from Weatherhq and log it to an sqlite3 database.  

Subsequently, a Jupyter notebook [VackerWeatherLog.ipynb](./VackerWeatherLog.ipynb) detailing the methods involved and the associated problems to be overcome to produce the complete set of data required.

The weather records retrieved from the Vackertvader web service proved not to have been recorded at uniform time intervals.  Thus the data has been interpolated (additional datapoints added between the actual records) to correct this. [InterpolateWeatherData.ipynb](./InterpolateWeatherData.ipynb)
