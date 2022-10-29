FROM python:3.9-alpine

# Install requirements
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Run the app
CMD ["uvicorn", "api.fastapi.main:app", "--host", "0.0.0.0", "--port", "8000"]
