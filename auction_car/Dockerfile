FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /auction_car

COPY req.txt /auction_car/
RUN pip install gunicorn
RUN pip install setuptools
RUN pip install --upgrade pip && \
    pip install -r req.txt

COPY . /auction_car/