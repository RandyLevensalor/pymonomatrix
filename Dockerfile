FROM python:3.10.10

WORKDIR /app

COPY requirements.txt requirements.txt
COPY pymonomatrix pymonomatrix
COPY setup.py setup.py
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "sleep", "infinity" ]

