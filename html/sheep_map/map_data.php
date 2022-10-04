<?php
    class MyDB extends SQLite3{
        function __construct(){
            $this->open('../sheep_maps.db');
        }
    }
    if(is_array($_GET)&&count($_GET)>0){//判断是否有Get参数
        if(isset($_GET["id"])){//判断所需要的参数是否存在，isset用来检测变量是否设置，返回true or false
            $id = $_GET["id"];//存在
            $db = new MyDB();
            if(!$db){
                echo "window.alert('".$db->lastErrorMsg()."');\n";
                //echo $db->lastErrorMsg();
            } else {
                echo "console.log('成功打开数据文件');\n";
                //echo "成功创建或打开数据文件\n";
            }
            $ret1 = $db->query("SELECT ID,MAP_INFO from MAPS WHERE ID = $id");
            $ret2 = $db->query("SELECT MIN(ID) from MAPS");
            while($row = $ret1->fetchArray()){
                $map_info = $row["MAP_INFO"];
                echo "const map_data = $map_info;";
                array_push($obj,$row);
            }
            if(count($obj) == 0){
                echo "window.alert('没有查询到 id=$id 的关卡地图数据！关卡地图数据可能已过期或者id不正确!')";
            }
            while($row = $ret2->fetchArray()){
                $min_id = $row["MIN(ID)"];
                if(($id - $min_id) >= 50){
                    $ret3 = $db->exec("DELETE from MAPS where ID=$min_id;");
                    if(!$ret3){
                        echo "window.alert('".$db->lastErrorMsg()."');\n";
                    } else {
                        echo "console.log('".$db->changes()."  成功删除数据');\n";
                    }
                }
            }
        }
    }
?>