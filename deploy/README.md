## 基础镜像构建

```shell script

sudo docker login -u username -p password registry-1.docker.io

sudo docker build   -f ./deploy/Dockerfile -t flask_example:v{versin_number} .

sudo docker tag flask_example:v{versin_number} hub.docker.com/1376178051/flask_example:v{versin_number}

sudo docker push hub.docker.com/1376178051/flask_example:v{versin_number}

```