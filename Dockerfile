FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/flaskr /app/flaskr

CMD ["python", "-m", "src.flaskr.website",  "run", "--host=0.0.0.0"]