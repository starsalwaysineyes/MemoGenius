def func1():
    print("开始测试上传按钮")

    url = "http://mg.dawnaurora.top/upload"  # 替换为服务器端接收上传文件的URL
    file_path = "D:/test.txt"  # 替换为要上传的文件路径

    with open(file_path, "rb") as file:
        files = {"file": file}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        print("文件上传成功")
    else:
        print(response.status_code)
        print("文件上传失败")

    print("测试结束")