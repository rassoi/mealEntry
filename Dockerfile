FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install poppler-utils -y
RUN apt-get install libgl1-mesa-glx -y
EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]