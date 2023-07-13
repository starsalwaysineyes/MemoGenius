<?php
    //获取提交参数
    $a = $_POST["key"];
    $b = $_POST["key2"];

    echo $_FILES['file']['name'];
    if (isset($_FILES['file']))
    {
        //将文件传到服务器根目录中
        //$Up_Path = $_FILES['file']['name'];
        $Up_Path = __DIR__ . '/uploads/' . $_FILES['file']['name'];
        $tmpname = $_FILES['file']['tmp_name'];
        //转移临时文件
        if(move_uploaded_file($tmpname,$Up_Path)){
            echo "上传成功";
        }else{
            echo "上传失败";
        }
    }
    else
    {
        echo "上传失败";
        
    }