## Setting up common services for platform

1. In `common/` create a `.env` file for the services:
```sh
MINIO_ROOT_USER="minio-root-user"
MINIO_ROOT_PASSWORD="minio-root-password"
MINIO_ACCESS_KEY_ID="minio-access-key-id"
MINIO_SECRET_ACCESS_KEY="minio-secret-access-key"
REDIS_USER="redis-user"
REDIS_PASSWORD="redis-password"
```

2. Create the netowork so that services in other files can access these
```sh
docker network create --driver bridge my-network
```
3. Create a folder `data/` in `common/`.
```
cd common
mkdir data
```
4. Start the services
```sh
docker compose up
```
CTRL+C (maybe twice on codespaces) when you've confirmed everything is working as expected.

5 When you're sure it all works: 
```sh
docker compose up -d
```

And see what's working:
```sh
docker ps
```

You should see something like:
```
CONTAINER ID   IMAGE         COMMAND                  CREATED         STATUS         PORTS                                       NAMES
fd796492a007   minio/minio   "/usr/bin/docker-ent…"   6 minutes ago   Up 3 seconds   0.0.0.0:9000->9000/tcp, :::9000->9000/tcp   common-minio-1
8fac49448c08   redis         "docker-entrypoint.s…"   6 minutes ago   Up 3 seconds   0.0.0.0:6379->6379/tcp, :::6379->6379/tcp   common-redis-1
```

6. To turn it off
```sh
docker compose down
```