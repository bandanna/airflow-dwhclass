# docker-airflow
[![CI status](https://github.com/puckel/docker-airflow/workflows/CI/badge.svg?branch=master)](https://github.com/puckel/docker-airflow/actions?query=workflow%3ACI+branch%3Amaster+event%3Apush)
[![Docker Build status](https://img.shields.io/docker/build/puckel/docker-airflow?style=plastic)](https://hub.docker.com/r/puckel/docker-airflow/tags?ordering=last_updated)

[![Docker Hub](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com/r/puckel/docker-airflow/)
[![Docker Pulls](https://img.shields.io/docker/pulls/puckel/docker-airflow.svg)]()
[![Docker Stars](https://img.shields.io/docker/stars/puckel/docker-airflow.svg)]()

This repository contains **Dockerfile** of [apache-airflow](https://github.com/apache/incubator-airflow) for [Docker](https://www.docker.com/)'s [automated build](https://registry.hub.docker.com/u/puckel/docker-airflow/) published to the public [Docker Hub Registry](https://registry.hub.docker.com/).


## Usage

By default, docker-airflow runs Airflow with **SequentialExecutor** :

    docker run -d -p 8080:8080 puckel/docker-airflow webserver

If you want to run another executor, use the other docker-compose.yml files provided in this repository.

For **LocalExecutor** :

    docker-compose -f docker-compose-LocalExecutor.yml up -d


NB : If you want to have DAGs example loaded (default=False), you've to set the following environment variable :

`LOAD_EX=n`

    docker run -d -p 8080:8080 -e LOAD_EX=y puckel/docker-airflow

If you want to use Ad hoc query, make sure you've configured connections:
Go to Admin -> Connections and Edit "postgres_default" set this values (equivalent to values in airflow.cfg/docker-compose*.yml) :
- Host : postgres
- Schema : airflow
- Login : airflow
- Password : airflow

## Install custom python package

- Create a file "requirements.txt" with the desired python modules
- Mount this file as a volume `-v $(pwd)/requirements.txt:/requirements.txt` (or add it as a volume in docker-compose file)
- The entrypoint.sh script execute the pip install command (with --user option)

## UI Links

- Airflow: [localhost:8080](http://localhost:8080/)
- Flower: [localhost:5555](http://localhost:5555/)

## Work with PostgresDB
Once the `LocalExecutor` docker-compose is running, you could could to your PostgresDB instance using tools like DBeaver, etc. 

The connections credentials are:

```
Host: localhost
Port: <CHECK THE NOTE BELOW>
Database: mydb
User: mydb
Password: mydb
```

**Note**: If you loading the database from inside Airflow then the port is `5432`, but if you are loading it from your `localhost` (your computer) then it's `5439`.

Any files added to the folder `/pg_data/` can be seen and accessed by Postgres. 

For example, let's create a table:
```
CREATE TABLE pet (name VARCHAR(20), owner VARCHAR(20),
       species VARCHAR(20), sex CHAR(1), birth DATE, death DATE);
```

Now, let's insert the data from `pg_data/test.csv`
```
copy pet FROM '/var/lib/postgresql/data/test.csv' DELIMITER ',' CSV;
```

Remmber, if the CSV had head, it'd have been with `HEADER` as of:
```
copy pet FROM '/pg_data/test.csv' DELIMITER ',' HEADER CSV;
```

Check it out
```
select * 
from pet;
```


## Work with Mysql

Once the `LocalExecutor` docker-compose is running, you could could to your mysql DB instance using tools like DBeaver or MySQL Workbench. The parameters are as follows:

```
Host: 127.0.0.1
Port: 3306
Database: db
User: root
Password: password
```

Any files added to the folder `/imported_data/` can be seen and accessed by Mysql. 

Example:

Creating table 

```
CREATE TABLE pet (name VARCHAR(20), owner VARCHAR(20),
       species VARCHAR(20), sex CHAR(1), birth DATE, death DATE);
```

Insert values

```
INSERT INTO `pet`(name,owner,species,sex,birth,death) VALUES ("dog","me","boo","M",'2019-01-01','2019-01-30');

```

load the values from an example file `/imported_data/test.csv`

```
LOAD DATA INFILE  
'/imported_data/test.csv'
INTO TABLE db.pet  
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(name,owner,species,sex,birth,death);
```


check the data (same row once manually and once from the file)

```
 select *
 from db.pet; 
```

**Important Note** : if you want your data to be saved and transferred once working with others on the same project, make sure to uncommenct the `data` folder part from `.gitignore`

-------

## DWH Class Exercise

The slides from the class are available here:
https://docs.google.com/presentation/d/1bhj3weU4ZrwaCkbcQvmL-WwrrMmN2HQzgXpSuIbA_YU/edit?usp=sharing

Airflow recognizes all DAGs and binaries using a home folder `$AIRFLOW_HOME`. In our case this folder is `dags`. Thus, everything included in that folder is visible and accessible to Airflow.

The files which start with `dag_..` are example pipelines. Please browse them to understand the structure more. The most important file for this exercise is `dag_dwh_class_example.py`. This file includes example Operators of which we'd need in this tutorial (DummyOperator, PythonOperator, PostgresOperator)

Before starting, make sure to get your cluster up and running, use the following command:

```
docker-compose -f docker-compose-LocalExecutor.yml up -d
```

Check `docker ps` and in your web browser `localhost:8080` that Airflow is up and running.

As for the tasks:
1. Create a connection called `mydb` in Airflow. For that check (work with PostgresDB) [the section above](#work-with-postgresdb)
2. Create cron schedule to run once a day at 9AM
    - You may use https://crontab-generator.org for that
3. The exercise will be performed fully in `dag_dwh_solution.py`, in which the dependencies and some helpful hints are already filled.
4. Create your dag configuration, call it `etl_dwh_class` (not the filename, but the dag name)
5. Create a dag object with the name and the cron schedule from the second step.
6. Make sure to set your starting date for November 29, 2019.
7. Create 2 DummyOperators, one call it `start` and another call it `end`. Connect them in a way that `start`->`end`.
    - save the file and refresh, make sure it appears in the UI   
8. Create a PostgresOperator called `create_tables` that runs the tables creation in the `create_tables.sql`. Use the helping lines in the file.
    - Now convert your pipeline to be start->create_table->end
    - Double check in the UI (be patient it could take sometime to update)
9. Create a PythonOperator called `load_employees_and_orders` that runs the `load_data` function which is already imported in `dag_dwh_solution.py`.
    - Add this Operator between create_tables and end.
10. Create PostgresOperator called `load_products`. This Operator should run right after the one from the previous step and before `end`. Oh, and the query which loads the Products data is below. Please, rely on the given examples and plug it into PostgresOperator:
```
copy products from '/pg_data/products.csv' DELIMITER ',' header CSV;
```
11. Make `load_employees_and_orders` and `load_products` parallel instead of sequential. 


