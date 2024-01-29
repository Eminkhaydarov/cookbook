
FROM python:latest

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/cookbook

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/cookbook/entrypoint.sh
RUN chmod +x /usr/src/cookbook/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/cookbook/entrypoint.sh"]