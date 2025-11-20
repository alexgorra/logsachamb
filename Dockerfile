FROM python:3.12

WORKDIR /app

COPY /requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make start script executable
RUN chmod +x start.sh

EXPOSE 8000 8080

ENV PYTHONUNBUFFERED=1

CMD ["./start.sh"]