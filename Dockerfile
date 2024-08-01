# Dockerfile for build up the image
FROM ubuntu:latest

LABEL MAINTAINER https://github.com/Nriver/trilium-translation

# 添加curl jq命令给health check使用
# 合并RUN减少镜像层数
# 减少镜像大小 purge清理包列表
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
    && apt-get clean \
    && apt-get update \
    && apt-get install -y curl jq \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

ADD trilium-linux-x64-server /app/
WORKDIR /app

EXPOSE 8080

CMD ["./trilium.sh"]

