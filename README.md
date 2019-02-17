# AdultScraper.bundle
Plex Agent plug-in

# AdultScraper功能
1、日本-自动搜刮
2、日本-手动搜刮列表选择

# AdultScraper挂取信息
1、番号
2、标题
3、介绍
4、导演
5、演播室
6、类别
7、系列（支持隐藏合并）
8、演员（可头像显示）
9、海报

# AdultScraper安装
1、群晖下 python 2.7
plex 自带python2.7 所以下面安装pip时候请指定安装路径

2、pip 安装扩展包
将扩展包安装到 plex自带python2.7的site-packages目录下
包路径
/volume1/@appstore/"Plex Media Server"/Resources/Python/lib/python2.7/site-packages
安装时须使用--target=指定包路径

pip install --target=path packagename

实例
pip install --target=/volume1/@appstore/"Plex Media Server"/Resources/Python/lib/python2.7/site-packages lxml

3、所需要扩展包有
Pillow
requests
lxml

4、php设置
需要打开gd库
设置方式
web station - > PHP设置 -> 选择5.6 -> 在下面的扩展名列表中 勾选 gd库  

5、imagetool\index.php
使用web station 架设起来 
输入IP+端口 出现黑色页面表示架设成功并可以正常运行

# AdultScraper设置
1、必填* index.php 路径: 以http开头：
表示需要输入你刚才web station架设的imagetool\index.php页面路径
默认实例是http://192.168.X.XX:XXX需要修改

2、裁切像素
默认423
也可根据需要调整

3、封面宽
默认800
也可根据需要调整

4、封面高
默认538
也可根据需要调整

5、使用日本数据源（为后续加入欧美搜刮所使用的判断预留）
必须勾选否则无法使用！

6、日本标题样式
默认番号
设置标题样式
番号
标题
番号+标题

# AdultScraper使用
1、视频源文件命名规范 xxx-000.mp4或xxx 000.mp4 严禁出现其他字符

2、同片多版本或多CD的命名方法 xxx-000.cd1.mp4 、 xxx-000-cd2.mp4
注意.cd1与-cd2

3、添加资料库后会开始自动扫描所有新库片源

4、扫描完成后会出现无法找到的片源可以手动模式扫描 手动模式寻找的数据源是不一样的
