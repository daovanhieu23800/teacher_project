FROM tiangolo/uvicorn-gunicorn:python3.9

RUN mkdir /fastapi

COPY requirements.txt /fastapi

WORKDIR /fastapi

RUN pip install -r requirements.txt --proxy http://192.168.100.210:3128

COPY . /fastapi

EXPOSE 8080

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]