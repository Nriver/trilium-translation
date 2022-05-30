# Trilium Translation
我把这个牛逼的笔记软件[Trilium Notes](https://github.com/zadam/trilium)做了中文翻译. 翻译会持续跟进Trilium Notes的稳定版.

如果你想把Trilium翻译成其它语言，可以参考[这里](https://github.com/Nriver/trilium-translation/blob/main/README_CN.md#%E5%A4%AA%E9%95%BF-%E5%88%AB%E7%9C%8B-%E8%87%AA%E5%B7%B1%E7%BC%96%E8%AF%91)

如果你觉得不错, 可以留下一个star, 谢谢 ^_^

如果你是老用户, 使用前最好备份数据以防万一.

<a href="https://count.getloli.com"><img align="center" src="https://count.getloli.com/get/@Nriver_trilium-translation"></a><br>

Trilium Notes 交流qq群 686232370

![image](https://user-images.githubusercontent.com/6752679/125550117-ec2a118c-8628-46e4-99f4-7f7e12ba7ba6.png)


# 目录导航
<!--ts-->
* [Trilium Translation](#trilium-translation)
* [目录导航](#目录导航)
* [关于汉化版的内置文档](#关于汉化版的内置文档)
* [界面截图](#界面截图)
* [使用方法](#使用方法)
* [在Docker里运行服务端](#在docker里运行服务端)
* [更新版本](#更新版本)
   * [Docker服务端版本更新](#docker服务端版本更新)
   * [其它版本更新](#其它版本更新)
   * [(太长, 别看) 自己编译](#太长-别看-自己编译)
      * [翻译原理](#翻译原理)
      * [编译环境](#编译环境)
      * [翻译过程](#翻译过程)
      * [没翻译到的文字](#没翻译到的文字)
* [注意事项](#注意事项)
   * [数据同步](#数据同步)
* [常见问题](#常见问题)
   * [笔记数据库在哪?](#笔记数据库在哪)
   * [如何修改数据库位置？](#如何修改数据库位置)
   * [为什么用中文版的自带文档还是英文的?](#为什么用中文版的自带文档还是英文的)
   * [为什么程序打不开?](#为什么程序打不开)
   * [为什么程序打开之后是空白一片?](#为什么程序打开之后是空白一片)
   * [日记笔记跑到别的目录下了](#日记笔记跑到别的目录下了)
   * [为什么我的docker镜像更新之后还是旧版的?](#为什么我的docker镜像更新之后还是旧版的)
   * [为什么trilium-portable.bat提示禁止执行?](#为什么trilium-portablebat提示禁止执行)
* [0.47 升级到 0.48 的一些问题](#047-升级到-048-的一些问题)
   * [前端js报错](#前端js报错)
   * [第三方主题不生效](#第三方主题不生效)
   * [初始化慢，同步数据慢](#初始化慢同步数据慢)
* [关于本项目使用的字体](#关于本项目使用的字体)
* [限制](#限制)
* [Stargazers 数据](#stargazers-数据)
* [捐赠](#捐赠)
* [感谢](#感谢)
<!--te-->

# 关于汉化版的内置文档
内置的文档有做汉化，不过我做了些修改，删掉了一些我认为用处不大的内容。比如Trilium自带有TODO，所以我把不太好用的任务管理删了。另外增加了一些实用的示例，比如自定义api接口等。

原版的示例没有仔细分类，有些内容又在英文wiki上，我第一次看觉得一头雾水。所以我修改了示例文档的笔记结构，给不同功能的笔记进行分类。

里面的内容完全按照我个人口味添加，你可以随意修改。但是请注意！千万不要随意修改`日记`笔记的结构和笔记属性，你想移动可以移走整个日记笔记。不要动里面的结构，不然这个功能很容易被玩坏，所以除非你知道你在做什么，别去动这个笔记的结构！

# 界面截图

原版的黑暗主题

![dark](docs/screenshot_theme_dark.png)

原版的明亮主题

![light](docs/screenshot_theme_light.png)

我做的Nier主题 :)

![nier](docs/screenshot_theme_nier.png)

# 使用方法
1. [Release](https://github.com/Nriver/trilium-translation/releases)里下载对应客户端
2. 解压运行(Linux桌面运行trilium, Linux服务端运行trilium.sh, Windows 运行trilium.exe, macOS 运行trilium.app, ).
3. 玩去吧 :)

---
# 在Docker里运行服务端
Trilium Notes的服务端可以用我构建好的docker镜像运行. 注意！请不要使用加速镜像，可以避免类似 #16, #14 的问题.

直接下载 [docker-compose.yml](https://raw.githubusercontent.com/Nriver/trilium-translation/main/docker-compose.yml).

下载docker-compose配置文件
```
wget https://raw.githubusercontent.com/Nriver/trilium-translation/main/docker-compose.yml
```

运行
```
docker-compose up -d
```

它会从[Docker Hub](https://hub.docker.com/repository/docker/nriver/trilium-cn)直接拉镜像运行.

浏览器打开 http://127.0.0.1:8080 访问服务端.

笔记数据会在 docker-compose.yml 同目录下

(docker镜像存了一个0.47.5的旧版本备份，需要的可以自己拿)


# 更新版本
注意Trilium更新需要同时更新服务端与客户端, 版本必须一致. 更新前以防万一请备份好数据.

## Docker服务端版本更新
cd到docker-compose.yml所在目录

先停止trilium
```
docker-compose down
```

拉取最新镜像
```
docker-compose pull
```

运行
```
docker-compose up -d
```

## 其它版本更新
直接去[Release](https://github.com/Nriver/trilium-translation/releases)里下载对应最新版客户端


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
4. 运行 `python3 trans.py` 来生成翻译补丁.
4. 运行 `python3 make_release.py` 来发布翻译后的程序.

注意: `translations.py` 有一些开头和结尾引号是用来做正则匹配的, 翻译的时候别删了. 有些类似 '${xxxx}' 的字符串是 Trilium Notes 的占位符, 别动它们.

### 没翻译到的文字
参考 `trans.py` 写的, 用双花括号 '{{}}' 把要翻译的文字括起来.

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

docker 在docker-compose.yml同目录的`trilium-data`文件夹里

## 如何修改数据库位置？
可以参考客户端自带的`trilium-portable.sh`或者`trilium-portable.bat`以绿色版的方式运行。改数据库位置只要修改文件里的数据库路径即可。

如果你想体验原版最新的特性，建议使用这种方式运行。

## 为什么用中文版的自带文档还是英文的?
你运行过原版的Trilium程序, 你的笔记数据库已经按照英文的文档初始化过了。想要中文文档可以直接把项目中的demo-cn.zip导入到笔记中，或者删掉旧数据库(数据自行备份)，用中文版启动，重新进行初始化。

## 为什么程序打不开?
低版本的Trilium无法打开高版本的Trilium创建的数据，会导致程序无法启动。我发布中文版程序不会跟着原版每个版本都更新，版本号肯定是滞后的。

## 为什么程序打开之后是空白一片?
可能是GPU驱动不兼容，请尝试关闭gpu加速。增加启动运行参数，使用 `trilium --disable-gpu` 来启动。


## 日记笔记跑到别的目录下了
如果你创建日记笔记的时候笔记跑到别的地方去了，可以在`日记`这个笔记里加一个 `#calendarRoot` 的属性，再把错位的日记手动移到正常的笔记位置就行。如果还是不行，请手动搜索有没有其它笔记有 `#calendarRoot`，如果有就请删掉。  

## 为什么我的docker镜像更新之后还是旧版的?
目前我也不太清楚正确的解决办法, 只能有这几点建议:  
1. 不用国内的加速镜像, 它们的数据有可能不是最新的. 去掉加速镜像后再尝试pull.
2. (危险操作, 注意) 停掉trilium, 使用 `docker system prune -a` 来清理掉所有没有在使用的docker镜像和容器等再重新pull.

## 为什么`trilium-portable.bat`提示禁止执行?
0.50之后的windows客户端的portable模式改成了用powershell运行, 部分电脑上可能默认不允许运行`.ps1`格式的文件. 可以尝试在命令行输入以下命令解除限制. 请一行一行地执行.

```
powershell
set-executionpolicy remotesigned
```

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
# 关于本项目使用的字体

本项目使用的字体文件为免费字体.

`font/muyao-shouxie.ttf` 沐瑶随心手写体来自 [这里](https://www.maoken.com/freefonts/1323.html)
`font/muyao-softbrush.ttf` 沐瑶软笔手写体 [这里](https://www.maoken.com/freefonts/1309.html)

感谢 [https://www.zcool.com.cn/u/402511](https://www.zcool.com.cn/u/402511) 发布的这两款免费字体！

---
# 限制
Trilium Notes的文字是硬编码的, 所以没法切换语言.
翻译是修改代码, 如果把代码改坏了, 你的数据有可能丢失, 所以做好备份.

如果真改坏了, Trilium Notes启动不了, 或者翻译错了, 就要用`init.py`重新下载Trilium Notes.

---
# Stargazers 数据

统计图使用 [caarlos0/starcharts](https://github.com/caarlos0/starcharts) 项目生成.

[![Stargazers over time](https://starchart.cc/Nriver/trilium-translation.svg)](https://starchart.cc/Nriver/trilium-translation)

---
# 捐赠
如果你觉得我做的翻译对你有帮助, 欢迎捐赠, 这对我来说是莫大的鼓励!

支付宝:  
![Alipay](docs/alipay.png)

微信:  
![Wechat Pay](docs/wechat_pay.png)


---
# 感谢
你们的支持, 让我充满了决心.

感谢 `tr**one` 赞助的20元!

感谢 `1*0` 赞助的8元的蜜雪冰城!

感谢 `**钧` 赞助的38元的咖啡!

感谢 `*风` 赞助的25元!

感谢 `**进` 赞助的25元!

感谢 `**甜` 赞助的18元!

感谢Jetbrins公司提供的Pycharm编辑器!

[![Jetbrains](docs/jetbrains.svg)](https://jb.gg/OpenSource)
