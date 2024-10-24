FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE=1  # Prevent Python from writing pyc files to disc
ENV PYTHONUNBUFFERED=1         # Prevent Python from buffering stdout and stderr
WORKDIR /app
COPY requirements.txt /app/
RUN pip install requirements.txt
COPY . /app/
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0"]