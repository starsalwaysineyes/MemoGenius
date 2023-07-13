#服务器端接受文件脚本
from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file.save('/www/wwwroot/mg.dawnaurora.top/uploads/file001.txt')  # 保存文件到指定路径
        return '文件上传成功'
    else:
        return '文件上传失败'

if __name__ == '__main__':
    app.run()
