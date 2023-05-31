# syntax=docker/dockerfile:1

FROM python:3.10.6

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN chmod 777 -R /tmp && chmod o+t -R /tmp

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
