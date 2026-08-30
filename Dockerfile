#installing lighter version of python
FROM python:3.12-slim

#commands run form this folder inside the container
WORKDIR /app

#we copy the req.txt and download the prerquisites for the image
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copying rest of the code
COPY . .

#this container can be reached from this port 
EXPOSE 8000

#we run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]