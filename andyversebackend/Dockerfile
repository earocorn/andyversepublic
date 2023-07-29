FROM python:3.11.3

RUN apt-get update && apt-get install -y curl

ENV PYTHONUNBUFFERED=1

COPY certs ./certs

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000 

#CMD ["python","manage.py","runserver"]
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
