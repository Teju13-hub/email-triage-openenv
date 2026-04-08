FROM python:3.10-slim

WORKDIR /app

# Install dependencies first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Hugging Face Spaces expects port 7860
EXPOSE 7860

# Default: run the Flask web server (validator-friendly)
# Override with: docker run ... python inference.py
CMD ["python", "app.py"]
