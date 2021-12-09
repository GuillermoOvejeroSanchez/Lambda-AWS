FROM public.ecr.aws/lambda/python:3.8

# https://github.com/pypa/pipenv/issues/4220
RUN pip install pipenv==2018.11.26
COPY ./app ./app
COPY Pipfile.lock Pipfile.lock
COPY Pipfile Pipfile
RUN pipenv install --deploy && cp -r $(pipenv --venv)/lib/python3.8/site-packages/. ./

CMD ["app.main.handler"]