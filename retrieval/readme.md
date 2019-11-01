# Online archive data retrieval


## Wind turbine records

Orkney Renewable Energy Forum ([OREF](http://www.oref.co.uk/)) have a domestic wind turbine that logs its output to a public website:  
https://www.sunnyportal.com/Templates/PublicPageOverview.aspx?plant=7c8677c0-4e37-42d6-a115-d356f13a3120

`quarryhouse.py` - A python script that systematically accesses the webpage view of each month's readings and logs it to an sqlite3 database.

## Historical weather records

[weatherhq](https://www.weatherhq.co.uk/weather-station/kirkwall-airport) logs Met Office readings for many sites including Kirkwall Airport (site_id= 3017), at a higher resolution and with a larger free archive than supplied by the Met Office directly in their observations service ([DataPoint API](https://www.metoffice.gov.uk/datapoint/product/uk-hourly-site-specific-observations/detailed-documentation)), which only provides hourly observations for the last 24 hours.

`vackerWeather.py` - a python script that retrieves historical readings from Weatherhq and logs it to an sqlite3 database.