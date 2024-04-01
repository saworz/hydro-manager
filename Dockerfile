FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ./requirements.txt .
COPY ./requirements_dev.txt .
RUN pip install -r requirements.txt
RUN pip install -r requirements_dev.txt
COPY . .