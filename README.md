# python爬取InterfaceLIFT壁纸，下载到本地，数据存入数据库（mysql，mongodb）

## 适用pythopn版本

- [Python 2.7](https://www.python.org/downloads/) or [Python 3.6](https://www.python.org/downloads/)
- 只在这两个版本之下测试过，正常运行

## 项目文件说明
- main.py 主要文件
- mysql_orm.py mysql数据库ORM,封装数据的增删改查
- py_pymongo.py 封装mongodb数据的增删改查
- requirements.txt 项目依赖库

## 安装依赖库
```
pip install requirements.txt
```
## 使用
```
python main.py [-d DEST] [-t THREADS] [-o] [resolution]
```

如果没有指定,默认参数使用:

- Resolution: `1920x1080`
- Destination Directory: `./wallpapers`
- Threads: `4`
- Overwrite: `disabled`

列出可用的参数:
```
python main.py --list
```

显示帮助信息:

```
python main.py -h
```

### 使用案例

下载 `1920x1080` 分辨率的壁纸到 `./wallpapers` 文件夹:

```
python main.py 1920x1080
```

下载 `1600x900` 分辨率的壁纸使用 `8` 进程:

```
python main.py -t 8 1600x900
```

下载 `1600x900` 分辨率的壁纸到 `./wallpapers/1600x900` 文件夹:

```
python main.py -d "wallpapers/1600x900" 1600x900
```


参考文章

[SQLAlchemy入门和进阶](https://zhuanlan.zhihu.com/p/27400862)

[SQLAlchemy 教程 —— 基础入门篇](https://www.cnblogs.com/mrchige/p/6389588.html)

[SQLAlchemy技术文档（中文版）]( https://blog.csdn.net/Lotfee/article/details/57406450)

[Pymongo 3.03中文文档(翻译)](http://pengfei.ga/pymongo-3-03wen-dang-fan-yi/)

[PyMongo官方文档翻译](https://www.cnblogs.com/zhouxuchen/p/5544227.html)

[interfacelift-downloader](https://github.com/benjaminheng/interfacelift-downloader)