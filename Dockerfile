#use official Python image
FROM python:3.12


# Install system packages needed by pipenv
RUN apt-get update && apt-get install -y gcc curl && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy Pipenv files
COPY Pipfile Pipfile.lock ./

# Install pipenv & deps
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copy the rest of the app
COPY . .

# Run app using pipenv
CMD ["pipenv", "run", "python", "run.py"]
