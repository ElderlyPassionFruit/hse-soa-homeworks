FROM python

WORKDIR /soa-practice2

COPY requirements.txt .

RUN pip install  -r requirements.txt

COPY . .
