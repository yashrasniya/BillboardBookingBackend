FROM python:3
LABEL authors="Yash"

#ENTRYPOINT ["top", "-b"]
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1
WORKDIR /sd
ADD . /sd
COPY . /sd
COPY req.txt /sd/req.txt

RUN pip install --default-timeout=100 -r  req.txt
RUN python manage.py makemigrations
RUN python manage.py migrate

COPY . /sd

CMD ["python","manage.py","runserver"]

 