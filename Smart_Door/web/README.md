```
docker build -t iotdoor .
sudo docker tag iotdoor cartcr.azurecr.io/iotdoor

sudo docker push cartcr.azurecr.io/iotdoor
```