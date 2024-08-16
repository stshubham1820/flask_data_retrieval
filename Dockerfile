FROM python:3.10-slim

WORKDIR /flask_app

# Copy only requirements.txt to leverage Docker caching
COPY requirements.txt /flask_app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /flask_app

EXPOSE 8000

CMD ["gunicorn", "-w", "4","-k", "sync","-b", "0.0.0.0:8000", "--timeout", "120", "flask_app.main:app"]
