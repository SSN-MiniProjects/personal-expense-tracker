FROM python

COPY ./requirements.txt /flaskApp/requirements.txt

WORKDIR /flaskApp

RUN pip install -r requirements.txt

COPY . /flaskApp


ENTRYPOINT [ "python" ]
EXPOSE 5000
CMD ["app.py" ]

