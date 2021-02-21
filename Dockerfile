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
RUN pip install beautifulsoup4==4.9.3
RUN pip install boto3==1.17.13
RUN pip install lxml==4.6.2
RUN pip install smart-open==4.2.0

# Development
RUN pip install pylint


ENV PYTHONPATH="/app"

# Docker COPY goes at the very end to minimise Docker cache misses during build
COPY . /app
WORKDIR /app

ENTRYPOINT ["python", "-m", "scrapper.main"]

# Build like this:
# docker build -t crypto-research .