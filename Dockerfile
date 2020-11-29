FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app/
ARG CACHEBUST=2
RUN bash -c "ls"

# Install Pipenv
RUN bash -c "pip install pipenv"

# Copy Pipfile.lock* in case it doesn't exist in the repo
COPY ./app/Pipfile ./app/Pipfile.lock /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pipenv install --dev --pre --system --deploy --ignore-pipfile ; else pipenv install --pre --system --deploy --ignore-pipfile ; fi"

# Copy main application
COPY ./app /app

ENV PYTHONPATH=/app