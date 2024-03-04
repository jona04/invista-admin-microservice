## Pipeline

- Docker compose editar ver da imagem em image:
- docker compose -f docker-compose.prod.yml build
- docker tag invista/users:0.0.9 gcr.io/invista-367601/users 
- docker push gcr.io/invista-367601/admin
- docker tag invista/admin:0.0.12 gcr.io/invista-367601/admin