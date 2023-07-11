import requests
def up(path:str):
    def UpFile(Url, FilePath, data):
        '''
        用于POST上传文件以及提交参数
        @ Url 上传接口
        @ FilePath 文件路径
        @ data 提交参数 {'key':'value', 'key2':'value2'}
        '''
        files = {'file': open(FilePath, 'rb')}
        result = requests.post(Url, files=files, data=data)
        return result

    # 上传接口
    url = 'http://mg.dawnaurora.top/receive.php'
    # 需提交的参数
    data = {'key': 'value', 'key2': 'hello'}
    # 需上传的文件路径
    #file = 'D:/test1.txt'
    file = path
    r = UpFile(url, file, data)
    # 打印返回的值
    print(r.text)

if __name__=="__main__":
    up("D:/test1.txt")