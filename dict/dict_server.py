#dict_server.py

'''
name:liudahan
date:2018-09-28
email:liudahan@163.com
modules:dict_server
This is a decriptions

'''
from socket import *
import os 
import time
import signal
import pymysql
import sys

# 定义需要的全局变量
DICT_TEXT = './dict.txt'
HOST = '0.0.0.0'
PORT = 9000
ADDR = (HOST,PORT)

# 流程控制
def main():
    # 创建数据库连接
    db = pymysql.connect('localhost','liudahan','liudahan','dict')

    # 创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    # 忽略子进程信号
    singnal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            c,addr = s.accept()
            print('Connect from ',addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue

        # 创建子进程
        pid = os.fork()
        if pid == 0:
            s.close()
            # print('子进程准备处理请求')
            # sys.exit('子进程退出')
            do_child(c,db)
        else:
            c.close()
            continue

def do_child(c,db):
    # 循环接收客户请求
    while True:
        data = c.recv(128).decode()
        print(c.getpeername(),':',data)
        if (not data) or data[0] == 'E':
            c.close()
            sys.exit(0)
        if data[0] =='R':
            do_register(c,db,data)
        elif data[0] == 'L':
            do_login(c,db,data)
        elif data[0] == 'Q':
            do_query(c,db,data)
        elif data[0] == 'H':
            do_his(c,db,data)

def do_login(name,password):
    print('登录操作')
    l = data.split(' ')
    name = l[1]
    password = l[2]
    cursor = db.cursor()
    sql = "select * from userinfo where\
    name = '%s' and password = '%s'"\
    %(name,password)

    cursor.execute(sql)
    r = cursor.fetchone()

    if r == None:
        c.send(b'Fail')
    else:
        print("'%s'登录成功"%name)
        c.send(b'OK')   

def do_register(c,db,data):
    print('注册操作')
    l = data.split(' ')
    name = l[1]
    password = l[2]
    cursor = db.cursor()
    sql = "select * from user where \
     name = '%s'"%name
    cursor.excute(sql)
    r = cursor.fetchone()

    if r != None:
        c.send(b'EXIST')
        return
    sql = "insert into user(username,\
    password) values \
     ('%s','%s')" %(name,password)

    try:
        cursor.excute(sql)
        db.commit()
        c.send(b'OK')
    except:
        db.rollback()
        c.send(b'Fail')
    else:
        print('%s注册成功'%name)


def do_query():
    print('查询操作')
    l = data.split(' ')
    name = l[1]
    word = l[2]
    cursor = db.cursor()
    sql = 'select * from user where \
    name = '%s''%name
    cursor.excute(sql)

    def insert_history():
        tm = time.time()

        sql = 'insert into his(name,word,time)\
        values("%s","%s"))'%(name,word,tm)
        try:
            cursor.excute(sql)
            db.commit()
        except:
            db.rollback()        

    # 文本查询
    try:
        f = open(DICT_TEXT):
    except:
        c.send(b'Fail')
        return

    for line in f:
        tmp = line.split(' ')[0]
        if tmp > word:
            c.send(b'Fail')
            f.close()
            return
        elif tmp = word:
            c.send(b'OK')
            time.sleep(0.1)
            c.send(line.encode())
            f.close()
            insert_history()
            return
    c.send(b'Fail')
    f.close()

def do_his(c,db,data):
    print('查询历史记录')
    l = data.split(' ')
    name = l[1]
    cursor = db.cursor()
    
    sql = 'select * from his where \
    name = '%s''%name
    cursor.excute(sql)
    r = cursor.fetchall()
    if not r:
        c.send(b'Fail')
        return
    else:
        c.send(b'OK')

    for i in r:
        time.sleep(0.1)
        msg = '%s %s %s'%(i[1],i[2],i[3])
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b'##')

if __name__ == '__main__':
    main()