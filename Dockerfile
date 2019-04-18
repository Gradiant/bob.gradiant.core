FROM conda/miniconda3:latest

MAINTAINER acosta@gradiant.org

RUN apt-get update && apt-get -y install \
    git wget unzip libopenblas-dev 
ENV BUILD_NUMBER 0
RUN conda config --env --add channels defaults
RUN conda config --env --add channels https://www.idiap.ch/software/bob/conda
RUN conda install bob.io.video bob.measure h5py pandas bokeh pillow joblib mock scikit-learn sphinx_rtd_theme gitpython configobj
RUN conda install -c conda-forge phantomjs
RUN pip install coloredlogs selenium bokeh==0.13.0
RUN pip install xgboost
