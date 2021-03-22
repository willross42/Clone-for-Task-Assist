FROM python:3.8-slim-buster

WORKDIR /app

# Dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# App
COPY . /app

EXPOSE 5000

CMD ["python","-u","app.py"]