from settings import BASE_FOLDER, USE_PROXY, PROXIES, VERSION_INFO_OVERRIDE, force_version_info, VERSION_INFO_OVERRIDE_BETA, force_version_info_beta
import os
import re
import shutil
import requests
from zipfile import ZipFile
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# disable warning if use proxy
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

CLIENT_FOLDER = BASE_FOLDER + 'trilium-linux-x64'
REPO_NAME = 'zadam/trilium'
# regex match which file to download if multiple files exists
PREFERRED_RELEASE_NAME_PATTERN = 'trilium-linux-x64-.*?.tar.xz'
SOURCE_CODE_NAME_PATTERN = 'trilium-linux-x64-.*?.tar.xz'

CMD_STOP_SERVICE = """pkill -9 trilium"""

# 是否从GitHub下载文件
# whethere download files from GitHub
DO_DOWNLOAD = True

# 是否删除临时文件
# whethere delete template files
# DO_DELETE = False
DO_DELETE = True


def requests_get(url):
    ret = None
    try:
        ret = requests.get(url, proxies=PROXIES, verify=not USE_PROXY)
    except Exception as e:
        print('If github is not avaliable, you can set USE_PROXY to True and set PROXIES to your proxy.')
        print('Exception', e)
    return ret


def get_latest_version():
    """get latest version info"""
    print('get latest version info')
    url = f'https://api.github.com/repos/{REPO_NAME}/releases/latest'
    print(url)
    res = requests_get(url)
    version_info = {}

    # zipball_url is the source code
    version_info['zipball_url'] = res.json()['zipball_url']

    version_info['name'] = res.json()['name']
    for x in res.json()['assets']:
        if not re.match(PREFERRED_RELEASE_NAME_PATTERN, x['name']):
            continue
        version_info['browser_download_url'] = x['browser_download_url']
        break
    if 'browser_download_url' not in version_info:
        print('Did not find a matching release! Please check file name and modify PREFERRED_RELEASE_NAME_PATTERN.')
        exit()
    print(f'latest version is {version_info["name"]}')
    return version_info


def backup_old_service():
    BACKUP_SUFFIX = '_old'
    backup_dir = CLIENT_FOLDER + BACKUP_SUFFIX
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
    os.mkdir(backup_dir)

    if os.path.exists(CLIENT_FOLDER):
        os.system(f'mv {CLIENT_FOLDER} {CLIENT_FOLDER}{BACKUP_SUFFIX}')
        print(f'old version is moved to {CLIENT_FOLDER}{BACKUP_SUFFIX}')


def download_latest(url, file_name=None):
    """download latest release"""
    print('download latest tarball')
    if not file_name:
        file_name = url.split('/')[-1]

    print('downloading ...')
    if DO_DOWNLOAD:
        with requests.get(url, proxies=PROXIES, verify=False, stream=True) as r:
            r.raise_for_status()
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    print(f'download complete, file saved as {file_name}')
    return file_name


def download_source(url, file_name=None):
    print('download source', url)
    if not file_name:
        file_name = url.split('/')[-1]
    print('downloading ...')
    if DO_DOWNLOAD:
        with requests.get(url, proxies=PROXIES, verify=False, stream=True) as r:
            r.raise_for_status()
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    print(f'download complete, file saved as {file_name}')
    return file_name


def stop_service():
    if CMD_STOP_SERVICE:
        os.system(CMD_STOP_SERVICE)


def clean_cahce():
    os.system('rm -rf ~/.config/Trilium Notes/Cache/')
    os.system('rm -rf ~/.config/Trilium Notes/Code Cache/')
    os.system('rm -rf ~/.config/Trilium Notes/GPUCache/')


def decompress_package(file_name):
    print(f'decompress {file_name}')
    if file_name.endswith('tar.xz'):
        try:
            os.system(f'xz -d {file_name}')
        except:
            pass
        os.system(f'tar -xf {file_name[:-3]}')
        if DO_DELETE:
            os.system(f'rm -f {file_name[:-3]}')


def decompress_source_package(file_name):
    if file_name.endswith('.zip'):
        extracted_folder = ''
        with ZipFile(file_name, 'r') as zip:
            # printing all the contents of the zip file
            extracted_folder = zip.namelist()[0].split('/')[0]
        if extracted_folder:  
            os.system(f'unzip -o {file_name}')
            os.system('pwd')
            if DO_DELETE:
                os.system(f'rm -rf trilium-src.zip')
            print(extracted_folder)
            os.system(f'mv {extracted_folder} trilium-src')


if __name__ == '__main__':
    if os.path.exists(BASE_FOLDER):
        if not (input(f'BASE_FOLDER exists! DELETE {BASE_FOLDER}, continue?(y)')).lower() in ['y', 'yes']:
            exit()
        os.system(f'rm -rf {BASE_FOLDER}')
    os.makedirs(BASE_FOLDER)
    print('BASE_FOLDER', BASE_FOLDER)
    os.chdir(BASE_FOLDER)

    if VERSION_INFO_OVERRIDE:
        if VERSION_INFO_OVERRIDE_BETA:
            version_info = force_version_info_beta
        else:
            version_info = force_version_info
    else:
        version_info = get_latest_version()

    print(version_info)
    stop_service()

    # 翻译不生效可以尝试删除缓存
    # If the translation doesn't work, clean the cache files may help
    clean_cahce()
    # backup_old_service()

    # 下载release
    # get release file
    file_name = download_latest(version_info['browser_download_url'])
    print(f'file_name {file_name}')
    decompress_package(file_name)

    # 下载源码
    # get source code
    file_name = download_source(version_info['zipball_url'], 'trilium-src.zip')
    file_name = 'trilium-src.zip'
    print(f'file_name {file_name}')
    decompress_source_package(file_name)

    print('finished!')
