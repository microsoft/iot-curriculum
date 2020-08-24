FROM arm32v7/python:3

COPY qemu-arm-static /usr/bin

WORKDIR /usr/src/app

#COPY requirements.txt ./
COPY . .
RUN pip install --no-cache-dir -r requirements.txt



#CMD [ "python", "./AnolalyDetection.py" ]


