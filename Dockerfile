FROM conda/miniconda2:latest

MAINTAINER acosta@gradiant.org

RUN apt-get update && apt-get -y install git libopenblas-dev
ENV BUILD_NUMBER 0
RUN conda config --env --add channels defaults
RUN conda config --env --add channels https://www.idiap.ch/software/bob/conda
RUN conda install bob.io.image bob.io.video bob.measure h5py pandas bokeh pillow joblib mock scikit-learn sphinx_rtd_theme
RUN conda install gitpython=2.1.11
RUN conda install -c conda-forge opencv
RUN pip install enum34
