# AdultScraper.bundle
Plex Agent plug-in

# AdultScraper功能
- 日本-自动搜刮
- 日本-手动搜刮列表选择

# AdultScraper挂取信息
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
## 群晖下 python 2.7
plex 自带python2.7 所以下面安装扩展包时 pip 请指定安装路径

## pip 安装扩展包
- 将扩展包安装到 plex自带python2.7的site-packages目录下
- 包路径 /volume1/@appstore/"Plex Media Server"/Resources/Python/lib/python2.7/site-packages
- 安装时须使用--target=指定包路径
pip install --target=path packagename
## 实例
- pip install --target=/volume1/@appstore/"Plex Media Server"/Resources/Python/lib/python2.7/site-packages lxml

## 所需要扩展包有
- Pillow
- requests
- lxml
## php设置
- 需要打开gd库
### 设置方式
- web station - > PHP设置 -> 选择5.6 -> 在下面的扩展名列表中 勾选 gd库  
### imagetool\index.php
使用web station 架设起来 
输入IP+端口 出现黑色页面表示架设成功并可以正常运行

# AdultScraper设置
## 必填* index.php 路径: 以http开头：
表示需要输入你刚才web station架设的imagetool\index.php页面路径
默认实例是http://192.168.X.XX:XXX需要修改

## 裁切像素
默认：423
也可根据需要调整

## 封面宽
默认：800
也可根据需要调整

## 封面高
默认：538
也可根据需要调整

## 使用日本数据源（为后续加入欧美搜刮所使用的判断预留）
必须勾选否则无法使用！

## 日本标题样式
默认：番号

# AdultScraper使用
- 视频源文件命名规范 xxx-000.mp4或xxx 000.mp4 严禁出现其他字符

- 同片多版本或多CD的命名方法 xxx-000.cd1.mp4 、 xxx-000-cd2.mp4
- 注意.cd1与-cd2

- 添加资料库后会开始自动扫描所有新库片源

- 扫描完成后会出现无法找到的片源可以手动模式扫描 手动模式寻找的数据源是不一样的
