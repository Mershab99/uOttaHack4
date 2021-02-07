docker build backend/. -t be-service
docker tag be-service mershab99/be-sani
docker push mershab99/be-sani

docker build my-app/. -t fe-service
docker tag fe-service mershab99/fe-sani
docker push mershab99/fe-sani