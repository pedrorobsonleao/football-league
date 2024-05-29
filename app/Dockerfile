FROM python:3-alpine

# ENV DEBIAN_FRONTEND noninteractive

WORKDIR /app

COPY . /app/

RUN \
    addgroup -S app && \
    adduser -G app -S app && \
    python -m venv /app && \
    pip install \
    --root-user-action=ignore \
    pandas \
    pymongo
    
USER app

ENTRYPOINT [ "python", "./football.py" ]