FROM python:latest

ADD coursefinder /coursefinder
WORKDIR /coursefinder

RUN pip3 install -r requirements.txt -U

EXPOSE 8000

CMD ["./manage.py", "runserver", "0.0.0.0:8000"]