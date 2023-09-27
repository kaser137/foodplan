FROM python:3.10-slim

RUN mkdir "foodplan"

WORKDIR /foodplan

COPY ./requirements.txt /foodplan

RUN pip install -r /foodplan/requirements.txt

COPY . /foodplan

EXPOSE 4000

CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:4000"]

