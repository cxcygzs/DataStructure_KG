from flask import Flask, render_template, request, jsonify, make_response, redirect, session
from neo_db.query_graph import *
from KGQA.ltp import get_target_array, get_fuzzy_array, seg_word, seg_word_flag
from neo_db.update import update_node, add_node, delete_node
from kg_data.data_processing import get_data_num
from kg_data.data_show import get_train_data_list
from mysql_db.data_show import cate_rel_show, operation
from mysql_db import login
from werkzeug.utils import secure_filename
from flask_session import Session
import numpy as np
import pandas as pd
import csv
import os
import datetime
import json
import pymysql


app = Flask(__name__)
# app.config['SECRET_KEY'] = os.urandom(24)
app.secret_key = 'beifang changjian de keke ....'


@app.route('/', methods=['GET', 'POST'])
# @app.route('/index', methods=['GET', 'POST'])
def first(name=None):
    return render_template('first.html', name=name)


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/search.html', methods=['GET', 'POST'])
def search():
    return render_template('search.html')


@app.route('/KGQA.html', methods=['GET', 'POST'])
def KGQA():
    return render_template('KGQA.html')


@app.route('/get_profile', methods=['GET', 'POST'])
def get_profile():
    name = request.args.get('character_name')
    json_data = get_answer_profile(name)
    return jsonify(json_data)


# all_relation.html所使用
@app.route('/get_all_profile', methods=['GET', 'POST'])
def get_all_profile():
    name = request.args.get('character_name')
    # cate = request.args.get('cate')
    json_data = get_answer_all_profile(name)
    return jsonify(json_data)


@app.route('/all_node', methods=['GET', 'POST'])
def all_node():
    show_node_number = request.args.get('number')
    # print('show_node_number=', show_node_number, type(show_node_number))
    if show_node_number:
        show_node_number = int(int(show_node_number) / 1.2)
    else:
        show_node_number = 300

    # print ("number=" + str(show_node_number) )
    json_data, name_dict = all(str(show_node_number))
    # session['name_dict'] = name_dict
    # print(session['name_dict'])
    return jsonify(json_data)


@app.route('/search_a_node', methods=['GET', 'POST'])
def search_a_node():
    # name = request.args.get('name')
    # id = session.get('name_dict')[name]
    # json_data = {'id': id}
    name = request.args.get('name')
    json_data = search_aNode(name)
    return jsonify(json_data)


@app.route('/KGQA_answer', methods=['GET', 'POST'])
def KGQA_answer():
    question = request.args.get('name')
    target_array = get_target_array(str(question))
    if len(target_array) == 1:
        json_data = query(str(target_array[0]))
    elif len(target_array) == 0:
        json_data = query(question)
    else:
        json_data = get_KGQA_answer(target_array)
    return jsonify(json_data)


@app.route('/KGQA_fuzzy', methods=['GET', 'POST'])
def KGQA_fuzzy():
    question = request.args.get('name')
    target_array = get_fuzzy_array(question)
    # print(f"tar {target_array}")
    json_data = fuzzy_search(target_array)
    # print(f"js {json_data}")
    return jsonify(json_data)


# 知识点检索
@app.route('/search_name', methods=['GET', 'POST'])
def search_name():
    name = request.args.get('name')
    json_data = query(str(name))
    return jsonify(json_data)


# 多度查询，分支检索
@app.route('/search_branch', methods=['GET', 'POST'])
def search_branch():
    name = request.args.get('name')
    deep = request.args.get('deep')
    json_data = query_branch(str(name), deep)
    return jsonify(json_data)


# 查询最短路径
@app.route('/search_path', methods=['GET', 'POST'])
def search_path():
    a = request.args.get('a')
    b = request.args.get('b')
    json_data = query_path(str(a), str(b))
    return jsonify(json_data)


## Neo4j数据库增删改查
# 改变节点概念级别
@app.route('/change_node', methods=['GET', 'POST'])
def change_node():
    node = request.args.get('node')
    cate = request.args.get('cate')
    update_node(node, cate)
    return render_template('all_relation.html')
    # json_data = update_node(str(node), str(cate))
    # return jsonify(json_data)


# 添加一条关系
@app.route('/add_Node', methods=['GET', 'POST'])
def add_Node():
    e1 = request.form.get('e1')
    e2 = request.form.get('e2')
    rel = request.form.get('rel')
    c1 = request.form.get('c1')
    c2 = request.form.get('c2')
    add_node(e1, e2, rel, c1, c2)
    # print(message)
    # print(e1)
    # response = make_response(jsonify({'status':'success'}))
    return redirect('/all_relation.html')


# 删除一个节点
@app.route('/delete_aNode', methods=['GET', 'POST'])
def delete_aNode():
    name = request.args.get('node')
    delete_node(name)
    return redirect('/all_relation.html')


@app.route('/all_relation.html', methods=['GET', 'POST'])
def get_all_relation():
    relation = session.get('relation')
    return render_template('all_relation.html', relation=relation)


# --------------------------part-------------------------------
# --------------------------part-------------------------------


@app.route('/linear.html', methods=['GET', 'POST'])
def linear():
    return render_template('part/linear.html')


# -------------------------other------------------------------
# -------------------------other------------------------------
@app.route('/search_path.html', methods=['GET', 'POST'])
def search_path1():
    return render_template('search_path.html')


# -------------------------data_show------------------------------
# -------------------------data_show------------------------------
@app.route('/cate_rel', methods=['GET', 'POST'])
def cate_rel():
    """请求的数据源，该函数将数据库中存储的数据，返回以下这种数据的列表：
       {'name': '香蕉', 'id': 1, 'price': '10'}
       {'name': '苹果', 'id': 2, 'price': '10'}
    """
    # data = cate_rel_show()

    # if request.method == 'POST':
    #     print('post')
    # if request.method == 'GET':
    #     info = request.values
    #     limit = info.get('limit', 10)  # 每页显示的条数
    #     offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
    #     print('get', limit)
    # print('get  offset', offset)

    name = request.args.get('search_kw')
    if name:
        print(name)
        sql = "select * from cate_rel where e1 like '%{0}%' or e2 like '%{0}%' or rel like '%{0}%' or c1 like '%{0}%' or c2 like '%{0}%'".format(
            name)
    else:
        sql = 'SELECT * FROM cate_rel'
    data = cate_rel_show(sql)
    return jsonify(data)
    # return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
    # 注意total与rows是必须的两个参数，名字不能写错，total是数据的总长度，rows是每页要显示的数据,它是一个列表
    # 前端根本不需要指定total和rows这俩参数，他们已经封装在了bootstrap table里了


# 添加一条记录
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    e1 = request.form.get('e1')
    e2 = request.form.get('e2')
    rel = request.form.get('rel')
    c1 = request.form.get('c1')
    c2 = request.form.get('c2')
    item = [e1, e2, rel, c1, c2]
    sql = 'insert cate_rel (e1, e2, rel, c1, c2)VALUES (%s, %s, %s, %s, %s)'
    operation(sql, item)
    # print(e1)
    # response = make_response(jsonify({'status':'success'}))
    return redirect('/data_show.html')


# 更新一条记录
@app.route('/update_item', methods=['GET', 'POST'])
def update_item():
    cate_rel_id = request.form.get('cate_rel_id')
    e1 = request.form.get('update_e1')
    e2 = request.form.get('update_e2')
    rel = request.form.get('update_rel')
    c1 = request.form.get('update_c1')
    c2 = request.form.get('update_c2')
    item = [e1, e2, rel, c1, c2, cate_rel_id]
    # print(item)
    sql = 'update cate_rel set e1 = %s, e2 = %s, rel = %s, c1 = %s, c2 = %s where cate_rel_id = %s'

    operation(sql, item)
    # print(e1)
    # response = make_response(jsonify({'status':'success'}))
    return redirect('/data_show.html')


# 删除一条记录
@app.route('/delete_item', methods=['GET', 'POST'])
def delete_item():
    cate_rel_id = request.args.get("id")
    cate_rel_id = int(cate_rel_id)
    print(cate_rel_id)
    item = [cate_rel_id]
    sql = 'delete from cate_rel where cate_rel_id = "%s"'
    operation(sql, item)
    return redirect('/data_show.html')


@app.route('/data_show.html', methods=['GET', 'POST'])
def data_show():
    # train_data_list = get_train_data_list('/kg_data/cate.csv')
    return render_template('data_show/data_show.html')


@app.route('/cate.html', methods=['GET', 'POST'])
def cate():
    train_data_list = get_train_data_list('/kg_data/cate.csv')
    return render_template('data_show/cate.html', train_data_list=train_data_list)


@app.route('/relation.html', methods=['GET', 'POST'])
def relation():
    train_data_list = get_train_data_list('/kg_data/relation.csv')
    return render_template('data_show/relation.html', train_data_list=train_data_list)


# 注册界面
@app.route('/register.html', methods=['GET', 'POST'])
def register1():
    relation, entity = get_data_num()
    return render_template('register.html', entity=entity, relation=relation)


# 注册界面接收信息，并传送到数据库里面
@app.route('/register', methods=['POST'])
def register():
    a = login.register_function()
    if a:
        return render_template('register.html', msg='注册成功！')
    else:
        return render_template('register.html', msg='账号已被注册!')


# 登录界面
@app.route('/login.html', methods=['GET', 'POST'])
def login1():
    relation, entity = get_data_num()
    return render_template('login.html', entity=entity, relation=relation)


# 登录界面接收数据，判断是否登录成功
@app.route('/login', methods=['POST'])
def login2():
    a = login.login_function()
    if a:
        # 如果登录成功，获取到登录界面输入的username，然后用session定义一个可跨路由的变量
        user = request.form.get('username')
        session['user'] = user
        return render_template('index.html')
    else:
        return render_template('login.html', msg='账号或密码错误，请重新输入')


# 个人用户界面
@app.route('/personal_info.html', methods=['GET', 'POST'])
def personal_info1():
    relation, entity = get_data_num()
    return render_template('personal_info.html', entity=entity, relation=relation)


# 获取mysql里面的数据，展示在个人用户界面
@app.route('/personal_info', methods=['GET', 'POST'])
def personal_info():
    # 获取登录路由定义的user值
    user = session.get('user')

    # 调用函数personal_info_function，并将返回值赋值给u
    u = login.personal_info_function(user)
    return render_template('personal_info.html', u=u)


# 我的图谱界面
@app.route('/my_graph.html', methods=['GET', 'POST'])
def my_graph():
    relation, entity = get_data_num()
    return render_template('my_graph.html', entity=entity, relation=relation)


# 点击下载按钮，即可把图片base64数据传到数据库里面
@app.route('/base', methods=['GET', 'POST'])
def base():
    base1 = request.args.get('base')
    username = session.get('user')
    # 调用函数up_graph
    login.up_graph(base1, username)
    return ""


# 获取数据库里面的图片base64码，传到我的图谱界面
@app.route('/my_graph', methods=['GET', 'POST'])
def my_graph1():
    # 获取登录路由定义的user值
    user = session.get('user')
    # 调用函数show_graph
    u2 = login.show_graph(user)
    return render_template('my_graph.html', u=u2)


# 首页
@app.route('/welcome.html', methods=['GET', 'POST'])
def welcome():
    relation, entity = get_data_num()
    session['relation'] = relation
    return render_template('welcome.html', entity=entity, relation=relation)


# 分词界面
@app.route('/word_seg.html', methods=['GET', 'POST'])
def word():
    return render_template('word_seg.html')


# 分词界面
@app.route('/word_seg', methods=['GET', 'POST'])
def word_seg():
    text = request.form.get('input_text')
    result_seg = seg_word(text)
    result_seg_flag = seg_word_flag(text)
    return render_template('word_seg.html', result_seg=result_seg, result_seg_flag=result_seg_flag, text=text)


# 文件上传
@app.route('/up_file.html', methods=['GET', 'POST'])
def up_file():
    return render_template('up_file.html')


@app.route('/up_file', methods=['GET', 'POST'])
def up_file1():
    if request.method == 'POST':
        f = request.files['myfile']
        name = secure_filename(f.filename)
        if (f):
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            up_file_path = os.path.join(basepath, './static/updata_file', secure_filename(f.filename))
            # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            up_file_path = os.path.abspath(up_file_path)  # 将路径转换为绝对路径
            f.save(up_file_path)
    return render_template('up_file.html', name=name)


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
