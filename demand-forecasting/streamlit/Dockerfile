FROM python:3.9-slim

RUN mkdir /streamlit

COPY requirements.txt /streamlit

WORKDIR /streamlit

RUN pip install -r requirements.txt --proxy http://192.168.100.210:3128

COPY . /streamlit

EXPOSE 8501

CMD ["streamlit", "run", "ui.py"]