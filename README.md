# DataStructure_KG
数据结构知识图谱
项目来源https://github.com/cxcygzs/DataStructure_KG

## 文件树：
1) app.py是整个系统的主入口
2) templates文件夹是HTML的页面
     |-first.html 欢迎界面
     |-index.html 系统主界面
     |-search.html 搜索知识点
     |-all_relation.html 知识图谱全貌展示
     |-KGQA.html 智能问答页面
     |-part文件夹的html是小结图谱界面
3) static文件夹存放css和js，是页面的样式和效果的文件
4) raw_data文件夹是存在数据处理后的三元组文件
5) neo_db文件夹是知识图谱构建模块
     |-config.py 配置参数
     |-create_graph.py 创建知识图谱，图数据库的建立
     |-query_graph.py 知识图谱的查询
6) KGQA文件夹是问答系统模块
     |-ltp.py 分词、词性标注、命名实体识别
7) spider文件夹是爬虫模块
     |- get_*.py 是之前爬取的代码，已经产生好images和json 可以不用再执行
     |-show_profile.py 是调用爬虫信息和图谱展示在前端的代码
8) test文件夹为测试代码

## 数据处理
1. kg_data/relation.csv与cate.csv为手工构建最原始数据
2. 执行data_processing.py进行数据处理
    - col_to_dic() 将cate.csv按列类别生成字典，返回data_dict
    - add_cate(data_dict) 添加概念级别,并保存到raw_data/relation.csv
    - get_json_data() 将raw_data/relation.csv的数据转换成data link的json格式保存到（static/data.json)以便前端展示
2. 执行creat_graph.py创建图数据库,数据来自raw_data/relation.csv
4. 执行get_ds.py爬虫得到百度百科词条和图片（spider/json/data.json)(spider/images)
5. 执行get_dict.py得到自定义词典，在进行分词的时候，自定义词典里的词不会被分开
6. creat_graph.py 新增 添加数据属性到图数据库
> 上面步骤只需运行一次

## 部署步骤
* 0.下载完成后, 解压项目,用PyCharm打开,使用python 3.8版本
* 1.在终端执行 
  ```python
  pip install -r requirement.txt 
  ```
安装所需要的库
* 2.下载 [neo4j图数据库]( https://blog.csdn.net/littlexmj/article/details/119458370), 根据安装教程安装,我安装的是Neo4j Desktop,安装完成后,打开主界面, 点击左上方的 New , 创建一个新的数据库项目, 点击Add, 选择 Local DBMS 并将其命名为**neo4j**, 密码设置成**12345678**.
* 3.点击 Start 运行数据库, 在浏览器中打开http://localhost:7474/, 查看是否正常运行
* 4.找到到 neo_db 目录下的create_graph.py文件,运行它来建立知识图谱
* 5.下载[mysql数据库]( https://blog.csdn.net/maoziyang1996/article/details/85334935) ,根据安装教程安装,我安装的是8.0.26版本,安装完成后,在命令提示窗口输入 mysql -u root -p,然后输入安装时自己设置的密码,进入mysql,然后输入 source 路径（路径指的是你存放computer.sql文件的位置,例如我的路径是D:/大二学习\计算机专业课程教育知识图谱/KG_computer9.0/KG_computer9.0/computer.sql),如果设置的用户名不是root,密码不是123456,需要在mysql_db的文件夹里修改配置参数
* 6.直接运行根目录下的 app.py , 打开 http://127.0.0.1:8000/ (如果报错:OSError: [WinError 10013] 以一种访问权限不允许的方式做了一个访问套接字的尝试,可以尝试修改app.py文件里主函数里的app.run()里面的port参数,可以修改为port=8001等)
