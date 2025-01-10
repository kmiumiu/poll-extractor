FROM mcr.microsoft.com/playwright/python:v1.48.0-noble as build-image

WORKDIR /code

RUN apt-get update && apt-get install -y \
    g++ \
    make \
    cmake \
    unzip \
    libcurl4-openssl-dev \
    autoconf \
    libtool

# Install deps
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy function code
COPY ./main.py /code/main.py

EXPOSE 5000

CMD ["fastapi", "run", "main.py", "--port", "5000"]
