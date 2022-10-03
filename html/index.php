<!DOCTYPE html>
<html lang="zh-CN">
  <head>
      <title>羊了个羊3D地图</title>
      <meta charset="utf-8">
  </head>
  <body>
    <?php
      //header('Access-Control-Allow-Origin:*');  //支持全域名访问，不安全，部署后需要固定限制为客户端网址
      //header('Access-Control-Allow-Headers:x-requested-with,content-type');  //响应头 请按照自己需求添加。
      class MyDB extends SQLite3{
        function __construct(){
          $this->open('sheep_maps.db');
        }
      }
      $db = new MyDB();
      if(!$db){
        echo "<script>window.alert('".$db->lastErrorMsg()."');</script>\n\t";
        //echo $db->lastErrorMsg();
      } else {
        echo "<script>console.log('成功创建或打开数据文件');</script>\n\t";
        //echo "成功创建或打开数据文件\n";
      }

      $sql1 =<<<EOF
        CREATE TABLE IF NOT EXISTS MAPS(
          ID INTEGER PRIMARY KEY AUTOINCREMENT,
          MAP_INFO TEXT
        );
EOF;

      $ret1 = $db->exec($sql1);
      if(!$ret1){
        echo "<script>window.alert('".$db->lastErrorMsg()."');</script>\n\t";
        //echo $db->lastErrorMsg();
      } else {
        echo "<script>console.log('成功创建或检查数据表');</script>\n\t";
        //echo "成功创建或检查数据表\n";
      }

      $req_json_str = isset($GLOBALS['HTTP_RAW_POST_DATA']) ? $GLOBALS['HTTP_RAW_POST_DATA'] : file_get_contents("php://input");
      //echo gettype($req_json_str);
      if(strpos($req_json_str, "blockTypeData") !== false){
        $sql2 = "INSERT INTO MAPS (MAP_INFO) VALUES ('$req_json_str')";
        $ret2 = $db->exec($sql2);
        $ret3 = $db->query("SELECT MAX(ID) from MAPS");
        if(!$ret2){
          echo "<script>window.alert('".$db->lastErrorMsg()."');</script>\n\t";
          //echo $db->lastErrorMsg();
        } else {
          echo "<script>console.log('成功插入数据');</script>\n\t";
          //echo "成功插入数据\n";
          while($row = $ret3->fetchArray() ){
            $ID = $row["MAX(ID)"];
            echo "<a href='/sheep_map?id=$ID'>访问3d地图</a>\n\t";
            echo "<script>window.location.href='/sheep_map?id=$ID';</script>\n";
          }
        }
      } else {
        echo "<a href='/sheep_map'>访问3d地图</a>\n\t";
        echo "<script>window.location.href='/sheep_map';</script>\n";
      }
      $db->close();
    ?>
  </body>
