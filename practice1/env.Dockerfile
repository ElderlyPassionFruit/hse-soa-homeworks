FROM python

WORKDIR /soa-practice1

COPY requirements.txt . 

RUN pip install  -r requirements.txt

COPY . .
