<!DOCTYPE html>
<html lang="zh-CN">
    <head>
        <title>羊了个羊3D地图</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">
        <!-- <link type="text/css" rel="stylesheet" href="main.css"> -->
        <style>
            body {
                background-color: #cff998;
                color: #000;
                overflow: hidden;
                font-family: Monospace;
                font-size: 13px;
                line-height: 24px;
                overscroll-behavior: none;
            }
            a {
                color: #f00;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            * {
                margin:0;
            }
            #info {
                position: absolute;
                top: 0px;
                width: 100%;
                padding: 10px;
                box-sizing: border-box;
                text-align: center;
                -moz-user-select: none;
                -webkit-user-select: none;
                -ms-user-select: none;
            }
        </style>
        <script async src="https://unpkg.com/es-module-shims@1.3.6/dist/es-module-shims.js"></script>
        <script type="importmap">
            {
                "imports": {
                    "three": "https://unpkg.com/three@0.145.0/build/three.module.js",
                    "OrbitControls": "https://unpkg.com/three@0.145.0/examples/jsm/controls/OrbitControls.js"
                }
            }
        </script>
    </head>

    <body>
        <div id="info">
            <a id="undo" href="javascript:void(0)">【撤销移除】</a>
            <a id="auto_solve" href="javascript:void(0)"></a>
            <a id="single_step_solve" href="javascript:void(0)"></a>
        </div>

        <!-- Import maps polyfill -->
        <!-- Remove this when import maps will be widely supported -->
        <?php
            if(is_array($_GET)&&count($_GET)>0){//判断是否有Get参数
                if(isset($_GET["id"])){//判断所需要的参数是否存在，isset用来检测变量是否设置，返回true or false
                    $id = $_GET["id"];//存在
                    echo "<script type='module' src='./map_data.php?id=$id'></script>\n";
                } else {
                    echo "<script type='module' src='./map_data.php'></script>\n";
                }
            } else {
                echo "<script type='module' src='./map_data.php'></script>\n";
            }
        ?>
    </body>
</html>