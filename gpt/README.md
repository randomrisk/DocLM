# gpt

### vultr

### vultr
```
ssh -i ~/.ssh/id_rsa root@149.28.157.168
```

### docker (ubuntu20.04)
```
sudo apt-get update
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/ \
  $(lsb_release -cs) \
  stable"
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo docker run hello-world

sudo apt-get install docker-compose

```
### network
```
docker network create --driver=bridge --subnet=192.168.89.0/24 gpt
```

### server
```
cd server
docker build -t gpt-server:dev -f prod/Dockerfile .
# prod/.env AUTH_CODE和OPENAI_KEYS
docker-compose -f prod/docker-compose.yaml --env-file prod/.env up

make docker && make rund

#
docker logs -f gpt-server
```

### nginx
```
cd nginx
docker build -t nginx:dev -f Dockerfile .
docker-compose -f docker-compose.yaml up -d

make docker && make rund
```

### Test external visiting of the api
```
curl http://149.28.157.168:8000/gpt-server/gpt -X POST -d '{"auth_code":"839945449heros","question":"hello"}'
```