# Trilium Translation
[中文说明](README_CN.md)
This repo provides a translation for the awesome [Trilium Notes](https://github.com/zadam/trilium).
Currently, I have translated Trilium Notes into Chinese. Tested with trilium version 0.47.2 - 0.48.7.

Star this repo if you like it, thx :)

If you have old data, PLEASE BACK UP YOUR DATA BEFORE USE.

![20210606135851579_1868988429](https://user-images.githubusercontent.com/6752679/120914251-65009900-c6cf-11eb-9b38-dd9554657372.png)

---
# How to use
1. Download from the latest [Release](https://github.com/Nriver/trilium-translation/releases) that suit your computer system.
2. Unzip and execute(trilium for Linux, trilium.sh for Linux server, trilium.exe for Windows, trilium.app for macOS).
3. Enjoy :)

# How to run server with docker
For Trilium Notes server, you can download my [docker-compose.yml](https://github.com/Nriver/trilium-translation/blob/main/docker-compose.yml)
Then run it with docker simply by executing:
```
docker-compose up -d
```

It will download the Chinese version of Trilium I built on [Docker Hub](https://hub.docker.com/repository/docker/nriver/trilium-cn).

Open http://127.0.0.1:8080 in your browser to access the server page.

Your note data will be in the same directory of the docker-compose.yml file.

---
# How to translate
If you would like to check the code (my codes comes with Chinese and English comments, check it) and compile it by yourself. Here is some information may be useful.

WARNING! The scripts I wrote includes some 'rm -rf' commands, modify and use codes with care!

## How does the translation work
It extracts the resource files from the latest Trilium Notes official release and use regular expression to replace UI text for each file. Then pack the translated files back into the package. Done.


### Compile Environment Requirement
My environment is Manjaro(Linux)/macOS based, but you can make some change to work on other platform. You need to change some path configuration in my code to work on your machine.

Python3 with module
```
pip3 install requests --user
```

Nodejs with module
```
npm install -g asar
npm install -g webpack
npm install -g webpack-cli
```

7z if you want to make release

### Translate Process
1. Modify configurations in `settings.py` by the comments.
2. Do translate in `translations.py`. (See `translations_cn.py`. There are over 1000 lines to translate, be patient :) )
3. Run `python3 init.py` to download latest Trilium Notes.
4. Run `python3 trilium_trans.py` to make a translation patch.
4. Run `python3 make_release.py` to apply patch to releases for all platforms.

Note: In `translations.py` there are some texts begin or ends with quotes were made on purpose for regex match, do not remove them in your translation. There are some text like '${xxxx}' in the translation, these are the placeholder in the original Trilium Notes source code, do not modify them unless you know what you are doing.

### More text to translate
If you'd like to translate more text, mark each text in the file that you want to translate with double brackets`{{}}` like I did in `trilium_trans.py`.

Put everything between double brackets into the dict in `translations.py` and translate to the language you like. (Some text were ended with `}`. Try to avoid triple brackets by change from `${xxx}}}'` to something like `${xxx}'}}` )

---
# Limitations
The translation is hard-coded in the frontend/backend source code, so you can not switch between languages.
If there were some mistakes in the translation, Trilium Notes may not function correctly. Therefore, please back up your data before use.

If you break Trilium Notes somehow, you need to redownload everything with `init.py`.

---
# Thanks

[![Jetbrains](docs/jetbrains.svg)](https://jb.gg/OpenSource)
