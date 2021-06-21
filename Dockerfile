# Dockerfile for build up the image
FROM ubuntu:latest

LABEL MAINTAINER https://github.com/Nriver/trilium-translation

ADD trilium-linux-x64-server /app/
WORKDIR /app

EXPOSE 8080

CMD ["./trilium.sh"]