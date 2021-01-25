FROM python:3.7.9
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system --deploy --ignore-pipfile
COPY . /code/
