# Trilium Translation
我把这个牛逼的笔记软件[Trilium Notes](https://github.com/zadam/trilium)做了中文翻译.

如果你想把Trilium翻译成其它语言，可以参考[这里](https://github.com/Nriver/trilium-translation/blob/main/README_CN.md#%E5%A4%AA%E9%95%BF-%E5%88%AB%E7%9C%8B-%E8%87%AA%E5%B7%B1%E7%BC%96%E8%AF%91)

如果你觉得不错, 可以留下一个star, 谢谢 ^_^

如果你是老用户, 使用前最好备份数据以防万一.

![20210606135851579_1868988429](https://user-images.githubusercontent.com/6752679/120914251-65009900-c6cf-11eb-9b38-dd9554657372.png)


Trilium Notes 交流qq群 686232370

![image](https://user-images.githubusercontent.com/6752679/125550117-ec2a118c-8628-46e4-99f4-7f7e12ba7ba6.png)

# 关于汉化版的内置文档
内置的文档有做汉化，不过我做了些修改，删掉了一些我认为用处不大的内容。比如Trilium自带有TODO，所以我把不太好用的任务管理删了。另外增加了一些实用的示例，比如自定义api接口等。

原版的示例没有仔细分类，有些内容又在英文wiki上，我第一次看觉得一头雾水。所以我修改了示例文档的笔记结构，给不同功能的笔记进行分类。

里面的内容完全按照我个人口味添加，你可以随意修改。但是请注意！千万不要随意修改`日记`笔记的结构和笔记属性，你想移动可以移走整个日记笔记。不要动里面的结构，不然这个功能很容易被玩坏，所以除非你知道你在做什么，别去动这个笔记的结构！

# 使用方法
1. [Release](https://github.com/Nriver/trilium-translation/releases)里下载对应客户端
2. 解压运行(Linux桌面运行trilium, Linux服务端运行trilium.sh, Windows 运行trilium.exe, macOS 运行trilium.app, ).
3. 玩去吧 :)

---
# 在Docker里运行服务端
Trilium Notes的服务端可以用我构建好的docker镜像运行. 直接下载 [docker-compose.yml](https://github.com/Nriver/trilium-translation/blob/main/docker-compose.yml).
运行
```
docker-compose up -d
```

它会从[Docker Hub](https://hub.docker.com/repository/docker/nriver/trilium-cn)直接拉镜像运行.

浏览器打开 http://127.0.0.1:8080 访问服务端.

笔记数据会在 docker-compose.yml 同目录下

(docker镜像存了一个0.47.5的旧版本备份，需要的可以自己拿)

## (太长, 别看) 自己编译
如果你想自己检查代码(代码都有中英双语注释)再自己编译, 可以看看下面的东西.

警告! 代码里有'rm -rf'相关命令, 胡乱修改代码可能会删除你的文件, 请小心使用.

### 翻译原理
从Trilium Notes官方的Release下载Linux包和源码, 用正则替换掉里面的界面文字再编译打包回去.


### 编译环境
我用Manjaro(Linux)/macOS, 你想改成其它环境只要修改一下代码理论上也没问题.

Python3 和以下模块
```
pip3 install requests --user
```

Nodejs 和以下模块
```
npm install -g asar
npm install -g webpack
npm install -g webpack-cli
```

7z命令用来打包

### 翻译过程
1. 根据注释修改 `settings.py` 里的配置.
2. 翻译 `translations.py`. (参照 `translations_cn.py`. 大概有一千多行要翻译, 耐心点 :) )
3. 运行 `python3 init.py` 来下载最新的 Trilium Notes.
4. 运行 `python3 trilium_trans.py` 来生成翻译补丁.
4. 运行 `python3 make_release.py` 来发布翻译后的程序.

注意: `translations.py` 有一些开头和结尾引号是用来做正则匹配的, 翻译的时候别删了. 有些类似 '${xxxx}' 的字符串是 Trilium Notes 的占位符, 别动它们.

### 没翻译到的文字
参考 `trilium_trans.py` 写的, 用双花括号 '{{}}' 把要翻译的文字括起来.

把双括号里面的东西放到 `translations.py` 来做翻译. (要避免有些用花括号`}`结尾的文字, 可以把类似 `${xxx}}}'` 的改成`${xxx}'}}` )

---
# 注意事项
使用Trilium Notes需要注意的一些事项

## 数据同步
不能使用第三方同步工具, 比如 OneDrive 等网盘服务, 你辛苦整理的笔记数据库会被这些工具弄坏的. 如果要在多台电脑上同步Trilium Note的笔记数据, 需要自行建立 Trilium Notes 服务端, 让 Trilium 来处理同步, 这是目前唯一受支持的同步方式.


# 常见问题
下面是一些我觉得有代表性的问题

## 笔记数据库在哪?
默认路径

win C:\Users\用户名\AppData\Roaming\trilium-data

linux /home/用户名/.local/share/trilium-data

mac /Users/用户名/Library/ApplicationSupport/trilium-data

## 如何修改数据库位置？
可以参考客户端自带的`trilium-portable.sh`或者`trilium-portable.bat`以绿色版的方式运行。改数据库位置只要修改文件里的数据库路径即可。

如果你想体验原版最新的特性，建议使用这种方式运行。

## 为什么用中文版的自带文档还是英文的?
你运行过原版的Trilium程序, 你的笔记数据库已经按照英文的文档初始化过了。想要中文文档可以直接把项目中的demo-cn.zip导入到笔记中，或者删掉旧数据库(数据自行备份)，用中文版启动，重新进行初始化。

## 为什么程序打不开?
低版本的Trilium无法打开高版本的Trilium创建的数据，会导致程序无法启动。我发布中文版程序不会跟着原版每个版本都更新，版本号肯定是滞后的。

---
# 0.47 升级到 0.48 的一些问题
首先要说，追求稳定的话，不建议升级，因为改动很大，潜在问题比较多。

## 前端js报错
原版程序变化很大，有一些api改变了，如果是从旧版本升级上来的，js代码有些不兼容。

大部分js问题加个 async 就能解决

比如
```
const notes = await api.runOnBackend(() => {
```
改成
```
const notes = await api.runOnBackend(async () => {
```

## 第三方主题不生效
前端变化太大，旧的第三方主题基本全部失效，先用内置的主题吧。

## 初始化慢，同步数据慢
如果是第一次启动0.48，可能会卡在初始化那个页面，等个几秒钟直接把程序关了再打开就行。
如果是0.47升级上来，同步数据可能会特别慢。尝试直接把客户端的数据库移走，重新初始化客户端数据会快一点。


---
# 限制
Trilium Notes的文字是硬编码的, 所以没法切换语言.
翻译是修改代码, 如果把代码改坏了, 你的数据有可能丢失, 所以做好备份.

如果真改坏了, Trilium Notes启动不了, 或者翻译错了, 就要用`init.py`重新下载Trilium Notes.

---
# 感谢

[![Jetbrains](docs/jetbrains.svg)](https://jb.gg/OpenSource)
