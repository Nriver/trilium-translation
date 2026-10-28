import os
import re
import shutil
from zipfile import ZipFile

from settings import (
    BASE_FOLDER,
    VERSION_INFO_OVERRIDE,
    force_version_info,
    VERSION_INFO_OVERRIDE_BETA,
    force_version_info_beta,
)

# 源文件路径
TRILIUM_PLUS_ROOT = '/home/nate/gitRepo/trilium-plus/'
TRILIUM_PLUS_DIST = os.path.join(TRILIUM_PLUS_ROOT, 'dist/')

CLIENT_FOLDER = BASE_FOLDER + 'trilium-linux-x64'

CMD_STOP_SERVICE = """pkill -9 trilium"""

DO_DOWNLOAD = False
DO_DELETE = True


def copytree_ignore_broken(src, dst):
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.islink(s):
            try:
                linkto = os.readlink(s)
                if os.path.lexists(d):
                    try:
                        os.remove(d)
                    except Exception:
                        pass
                os.symlink(linkto, d)
            except Exception:
                continue
        elif os.path.isdir(s):
            copytree_ignore_broken(s, d)
        else:
            try:
                if os.path.lexists(d):
                    try:
                        os.remove(d)
                    except Exception:
                        pass
                shutil.copy2(s, d)
            except Exception:
                continue


def stop_service():
    if CMD_STOP_SERVICE:
        os.system(CMD_STOP_SERVICE)


def clean_cache():
    os.system('rm -rf ~/.config/Trilium Notes/Cache/')
    os.system('rm -rf ~/.config/Trilium Notes/Code Cache/')
    os.system('rm -rf ~/.config/Trilium Notes/GPUCache/')


def prepare_from_local():
    """从本地 trilium-plus 获取编译好的包和源码，不下载"""
    print(f'从本地获取 trilium-plus 文件: {TRILIUM_PLUS_ROOT}')

    # 获取编译好的包
    src_client = os.path.join(TRILIUM_PLUS_DIST, 'trilium-linux-x64')
    if os.path.exists(src_client):
        print(f'复制编译好的包: {src_client} -> {CLIENT_FOLDER}')
        if os.path.exists(CLIENT_FOLDER):
            shutil.rmtree(CLIENT_FOLDER)
        shutil.copytree(src_client, CLIENT_FOLDER)
    else:
        print('未找到编译好的 trilium-linux-x64 包')
        exit()

    # 获取源码 - 2.trans.py 期望结构: BASE_FOLDER/trilium-src/src/...
    src_root = os.path.join(TRILIUM_PLUS_ROOT, 'src')
    if not os.path.exists(src_root):
        print('未找到 trilium-plus/src')
        exit()

    dst_root = os.path.join(BASE_FOLDER, 'trilium-src')
    dst_src = os.path.join(dst_root, 'src')
    if os.path.exists(dst_root):
        shutil.rmtree(dst_root)
    os.makedirs(dst_src, exist_ok=True)

    print(f'复制源码: {src_root} -> {dst_src}')
    copytree_ignore_broken(src_root, dst_src)

    # 复制 trilium-plus 根目录的一些文件到 trilium-src 根目录
    for root_file in ['package.json', 'package-lock.json', 'webpack.config.js', 'webpack.excalidraw.config.js']:
        src_f = os.path.join(TRILIUM_PLUS_ROOT, root_file)
        if os.path.exists(src_f):
            try:
                shutil.copy2(src_f, os.path.join(dst_root, root_file))
            except Exception:
                pass


if __name__ == '__main__':
    if os.path.exists(BASE_FOLDER):
        if not (input(f'BASE_FOLDER exists! DELETE {BASE_FOLDER}, continue?(y)')).lower() in [
            'y',
            'yes',
        ]:
            exit()
        os.system(f'rm -rf {BASE_FOLDER}')
    os.makedirs(BASE_FOLDER)
    print('BASE_FOLDER', BASE_FOLDER)
    os.chdir(BASE_FOLDER)

    stop_service()
    clean_cache()

    prepare_from_local()

    print('finished!')
