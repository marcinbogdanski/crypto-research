FROM python:3.9.0-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl

RUN pip install --upgrade pip


# Jupyter Notebook
RUN pip install jupyterlab==3.0.7
RUN pip install nbdime==2.1.0
RUN pip install ipywidgets==7.6.3

# Jupyter Notebook Extensions
RUN curl -sL https://deb.nodesource.com/setup_15.x | bash -
RUN apt-get install -y nodejs
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager
RUN jupyter labextension install nbdime-jupyterlab

# Third Party
# RUN pip install numpy==1.19.4
# RUN pip install matplotlib==3.3.3
# RUN pip install pandas==1.1.4
# RUN pip install tqdm==4.52.0


ENV PYTHONPATH="/app"

# Docker COPY goes at the very end to minimise Docker cache misses during build
COPY . /app
WORKDIR /app

# Build like this:
# docker build -t crypto-research .