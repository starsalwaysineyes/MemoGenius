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
            
            $param = $_FILES['file']['name'];
    
            // 指定目标文件路径和名称
            $file = '/www/wwwroot/mg.dawnaurora.top/test/input.txt';
            
            // 将参数写入文件
            file_put_contents($file, $param);
            
            /*
            $outputFile = '/www/wwwroot/mg.dawnaurora.top/test/file.txt';  // 替换为Python脚本输出的文件路径
            $output = file_get_contents($outputFile);
            echo nl2br($output);  // 显示输出内容
            */
            
            $output = exec("python3 /pyworks/transfile.py");
            echo "总结完成！";
            //echo nl2br($output);  // 显示输出内容
            
            //$outputFile = '/www/wwwroot/mg.dawnaurora.top/test/result.txt';  // 替换为Python脚本输出的文件路径
            //$output2 = file_get_contents($outputFile);
            //echo nl2br($output2);  // 显示输出内容
            
            /*
            //开始编写调用python脚本的程序
            $pythonScript = '/pyworks/testexec.py';  // 替换为实际的Python脚本路径
            exec("python3 $pythonScript", $output, $returnStatus);
            if ($returnStatus == 0) {
                echo 'Python脚本执行成功';
                // 输出Python脚本的内容
                foreach ($output as $line) {
                    echo $line . '<br>';
                }


            } else {
                echo 'Python脚本执行失败';
            }*/
            

        }
        else
        {
            echo "上传失败";
        }
    }
    else
    {
        echo "上传失败";
        
    }