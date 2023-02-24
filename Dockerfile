# Dockerfile for build up the image
FROM ubuntu:latest

LABEL MAINTAINER https://github.com/Nriver/trilium-translation

RUN info(){ printf '\x1B[32m--\n%s\n--\n\x1B[0m' "$*"; } && \
    addgroup -gid 1000 triliumgroup && \
    adduser -uid 1000 -gid 1000 triliumuser

USER triliumuser:triliumgroup

ADD --chown=triliumuser:triliumgroup trilium-linux-x64-server /app/
WORKDIR /app


EXPOSE 8080

CMD ["./trilium.sh"]
