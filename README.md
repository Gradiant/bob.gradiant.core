# bob.gradiant.core  [![Build Status](https://travis-ci.org/Gradiant/bob.gradiant.core.svg?branch=master)](https://travis-ci.org/Gradiant/bob.gradiant.core) [![Doc](http://img.shields.io/badge/docs-latest-orange.svg)](https://gradiant.github.io/bob.gradiant.core/)


[Bob](https://www.idiap.ch/software/bob/) package (python) which defines useful rules and interfaces for biometrics researching.

## Docker 

The fastest way to contact the package is to use docker. 

You can dowload the docker image from dockerhub

~~~
docker pull acostapazo/bob.gradiant:latest 
~~~

or build it from Dockerfile

~~~
docker build --no-cache -t acostapazo/bob.gradiant:latest .
~~~

To check if everything is alright you can run the ci.sh script with:

~~~
docker run -v $(pwd):/bob.gradiant.core acostapazo/bob.gradiant:latest bin/bash -c "cd bob.gradiant.core; ./ci.sh"
~~~


## Environment

We strongly recommend to use [conda](https://conda.io/docs/) to manage the project environment.

There is available two shared recipes to create the enviroment for this project on anaconda cloud.

*Linux*
~~~
conda env create gradiant/biometrics_py27
~~~

*Mac Os*
~~~
conda env create gradiant/biometrics_mac_py27
~~~

If you prefer to install the environment from yaml files:

*Linux*
~~~
conda env create -f environments/biometrics_ubuntu_py27.yml
~~~

*Mac Os*
~~~
conda env create -f environments/biometrics_mac_py27.yml
~~~


## Installation

We assume you have activate biometrics_py27 (or biometrics_mac_py27) environment 

~~~
source activate biometrics_py27
~~~

Then, you can buildout the project with:

~~~
  cd bob.gradiant.core
  python bootstrap-buildout.py
  bin/buildout
~~~

## Test

~~~
  bin/nosetests -v
~~~

## Clean

~~~
  python clean.py
~~~

## Coverage

~~~  
  bin/coverage run -m unittest discover
  bin/coverage html -i
  bin/coverage xml -i
~~~

Coverage result will be store on htmlcov/.

## Doc

~~~
bin/sphinx-build -b html doc/ doc/html/
~~~
