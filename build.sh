docker build -t be backend/.
docker tag be mershab99/be-sani
docker push mershab99/be-sani
docker build -t fe my-app/.
docker tag fe mershab99/fe-sani
docker push mershab99/fe-sani