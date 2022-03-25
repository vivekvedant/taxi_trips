echo killing old docker processes
docker-compose  down -v
echo building docker containers
docker-compose up --build  -d
echo test flask_app container
docker-compose exec flask_app pytest "tests"