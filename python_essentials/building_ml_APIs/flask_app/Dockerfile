FROM python:3.8

COPY ./requirements.txt /webapp/requirements.txt

WORKDIR /webapp

RUN pip install --no-cache-dir -r requirements.txt

COPY webapp/* /webapp

ENTRYPOINT ["python"]

CMD ["app.py"]