FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y nginx git python-setuptools python-dev
RUN easy_install pip

RUN mkdir -p /app/src

WORKDIR /app/src

COPY src/requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 80 8000

COPY /src .

CMD ["python3", "app.py"]