import contextlib
import os
import re
import shutil

import requests
import urllib3

from settings import (
    PATCH_FOLDER,
    LANG,
    TRANS_RELEASE_FOLDER,
    USE_PROXY,
    PROXIES,
    ASAR_PATH,
)


DEBUG = False
# DEBUG = True

# 本次要打包的端（默认全部）
# 可选值: linux / linux-server / linux-server-arm64 / windows / mac / debian
ALL_PACKAGES = [
    'linux',
    'linux-server',
    'linux-server-arm64',
    'windows',
    'mac',
    'debian',
]

# DEBUG=True 时只打包这里列出的端，方便单独打包某些端进行测试
# 例如只测试 linux 客户端和 arm64 server:
DEBUG_PACKAGES = [
    'linux',
    'linux-server-arm64',
]

# DEBUG 只负责选择打包目标，不再影响是否生成最终安装包
PACKAGES = DEBUG_PACKAGES if DEBUG else ALL_PACKAGES

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


@contextlib.contextmanager
def release_workdir():
    """每个包都从发布目录开始处理，结束时（含异常）恢复原工作目录。

    之前各 patch 函数靠末尾手动 chdir 回发布目录，DEBUG 提前返回或调换打包顺序时，
    cwd 会残留在某个 asar 目录里，导致后续包解压/打补丁到错误位置而失败。
    """
    previous = os.getcwd()
    os.chdir(TRANS_RELEASE_FOLDER)
    try:
        yield
    finally:
        os.chdir(previous)


def add_lang_suffix(file_name):
    """在原文件名基础上添加语言后缀，保留版本号信息
    例如 trilium-linux-x64-0.60.4.tar.xz -> trilium-linux-x64-0.60.4-cn.tar.xz
    """
    for ext in ('.tar.xz', '.7z', '.zip', '.deb'):
        if file_name.endswith(ext):
            return f'{file_name[:-len(ext)]}-{LANG}{ext}'
    return f'{file_name}-{LANG}'


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
        'linux-server-arm64': r'trilium-linux-arm64-server-([0-9\.]+)\.tar\.xz',
        'windows': r'trilium-windows-x64-([0-9\.]+)\.7z',
        'mac': r'trilium-mac-x64-([0-9\.]+)\.zip',
        'debian': r'trilium_([0-9\.]+)_(?:amd64|arm64|i386)\.deb',
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


def download_release(releases, package_type):
    for x in releases:
        if x == package_type:
            release = releases[x]
            download_file(release['url'], os.path.join(TRANS_RELEASE_FOLDER, release['name']))
            return


def download_and_patch(releases, package_type):
    """单独处理一个端：干净目录 + 独立工作目录，顺序可任意调换。"""
    with release_workdir():
        if package_type not in releases:
            print(f'跳过 {package_type}：本地 dist 中没有对应的发布包')
            return None

        # 清掉之前可能残留的同名目录，避免旧文件混进新包（也支持 DO_DELETE=False）
        root_folder = PACKAGE_ROOT_FOLDERS[package_type]
        os.system(f'rm -rf "{os.path.join(TRANS_RELEASE_FOLDER, root_folder)}"')

        download_release(releases, package_type)
        file_name = releases[package_type]['name']
        new_name = PACKAGE_PATCHERS[package_type](file_name)

        new_path = os.path.join(TRANS_RELEASE_FOLDER, new_name)
        if not os.path.exists(new_path):
            raise RuntimeError(f'{package_type} 打包失败：没有生成 {new_path}')
        print(f'[{package_type}] 打包完成: {new_name}')
        return new_name


def decompress_package(file_name):
    print(f'decompress {file_name}')
    # 解压目标目录由调用者决定，这里强制切到发布目录，避免受上一个包的 cwd 影响
    with release_workdir():
        if file_name.endswith('tar.xz'):
            # 先清掉上次可能残留的中间文件，否则 xz 会因目标已存在而失败
            try:
                os.system(f'rm -f "{file_name[:-3]}"')
                os.system(f'xz -d "{file_name}"')
            except Exception:
                pass
            try:
                os.system(f'tar -xf "{file_name[:-3]}"')
                if DO_DELETE:
                    os.system(f'rm -f "{file_name[:-3]}"')
            except Exception:
                pass
        elif file_name.endswith('.7z'):
            try:
                os.system(f'7z x -y "{file_name}"')
                if DO_DELETE:
                    os.system(f'rm -f "{file_name}"')
            except Exception:
                pass
        elif file_name.endswith('.zip'):
            try:
                os.system(f'unzip -o "{file_name}"')

                if DO_DELETE:
                    os.system(f'rm -f "{file_name}"')
            except Exception:
                pass


def patch_linux(file_name):
    if not file_name.endswith('.tar.xz'):
        print('linux客户端文件名有问题')
        print('linux client wrong file name')
        exit()

    with release_workdir():
        file_path = os.path.join(TRANS_RELEASE_FOLDER, file_name)
        print('file_path', file_path)
        decompress_package(file_path)

        asar_folder = os.path.join(TRANS_RELEASE_FOLDER, 'trilium-linux-x64/resources')
        asar_path = os.path.join(asar_folder, 'app.asar')
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

        # 解包目录必须删掉，否则会被一起打进安装包
        # remove unpacked files before archiving
        os.system(f'rm -rf "{asar_folder}/app/"')

        # 打tar.xz包
        new_name = add_lang_suffix(file_name)
        print('new_name', new_name)
        patched_root_folder = 'trilium-linux-x64'
        os.chdir(TRANS_RELEASE_FOLDER)
        os.system(f'rm -f "{new_name}"')

        cmd = f'tar -cf - {patched_root_folder} | xz -{COMPRESS_LEVEL} -c > "{new_name}"'
        print(cmd)
        os.system(cmd)

        if DO_DELETE:
            os.system(f'rm -rf {patched_root_folder}')

        return new_name


def patch_linux_server(file_name):
    if not file_name.endswith('.tar.xz'):
        print('linux server 文件名有问题')
        print('linux server wrong file name')
        exit()

    with release_workdir():
        file_path = os.path.join(TRANS_RELEASE_FOLDER, file_name)
        print('file_path', file_path)
        decompress_package(file_path)

        if 'arm64' in file_name:
            patched_root_folder = 'trilium-linux-arm64-server'
        else:
            patched_root_folder = 'trilium-linux-x64-server'
        new_name = add_lang_suffix(file_name)

        # 打补丁
        # apply patch
        cmd = f'cp -rf {PATCH_FOLDER}* "{os.path.join(TRANS_RELEASE_FOLDER, patched_root_folder)}/"'
        print('cmd', cmd)
        os.system(cmd)

        # 打tar.xz包
        print('new_name', new_name)
        os.chdir(TRANS_RELEASE_FOLDER)
        os.system(f'rm -f "{new_name}"')
        cmd = f'tar -cf - {patched_root_folder} | xz -{COMPRESS_LEVEL} -c > "{new_name}"'
        print(cmd)
        os.system(cmd)

        if DO_DELETE:
            os.system(f'rm -rf {patched_root_folder}')

        return new_name


def patch_windows(file_name):
    if not (file_name.endswith('.zip') or file_name.endswith('.7z')):
        print('windows 文件名有问题')
        exit()

    with release_workdir():
        file_path = os.path.join(TRANS_RELEASE_FOLDER, file_name)
        print('file_path', file_path)
        decompress_package(file_path)

        asar_folder = os.path.join(TRANS_RELEASE_FOLDER, 'trilium-windows-x64/resources')
        asar_path = os.path.join(asar_folder, 'app.asar')
        print(asar_path)

        # asar解包
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
        os.system(f'rm -rf "{asar_folder}/app/"')

        # 打7z包
        new_name = add_lang_suffix(file_name)
        print('new_name', new_name)
        patched_root_folder = 'trilium-windows-x64'
        os.chdir(TRANS_RELEASE_FOLDER)
        os.system(f'rm -f "{new_name}"')
        cmd = f'7z a "{new_name}" -r {patched_root_folder}'
        print(cmd)
        os.system(cmd)

        if DO_DELETE:
            os.system(f'rm -rf {patched_root_folder}')

        return new_name


def patch_mac(file_name):
    if not file_name.endswith('.zip'):
        print('mac 文件名有问题')
        exit()

    with release_workdir():
        file_path = os.path.join(TRANS_RELEASE_FOLDER, file_name)
        print('file_path', file_path)
        decompress_package(file_path)

        asar_folder = os.path.join(
            TRANS_RELEASE_FOLDER, 'trilium-mac-x64/Trilium Notes.app/Contents/Resources'
        )
        asar_path = os.path.join(asar_folder, 'app.asar')
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
        new_name = add_lang_suffix(file_name)
        print('new_name', new_name)
        patched_root_folder = 'trilium-mac-x64'
        os.chdir(TRANS_RELEASE_FOLDER)
        os.system(f'rm -f "{new_name}"')
        cmd = f'zip -{COMPRESS_LEVEL} -y -r "{new_name}" {patched_root_folder}'
        print('压缩命令', cmd)
        os.system(cmd)

        if DO_DELETE:
            os.system(f'rm -rf {patched_root_folder}')

        return new_name


def patch_debian(file_name):
    if not file_name.endswith('.deb'):
        print('debian 文件名有问题')
        print('debian wrong file name')
        exit()

    with release_workdir():
        file_path = os.path.join(TRANS_RELEASE_FOLDER, file_name)
        print('file_path', file_path)

        # 解包deb
        # extract deb package
        deb_folder = os.path.join(TRANS_RELEASE_FOLDER, 'trilium-deb')
        os.system(f'rm -rf "{deb_folder}"')
        cmd = f'dpkg-deb -R "{file_path}" "{deb_folder}"'
        print('cmd', cmd)
        os.system(cmd)

        if DO_DELETE:
            # 删除复制过来的原始deb包
            # remove the copied original deb package
            os.system(f'rm -f "{file_path}"')

        asar_folder = os.path.join(deb_folder, 'usr/lib/trilium/resources')
        asar_path = os.path.join(asar_folder, 'app.asar')
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

        # 解包目录必须删掉，否则会被一起打进 deb 包
        # remove unpacked files before archiving
        os.system(f'rm -rf "{asar_folder}/app/"')

        # 回到发布目录，避免影响后续打包
        # return to release folder to avoid affecting subsequent packaging
        os.chdir(TRANS_RELEASE_FOLDER)

        # 重新打deb包
        # make deb package
        new_name = add_lang_suffix(file_name)
        print('new_name', new_name)
        new_file_path = os.path.join(TRANS_RELEASE_FOLDER, new_name)
        os.system(f'rm -f "{new_file_path}"')
        cmd = f'dpkg-deb --build --root-owner-group "{deb_folder}" "{new_file_path}"'
        print(cmd)
        os.system(cmd)

        if DO_DELETE:
            os.system(f'rm -rf "{deb_folder}"')

        return new_name


# 包名 -> 处理函数 / 解压后的根目录，集中管理以免遗漏某个端
PACKAGE_PATCHERS = {
    'linux': patch_linux,
    'linux-server': patch_linux_server,
    'linux-server-arm64': patch_linux_server,
    'windows': patch_windows,
    'mac': patch_mac,
    'debian': patch_debian,
}

PACKAGE_ROOT_FOLDERS = {
    'linux': 'trilium-linux-x64',
    'linux-server': 'trilium-linux-x64-server',
    'linux-server-arm64': 'trilium-linux-arm64-server',
    'windows': 'trilium-windows-x64',
    'mac': 'trilium-mac-x64',
    'debian': 'trilium-deb',
}


if __name__ == '__main__':
    print(f'DEBUG is {DEBUG}')
    print('本次打包列表:', PACKAGES)

    unknown = [p for p in PACKAGES if p not in PACKAGE_PATCHERS]
    if unknown:
        raise ValueError(f'未知的打包目标: {unknown}，可选值: {list(PACKAGE_PATCHERS)}')

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

    # 按列表顺序逐个打包。每个端都会重置工作目录、清理自己的临时目录，
    # 所以调换顺序（或者只打包其中几个）不会影响结果。
    built = []
    for package_type in PACKAGES:
        new_name = download_and_patch(releases, package_type)
        if new_name:
            built.append(new_name)

    print('已生成:', built)
    os.system(f'xdg-open {TRANS_RELEASE_FOLDER}')

    print('finished')
