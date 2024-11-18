FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directory for user preferences
RUN mkdir -p /app/user_prefs

# Expose port
EXPOSE 7862

# Command to run the application
CMD ["python", "main.py"]
