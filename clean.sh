rm -rf ~/.llama
mkdir -p ~/.llama

docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
docker system prune -a --volumes
