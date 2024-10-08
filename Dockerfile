#FROM ubuntu:latest
#LABEL authors="caine"
#
#ENTRYPOINT ["top", "-b"]
#
#FROM python:3.9-slim
#WORKDIR /app
#COPY . /app
#
#RUN pip install --no-cache-dir -r requirements.txt
#EXPOSE 8080
#CMD ["python", "fitness.py"]


FROM python:3.9-slim
WORKDIR /app
COPY . /app

RUN pip install --no-cache -r requirements.txt
EXPOSE 8080
#CMD python3 ./fitness.py будемо управляти з докер-компоуз файлу