# Use official Python image
FROM python:3.10
 
# Set working directory
WORKDIR /app
COPY . . 

# Install dependencies
RUN pip install -r requirements.txt
 
# Run the application
CMD ["python", "app.py"]