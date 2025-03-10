# GridSnek :snake:
This repository is a for a simple API that helps checking network coverage with each available provider at a geographical location.

## Endpoints
GridSnek in total has a whopping 2 endpoints :clap:

/coverage
----------
```http
GET /coverage?q=<some_address>
Host: http://localhost:5000
```
It accepts the following query parameters:
1. q &rarr; Which should be an address
2. lon &rarr; A Longitude point 
3. lat &rarr; A Latitude point 

If you wish to get coverage information using GPS(lon, lat) points you have to provide both otherwise no coverage data could be returned.

Using address is superior to GPS points!

The endpoint will return a dictionary of providers and their available services at the given geographical point:
```json
{
	"orange": {"2G": true, "3G": true, "4G": false}, 
	"SFR": {"2G": true, "3G": true, "4G": true}
}
```

/apidocs
--------
By accessing the /apidocs endpoint from a browser a Swagger API docs ui will provide some details about the available
endpoints and the API could be tried out from there.

## Setup and Run
GridSnek is a dockerized Flask application served by Gunicorn for a modern and comfortable experience.
Data is stored in a Relational Database (in this case mysql). The database runs in a separate docker container and
spins up before the application.

To run the application all you need is Docker (Guide can be found here: [Docker Guide](https://www.docker.com/get-started/))

The following command works in any linux terminal (docker compose v2 is available, essentially any system that runs up to date docker) .

Standing in the root folder of the application:
```shell
docker compose up
```
This will build and run the application.

The application is available at the following address: 
```http
http://localhost:5000
```

### Configuration
Configuration can be done by editing the docker-compose.yml

Commenting the following line will not populate the database upon first startup with data from csv file found in static folder.
```yaml
      - ./static/db_init:/docker-entrypoint-initdb.d/ # Initialize DB with already processed data
```

By setting the following environment variable to True the startup script will process and import csv files to populate the database with provider and coverage data.
```yaml
      - LOAD_CSV_DATA=False # Set this to False if it is not the first startup or the database was already populated
```
The initial data(coverage, providers) csv files can be overwritten by attaching new csv files to the container and setting
the following environment variables with their incontainer path's. Note that their format has to match the original format!
```yaml
#      in case new data was attached to the container in volumes(but it has to match the format of the base csv files as these are bound to a Model)
      - CSV_COVERAGE_DATA_PATH=<some_in_container_path>
      - CSV_PROVIDERS_DATA_PATH=<some_in_container_path>
```
Changing the following variable will change the amount of records to be inserted at once during csv processing.
```yaml
      - DB_INSERT_BATCH_SIZE=100
```