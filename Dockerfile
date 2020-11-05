# set base image (host OS)
FROM amd64/python:3.7-slim-stretch

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN    apt-get update \
    && apt-get install -y --no-install-recommends \
               ca-certificates \
               git \
               build-essential \
               libssl-dev \
               libffi-dev \
               libunwind-dev \
               libsnappy-dev \
               libbz2-dev \
    && rm -rf ~/.cache \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip && \
    pip install -U setuptools && \
    pip install autobahn[twisted,asyncio,accelerate,serialization,encryption,xbr]
RUN pip3 install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY autobahn_subscriber.py .

# command to run on container start
CMD [ "python3", "./autobahn_subscriber.py" ]
