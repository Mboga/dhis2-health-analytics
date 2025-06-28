# Use a lightweight official Python image as a base
FROM python:3.9-slim-buster

# Install build dependencies for gevent and other packages that might need compilation
# `build-essential` includes gcc, g++, make, etc.
# `libev-dev` or `libevent-dev` might be needed for gevent's underlying event loop,
# though gevent usually bundles libev/libuv. Adding them just in case.
# `python3-dev` provides headers for Python C extensions.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libev-dev \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Explicitly ensure the /app directory exists (though WORKDIR does this, this is for robustness)
RUN mkdir -p /app

# Copy the requirements file into the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code into the container
# Use absolute paths for the destination to be super explicit
COPY app/app.py /app/app.py
COPY app/dhis2_data.csv /app/dhis2_data.csv
# COPY app/ .

# Expose the port your Dash app will run on (default Gunicorn port is 8000)
EXPOSE 8000

# Command to run the application using Gunicorn
# The `app.server` refers to the Flask server instance of your Dash app in app.py
# If your app.py is in 'src' directory, then it should be 'src.app:server'
CMD ["gunicorn", "--worker-class", "gevent", "--workers", "4", "--bind", "0.0.0.0:8000", "app:server"]
# If your app.py is in 'src/app.py', the command should be `src.app:server`
# Corrected based on your app.py being in `src/app.py` and the App Service expects `0.0.0.0`
# CMD ["gunicorn", "--worker-class", "gevent", "--workers", "4", "--bind", "0.0.0.0:8000", "src.app:server"]