FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-2022-11-25
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
ENV PYTHONPATH=/code

# install python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt