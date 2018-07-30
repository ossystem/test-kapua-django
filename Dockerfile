FROM python:2.7
WORKDIR /w/
COPY . /w/
RUN pip install -r requirements.txt
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
