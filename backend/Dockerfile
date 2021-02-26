FROM insightful/alpine-python

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

ADD . /app
ENTRYPOINT [ "python" ]

CMD ["backend.py"]