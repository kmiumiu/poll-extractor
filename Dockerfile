# Define custom function directory
ARG FUNCTION_DIR="/function"

FROM mcr.microsoft.com/playwright/python:v1.48.0-noble as build-image

ARG FUNCTION_DIR

# Install aws-lambda-ric build dependencies
RUN apt-get update && apt-get install -y \
    g++ \
    make \
    cmake \
    unzip \
    libcurl4-openssl-dev \
    autoconf \
    libtool

# Install deps
RUN mkdir -p ${FUNCTION_DIR}
COPY requirements.txt ${FUNCTION_DIR}

RUN pip install --target ${FUNCTION_DIR} -r ${FUNCTION_DIR}/requirements.txt

# Copy function code
COPY lambda_function.py ${FUNCTION_DIR}

WORKDIR ${FUNCTION_DIR}

# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "python", "-m", "awslambdaric" ]

CMD ["lambda_function.lambda_handler"]
