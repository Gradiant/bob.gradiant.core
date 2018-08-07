# bob.gradiant.core 
[![Build Status](http://devel.gradiant.org/jenkins_biometrics/buildStatus/icon?job=bob.gradiant.core/master)](http://devel.gradiant.org/jenkins_biometrics/job/bob.gradiant.core/job/master/)
[![Doc](http://img.shields.io/badge/docs-latest-orange.svg)](http://10.5.1.61:8000/doc/private/bob/bob.gradiant.core/)

[Bob](https://www.idiap.ch/software/bob/) package template for Gradiant toolboxes.

#### Environment

We strongly recommend to use [conda](https://conda.io/docs/) to manage project environment.

There is available two shared recipes to create the enviroment for this project.

###### Linux
~~~
conda env create gradiant/biometrics_py27
~~~

###### Mac
~~~
conda env create gradiant/biometrics_mac_py27
~~~

If you prefer to install the environment from yaml files:

###### Linux
~~~
conda env create -f environments/biometrics_ubuntu_py27.yml
~~~

###### Mac
~~~
conda env create -f environments/biometrics_mac_py27.yml
~~~


#### Installation

We assume you have activate biometrics_py27 (or biometrics_mac_py27) environment 

~~~
source activate biometrics_py27
~~~

Then, you can do the following:

~~~
  cd bob.gradiant.core
  python bootstrap-buildout.py
  bin/buildout
~~~

#### Test

~~~
  bin/nosetests -v
~~~

#### Clean

~~~
  python clean.py
~~~

#### Coverage

~~~  
  bin/coverage run -m unittest discover
  bin/coverage html -i
  bin/coverage xml -i
~~~

Coverage result will be store on htmlcov/.

#### Doc

~~~
bin/sphinx-build -b html doc/ doc/html/
~~~