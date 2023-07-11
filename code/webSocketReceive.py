#socket服务器端监听
#导入模块
import socket
#模块进行实例化
sk = socket.socket()
#设置端口通讯地址
ip_port = ('127.0.0.1',5000)
#地址绑定
sk.bind(ip_port)
#最大连接数量
sk.listen(5)
#进入循环接收数据
while True:
    #等待客户端连接
    conn,address = sk.accept()
    #一直使用当前连接进行数据发送
    #直到标志接收完成
     #循环接收数据
    while True:
        #打开文件
        with open("file","ab") as f:
            #准备写入数据
            data = conn.recv(1024)
            #进行判断数据是否接收完毕
            if data == b'quit':
                break
            #写入文件数据
            f.write(data)
        # 接收完成标志
        conn.send('success'.encode())
    #打印文件信息
    print('文件接收完成')
sk.close()