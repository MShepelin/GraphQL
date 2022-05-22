FROM python:3.7
COPY . .
RUN apt-get update
RUN apt-get install redis-server -y
RUN pip install -r requirements.txt
EXPOSE 5001
CMD redis-server & python3 -u server.py
