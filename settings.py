# 警告! 文件夹的内容可能会被删除, 请确保路径没有重要文件
# WARNING! folders may get deleted during the execution
# make sure the folders not containing anything important!

# 路径结尾的斜杠不能省略
# ending slash in folders can NOT be omitted

import platform

if platform.system() == 'Linux':
    # BASE_PATH 是工作目录
    # BASE_PATH is the working directory
    BASE_FOLDER = '/home/nate/soft/trilium/trilium-trans/'

    # PATCH_FOLDER 是输出补丁的目录
    # PATCH_FOLDER is the output for patch
    PATCH_FOLDER = '/home/nate/soft/trilium/trilium-trans-patch/'

    # TRANS_RELEASE_FOLDER 是翻译好的客户端发布的路径
    # TRANS_RELEASE_FOLDER is the release directory for translated clients
    TRANS_RELEASE_FOLDER = '/home/nate/soft/trilium/trilium-trans-release/'
else:
    # MacOS
    BASE_FOLDER = '/Users/nate/soft/trilium/trilium-trans/'
    PATCH_FOLDER = '/Users/nate/soft/trilium/trilium-trans-patch/'
    TRANS_RELEASE_FOLDER = '/Users/nate/soft/trilium/trilium-trans-release/'


# release文件名后缀
# release file name suffix
LANG = 'cn'

# 翻译者信息, 会在关于页面显示
# translator info, will be in about page
TRANSLATOR = 'Nriver'
TRANSLATOR_URL = 'https://github.com/Nriver/trilium-translation'

# 连不到GitHub需要设置代理 USE_PROXY=False 不会用代理
# Change following proxy setting if you need proxy to connect to GitHub. set USE_PROXY=False can ignore it.
# USE_PROXY = True
USE_PROXY = False
PROXIES = {
    "http": "socks5://127.0.0.1:10808",
    "https": "socks5://127.0.0.1:10808"
}

# 避免兼容性问题，强制使用某个版本的trilium
# To avoid compatibility issue, force to use certain version of trilium
VERSION_INFO_OVERRIDE = True
# 0.47
force_version_info = {
    'name': 'v0.47.8 release',
    'zipball_url': 'https://api.github.com/repos/zadam/trilium/zipball/v0.47.8',
    'browser_download_url': 'https://github.com/zadam/trilium/releases/download/v0.47.8/trilium-linux-x64-0.47.8.tar.xz'
}

force_version_info_full = {
    'name': 'v0.47.8 release',
    'releases': {
        'linux': {'name': 'trilium-linux-x64-0.47.8.tar.xz', 'url': 'https://github.com/zadam/trilium/releases/download/v0.47.8/trilium-linux-x64-0.47.8.tar.xz'},
        'linux-server': {'name': 'trilium-linux-x64-server-0.47.8.tar.xz', 'url': 'https://github.com/zadam/trilium/releases/download/v0.47.8/trilium-linux-x64-server-0.47.8.tar.xz'},
        'mac': {'name': 'trilium-mac-x64-0.47.8.zip', 'url': 'https://github.com/zadam/trilium/releases/download/v0.47.8/trilium-mac-x64-0.47.8.zip'},
        'windows': {'name': 'trilium-windows-x64-0.47.8.zip', 'url': 'https://github.com/zadam/trilium/releases/download/v0.47.8/trilium-windows-x64-0.47.8.zip'}
    }
}
