FROM python:3.9-bookworm
RUN apt-get update
RUN apt-get -y install libusb-1.0-0-dev
EXPOSE 5000
WORKDIR /userdata/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD ["python3", "main.py"]
