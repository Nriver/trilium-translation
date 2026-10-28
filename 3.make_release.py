import os
import re
import shutil

import requests
import urllib3

from settings import (
    DEBUG,
    PATCH_FOLDER,
    LANG,
    TRANS_RELEASE_FOLDER,
    USE_PROXY,
    PROXIES,
    ASAR_PATH,
)

# 本地 trilium-plus 打包文件目录
LOCAL_DIST = '/home/nate/gitRepo/trilium-plus/dist/'  # disable warning if we use proxy
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COMPRESS_TOOL = '7z'

COMPRESS_LEVEL = 9

REPO_NAME = 'nriver/trilium-plus'


# 是否从GitHub下载文件
# whether download files from GitHub
DO_DOWNLOAD = False

# 是否删除临时文件
# whether delete template files
DO_DELETE = True


def requests_get(url):
    ret = None
    try:
        ret = requests.get(url, proxies=PROXIES, verify=not USE_PROXY)
    except Exception as e:
        print('Exception', e)
    return ret


def get_local_releases():
    """从本地 trilium-plus/dist 获取发布文件，直接从文件名解析版本号"""
    print('get local releases from', LOCAL_DIST)
    patterns = {
        'linux': r'trilium-linux-x64-([0-9\.]+)\.tar\.xz',
        'linux-server': r'trilium-linux-x64-server-([0-9\.]+)\.tar\.xz',
        'windows': r'trilium-windows-x64-([0-9\.]+)\.7z',
        'mac': r'trilium-mac-x64-([0-9\.]+)\.zip',
    }

    releases = {}
    version = None

    for fname in os.listdir(LOCAL_DIST):
        for package_type, pattern in patterns.items():
            m = re.match(pattern, fname)
            if m:
                if version is None:
                    version = m.group(1)
                elif version != m.group(1):
                    print(f'警告：不同平台版本号不一致 {version} vs {m.group(1)}')
                releases[package_type] = {'name': fname, 'url': os.path.join(LOCAL_DIST, fname)}
                break

    if not version:
        print('未在本地 dist 找到匹配的 trilium 发布包')
        print('请检查', LOCAL_DIST)
        raise FileNotFoundError('no local release packages found')

    version_info = {'name': f'v{version} release', 'releases': releases}
    print('version_info', version_info)
    return version_info


def download_file(url, file_name=None):
    """copy local file from trilium-plus/dist"""
    print('copy local file')
    if not file_name:
        file_name = os.path.basename(url)
    print(f'copying from {url} -> {file_name}')
    src = url
    dst = file_name

    if not os.path.isabs(src):
        src = os.path.join(LOCAL_DIST, src)

    if not os.path.exists(src):
        print(f'本地文件不存在: {src}')
        raise FileNotFoundError(src)

    shutil.copy2(src, dst)
    print(f'copy complete, file saved as {file_name}')
    return file_name


def download_releases(releases):
    for package_type in releases:
        if DEBUG:
            if package_type != 'linux':
                continue
        release = releases[package_type]
        download_file(release['url'], TRANS_RELEASE_FOLDER + release['name'])


def download_release(releases, package_type):
    for x in releases:
        if x == package_type:
            release = releases[x]
            download_file(release['url'], TRANS_RELEASE_FOLDER + release['name'])
            return


def download_and_patch(releases, package_type):
    download_release(releases, package_type)
    file_name = releases[package_type]['name']
    if package_type == 'linux':
        patch_linux(file_name)
    elif package_type == 'windows':
        patch_windows(file_name)
    elif package_type == 'linux-server':
        patch_linux_server(file_name)
    elif package_type == 'mac':
        patch_mac(file_name)


def decompress_package(file_name):
    print(f'decompress {file_name}')
    if file_name.endswith('tar.xz'):
        try:
            os.system(f'xz -d {file_name}')
        except Exception:
            pass
        try:
            os.system(f'tar -xf {file_name[:-3]}')
            if DO_DELETE:
                os.system(f'rm -f {file_name[:-3]}')
        except Exception:
            pass
    elif file_name.endswith('.7z'):
        try:
            os.system(f'7z x -y {file_name}')
            if DO_DELETE:
                os.system(f'rm -f {file_name}')
        except Exception:
            pass
    elif file_name.endswith('.zip'):
        try:
            os.system(f'unzip -o {file_name}')

            if DO_DELETE:
                os.system(f'rm -f {file_name}')
        except Exception:
            pass


def patch_linux(file_name):
    if not file_name.endswith('.tar.xz'):
        print('linux客户端文件名有问题')
        print('linux client wrong file name')
        exit()

    file_path = TRANS_RELEASE_FOLDER + file_name
    print('file_path', file_path)
    decompress_package(file_path)

    asar_folder = TRANS_RELEASE_FOLDER + 'trilium-linux-x64/resources'
    asar_path = asar_folder + '/app.asar'
    print(asar_path)

    # asar解包
    # asar unpack
    os.chdir(asar_folder)
    os.system(f'"{ASAR_PATH}" extract app.asar ./app/')

    # 打补丁
    # apply patch
    os.system(f'cp -rf {PATCH_FOLDER}* "{asar_folder}/app/"')

    # asar封包
    # asar pack
    os.system(f'"{ASAR_PATH}" pack app/ app.asar')

    if not DEBUG:
        # 删除解包文件
        # remove unpacked files
        os.system(f'rm -rf {asar_folder}/app/')

        # 打tar.xz包
        new_name = f'trilium-{LANG}-linux-x64.tar.xz'
        print('new_name', new_name)
        os.system(f'rm -f {new_name}')
        patched_root_folder = 'trilium-linux-x64'
        os.chdir(TRANS_RELEASE_FOLDER)

        cmd = f'tar -cf - {patched_root_folder} | xz -{COMPRESS_LEVEL} -c > {new_name}'
        print(cmd)
        os.system(cmd)

        if DO_DELETE:
            os.system('rm -rf trilium-linux-x64')

        return new_name


def patch_linux_server(file_name):
    if not file_name.endswith('.tar.xz'):
        print('linux server 文件名有问题')
        print('linux server wrong file name')
        exit()

    file_path = TRANS_RELEASE_FOLDER + file_name
    print('file_path', file_path)
    decompress_package(file_path)

    # 打补丁
    # apply patch
    cmd = f'cp -rf {PATCH_FOLDER}* {TRANS_RELEASE_FOLDER}/trilium-linux-x64-server/'
    print('cmd', cmd)
    os.system(cmd)

    # 打tar.xz包
    new_name = f'trilium-{LANG}-linux-x64-server.tar.xz'
    print('new_name', new_name)
    os.system(f'rm -f {new_name}')
    patched_root_folder = 'trilium-linux-x64-server'
    os.chdir(TRANS_RELEASE_FOLDER)
    cmd = f'tar -cf - {patched_root_folder} | xz -{COMPRESS_LEVEL} -c > {new_name}'
    print(cmd)
    os.system(cmd)

    if DO_DELETE:
        os.system('rm -rf trilium-linux-x64-server')

    return new_name


def patch_windows(file_name):
    if not (file_name.endswith('.zip') or file_name.endswith('.7z')):
        print('windows 文件名有问题')
        exit()

    file_path = TRANS_RELEASE_FOLDER + file_name
    print('file_path', file_path)
    decompress_package(file_path)

    asar_folder = TRANS_RELEASE_FOLDER + 'trilium-windows-x64/resources'
    asar_path = asar_folder + '/app.asar'
    print(asar_path)

    # asar解包
    os.chdir(asar_folder)
    os.system(f'"{ASAR_PATH}" extract app.asar ./app/')

    # 打补丁
    # apply patch
    os.system(f'cp -rf {PATCH_FOLDER}* {asar_folder}/app/')

    # asar封包
    # asar pack
    os.system(f'"{ASAR_PATH}" pack app/ app.asar')
    # 删除解包文件
    # remove unpacked files
    os.system(f'rm -rf {asar_folder}/app/')

    # 打7z包
    new_name = f'trilium-{LANG}-windows-x64.7z'
    print('new_name', new_name)
    os.system(f'rm -f {new_name}')
    patched_root_folder = 'trilium-windows-x64'
    os.chdir(TRANS_RELEASE_FOLDER)
    cmd = f'7z a {new_name} -r {patched_root_folder}'
    print(cmd)
    os.system(cmd)

    if DO_DELETE:
        os.system('rm -rf trilium-windows-x64')

    return new_name


def patch_mac(file_name):
    if not file_name.endswith('.zip'):
        print('mac 文件名有问题')
        exit()

    file_path = TRANS_RELEASE_FOLDER + file_name
    print('file_path', file_path)
    decompress_package(file_path)

    asar_folder = TRANS_RELEASE_FOLDER + 'trilium-mac-x64/Trilium Notes.app/Contents/Resources'
    asar_path = asar_folder + '/app.asar'
    print(asar_path)

    # asar解包
    # asar unpack
    os.chdir(asar_folder)
    os.system(f'"{ASAR_PATH}" extract app.asar ./app/')

    # 打补丁
    # apply patch
    os.system(f'cp -rf {PATCH_FOLDER}* "{asar_folder}/app/"')

    # asar封包
    # asar pack
    os.system(f'"{ASAR_PATH}" pack app/ app.asar')

    # 删除解包文件
    # remove unpacked files
    cmd = f'rm -rf "{asar_folder}/app/"'
    print('cmd', cmd)
    os.system(cmd)
    # 打zip包
    # make zip package
    new_name = f'trilium-{LANG}-mac-x64.zip'
    print('new_name', new_name)
    os.system(f'rm -f {new_name}')
    patched_root_folder = 'trilium-mac-x64'
    os.chdir(TRANS_RELEASE_FOLDER)
    cmd = f'zip -{COMPRESS_LEVEL} -y -r {new_name} {patched_root_folder}'
    print('压缩命令', cmd)
    os.system(cmd)

    if DO_DELETE:
        os.system('rm -rf trilium-mac-x64')

    return new_name


if __name__ == '__main__':
    print(f'DEBUG is {DEBUG}')

    a = input(f'Delete folder {TRANS_RELEASE_FOLDER}, continue?(y)')
    if a not in [
        'y',
    ]:
        exit()

    os.system(f'rm -rf {TRANS_RELEASE_FOLDER}')
    os.makedirs(f'{TRANS_RELEASE_FOLDER}')
    os.chdir(TRANS_RELEASE_FOLDER)

    # 获取本地发布文件信息
    version_info = get_local_releases()
    print('version_info', version_info)

    # 获取文件并打补丁
    releases = version_info['releases']

    # linux
    download_and_patch(releases, 'linux')

    if not DEBUG:
        # linux-server
        download_and_patch(releases, 'linux-server')

        # windows
        download_and_patch(releases, 'windows')

        # mac
        download_and_patch(releases, 'mac')

    os.system(f'xdg-open {TRANS_RELEASE_FOLDER}')

    print('finished')
