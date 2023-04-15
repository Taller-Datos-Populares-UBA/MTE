FROM python:3.9.10-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn","index:server","-b 0.0.0.0:8000"]
