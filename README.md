# An analysis of electricity production and consumption in the Orkney Islands, especially with respect to curtailment due to excessive generation.

**Stuart Rendall**  
University of the Highlands and Islands  
_MSc Web Techologies research project_    
October 2019

## Summary

A live data feed of the current electricity demand and generation in the Orkney Isles is published by Southern Scottish Electricity Network. https://www.ssen.co.uk/ANM/

When generation is likely to exceed the capacity of the transmission network, some generators are shut down to ensure network safety.  This is known as curtailment and is controlled by the local electricity network operator SSEN using a system named ANM (Active Network Management), also known as a 'smart grid'. A live feed refecting the current state of the network is also published. https://www.ssen.co.uk/ANMGeneration/

Logging these data feeds will provide a useful resource for future analysis. Methods of doing this are described here.

It is intended that by combining this data with archived weather records we can gain some insight into the into the systems involved and create a computer model that will be able to forecast electricity usage, generation and curtailment events.

A system to log these data streams has been creaeted and implemented, along with methods to record weather data from the met office data point service - further details can be found [here](logging/readme.md).

The electricity and ANM logs have been checked and duplicates removed [[1](../dataclean/ExamineElectricityReadings.ipynb), [2](../dataclean/ExamineANMReadings.ipynb)] and then combined [[3](../dataclean/combine_datasets.ipynb)].

Some analysis of the logged data has also been performed [[4](../loganalysis/ElecandANManalysis.ipynb)].

Two external web resources have been identified that can provide information relevant to this investigation: Weather records and generation data from a domestic wind turbine.  Further details [here](retrieval/readme.md).

## Other information

### sqlite
sqlite has been used to store the data in an SQL data format and perform simple queries on the data.  It is simple to install and easy to use within python scripts and Jupyter lab. 

### Jupyter Lab
Jupyter Lab has been used throughout this project as an analysis and documentation tool. This repository is the result.

### Github

Github does not support large files.  As such, the large data files (database .db, comma separated variable .csv and sql dumps) have been omitted from this repository using relevant entries in the `.gitignore` file.

The logged sqlite data files used can be found here:
* Electricity log: [eleclog.db](https://comp-server.uhi.ac.uk/~14021635/ssen/finaldataset/eleclog.db)
* ANM log: [ANMstatus.db](https://comp-server.uhi.ac.uk/~14021635/ssen/finaldataset/ANMstatus.db)

all other files can be created using the methods in this repository


## Other documents
* [Research Proposal](docs/proposal.md)