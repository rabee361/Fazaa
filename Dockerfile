# Use an official Python runtime as a parent image
FROM python:3.11-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /home/app

# Install dependencies
COPY requirements.txt /home/app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /home/app/requirements.txt

# Copy project
COPY . /home/app

RUN python manage.py collectstatic --no-input

CMD ["python", "manage.py", "runserver" ,"0.0.0.0:8000"]
