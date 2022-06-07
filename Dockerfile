FROM python:3.9.5

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .
COPY Makefile .

RUN make install

COPY . .

EXPOSE 8000
