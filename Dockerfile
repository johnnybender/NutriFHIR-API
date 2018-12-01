FROM python:3
WORKDIR .
COPY . .
RUN pip install -r requirements.txt
EXPOSE 80
EXPOSE 5000
COPY . /backend
CMD ["python", "app.py"]
