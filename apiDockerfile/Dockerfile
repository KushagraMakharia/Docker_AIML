FROM python:3.8-bullseye

COPY ./api ./api

COPY ./artifacts ./artifacts

RUN pip install -r ./api/requirements.txt

CMD ["python", "./api/app.py"]