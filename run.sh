rm tokens.db
docker build -t py .
docker run -ti -v "$PWD:/project" py