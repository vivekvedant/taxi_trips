# echo "install loki pugin"
# docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions
echo "killing old docker processes"
docker-compose  down -v
echo "build image"
docker-compose build --no-cache
# echo "change tag"
# docker tag grafana/loki:v1.3.0  vivekvedant/taki_trips:loki
echo "building docker containers"
docker-compose up -d
echo "test flask_app container"
docker-compose exec flask_app pytest "tests"


