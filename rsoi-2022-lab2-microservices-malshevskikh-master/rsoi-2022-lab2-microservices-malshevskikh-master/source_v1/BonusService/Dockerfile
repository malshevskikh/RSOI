# syntax=docker/dockerfile:1

FROM python:3.8.5

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8050

WORKDIR /source_v1

COPY . /source_v1/

COPY requirements.txt /source_v1/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt


EXPOSE $PORT

#CMD ["python3", "manage.py", "runserver"]

#CMD [ "sh", "-c", "python3", "MaxFirstLab/manage.py runserver 0.0.0.0:$PORT"]

#CMD python3 manage.py runserver 0.0.0.0:$PORT