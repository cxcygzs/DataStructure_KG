from flask import request
import pymysql
import math


# 1.注册界面接收信息并传送到数据库里面
def register_function():
    # 接收数据
    user = request.form.get('username')
    pwd = request.form.get('password')
    email = request.form.get('email')
    tel = request.form.get('tel')
    gender = request.form.get('gender')
    birthday = request.form.get('birthday')
    # 和数据库建立连接
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='database1', charset='utf8')
    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root1', password='Root_12root', db='database1',
    #                        charset='utf8')
    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='qroot', db='database1', charset='utf8')

    # 拿到游标
    cursor = conn.cursor()

    hang = cursor.execute('select username from userinfo where username=(%s)', user)
    if hang:
        rows = 0
    else:
        # 执行sql语句
        sql = 'insert into userinfo(username, pwd, email, tel, sex, birthdate) values(%s,%s, %s, %s, %s, %s)'
        rows = cursor.execute(sql, (user, pwd, email, tel, gender, birthday))

    conn.commit()

    # 数据库和游标关闭
    cursor.close()
    conn.close()
    return rows


# 2.登录界面接收数据并和数据库中的信息相匹配
def login_function():
    user = request.form.get('username')
    pwd = request.form.get('pwd')

    # 连接数据库
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='database1', charset='utf8')
    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root1', password='Root_12root', db='database1',
    #                        charset='utf8')
    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='qroot', db='database1', charset='utf8')

    # 拿到游标
    cursor = conn.cursor()

    # 执行sql语句
    sql = 'select * from userinfo where username = %s and pwd=%s'
    rows = cursor.execute(sql, (user, pwd))

    # 数据库和游标关闭
    cursor.close()
    conn.close()
    return rows


# 3.获取mysql里面的数据，展示再个人用户界面
def personal_info_function(username):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='database1', charset='utf8')
    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root1', password='Root_12root', db='database1',
    #                        charset='utf8')
    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='qroot', db='database1', charset='utf8')

    # 拿到游标
    cursor = conn.cursor()

    # 执行sql语句
    sql = 'SELECT * FROM userinfo where username="%s"' % (str(username))
    cursor.execute(sql)
    # u = ((96, 'baipengkun', '123456', '779822892@qq.com', '', '男', '0000-00-00'),)
    u = cursor.fetchall()

    # 数据库和游标关闭
    cursor.close()
    conn.close()
    if not u:
        u = ((id, "未登录,请登录",),)

    return u


# 4.点击下载按钮，即可把图片base64数据传到数据库里面
def up_graph(base, username):
    if username:
        conn = pymysql.connect(host='localhost', user='root', password='123456', db='database1', charset='utf8')
        # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root1', password='Root_12root', db='database1',
        #                        charset='utf8')
        # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='qroot', db='database1', charset='utf8')

        # 拿到游标
        cursor = conn.cursor()
        sql = "INSERT INTO my_graph (data, name, username) VALUES (%s, '{0}', '{1}')".format("graph",
                                                                                             username)  # graph是上传图片的名字

        cursor.execute(sql, base)
        conn.commit()
        cursor.close()
        conn.close()



# 5.获取数据库里面的图片base64码，传到我的图谱界面,展示在前端
def show_graph(user):
    # 连接数据库
    conn = pymysql.connect(host='192.168.117.1', user='root', password='123', db='database1', charset='utf8')
    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root1', password='Root_12root', db='database1',
    #                        charset='utf8')
    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='qroot', db='database1', charset='utf8')
    # 拿到游标
    cursor = conn.cursor()

    # 执行sql语句，利用用户名进行查找，把所有图片base码放到u里
    sql = 'SELECT data FROM my_graph where username="%s"' % (str(user))
    cursor.execute(sql)
    u = cursor.fetchall()

    # 处理数据：把编码的b''去掉，u原始是这种形式(("a",), ("b",), ("c",))，处理u，使之变为(("a","b"), ("c",))
    # base = str(base64, 'utf-8')
    u1 = []
    for i in range(0, math.ceil(len(u) / 2)):
        c = list(u[2 * i])
        c[0] = str(c[0], 'utf-8')
        c = tuple(c)
        try:
            b = list(u[2 * i + 1])
            b[0] = str(b[0], 'utf-8')
            b = tuple(b)
            c = c + b
        except:
            pass
        u1.append(c)
    u2 = tuple(u1)
    # print(u2)

    # 数据库和游标关闭
    cursor.close()
    conn.close()
    # 如果没有登录，就获取不到最上面那个user，就不会执行上面的sql语句，u2就没有得到值
    img1 = ""
    img2 = ""
    if not u2:
        u2 = ((img1, img2),)
    return u2
