# AdultScraper.bundle
- 插件使用python2.7编写 尽可能的遵照了pep8规范。
- 这是第一次使用python语言并编写插件，插件未经过非常严格的逻辑与异常处理使用时请先做测试。
- 如发现逻辑性问题与BUG请告知，时间与条件允许时会尽可能的去解决。
- 也希望各位高手能够对插件进行修改并相互交流。

# AdultScraper功能
- 日本-自动搜刮
- 日本-手动搜刮列表选择

# AdultScraper搜刮信息
- 番号
- 标题
- 介绍
- 导演
- 演播室
- 类别
- 系列（支持隐藏合并）
- 演员（可头像显示）
- 海报

# AdultScraper安装
下载解压后删除文件名-master的部分
## 插件安装路径
- AdultScraper.bundle 复制到 Plug-ins 目录下
### Synology安装路径
- /Plex/Library/Application Support/Plex Media Server/Plug-ins
### Linux
- 安装的位置 .......Plex Media Server/Plug-ins
### Windows
- 安装的位置 .......Plex Media Server/Plug-ins

## PLEX服务端
- 自带python2.7 所以下面安装python扩展包时 pip 请指定安装路径

## pip 安装扩展包
- 将扩展包安装到 plex自带python2.7的site-packages目录下
- 安装时须使用--target=指定包路径
- pip install --target=path packagename
### 以Synology为例
- 包路径 /volume1/@appstore/"Plex Media Server"/Resources/Python/lib/python2.7/site-packages
- pip install --target=/volume1/@appstore/"Plex Media Server"/Resources/Python/lib/python2.7/site-packages lxml

## Python 所需要扩展包有
- Pillow
- requests
- lxml
## php设置
- 需要打开gd库
#### 以群晖为例
- web station - > PHP设置 -> 选择5.6 -> 在下面的扩展名列表中 勾选 gd库  

## 海报剪切工具（imagetool\index.php）
### Synology
- 使用web station + php5.6 架设起来 
输入IP+端口 出现黑色页面表示架设成功并可以正常运行
#### linux
- 使用nginx或其他 + php5.6  架设起来 
- 输入IP+端口 出现黑色页面表示架设成功并可以正常运行
#### windows
- 使用WampServer 或其他 架设起来
- 输入IP+端口 出现黑色页面表示架设成功并可以正常运行

# AdultScraper设置
## 必填* index.php 路径: 以http开头：
- 表示需要输入你刚才web station架设的imagetool\index.php页面路径
- 默认实例是http://192.168.X.XX:XXX需要修改

## 裁切像素
- 默认：423
- 也可根据需要调整

## 封面宽
- 默认：800
- 也可根据需要调整

## 封面高
- 默认：538
- 也可根据需要调整

## 使用日本数据源（为后续加入欧美搜刮所使用的判断预留）
- 必须勾选否则无法使用！

## 日本标题样式
- 默认：番号

# AdultScraper使用
- 视频源文件命名规范 xxx-000.mp4或xxx 000.mp4 严禁出现其他字符

- 同片多版本或多CD的命名方法 xxx-000.cd1.mp4 、 xxx-000-cd2.mp4以此类推
- 注意.cd1与-cd2

- 添加资料库后会开始自动扫描所有新库片源

- 扫描完成后会出现无法找到的片源可以手动模式扫描 手动模式寻找的数据源是不一样的
