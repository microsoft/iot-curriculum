```
sudo docker build -t falldetection .

sudo docker tag falldetection cartcr.azurecr.io/falldetection

sudo docker push cartcr.azurecr.io/falldetection

```

# On Device
```

docker login cartcr.azurecr.io
docker run  --name falldetection -it cartcr.azurecr.io/falldetection:latest


```
