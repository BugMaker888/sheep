<!DOCTYPE html>
<html lang="zh-CN">
  <head>
      <title>羊了个羊3D地图</title>
      <meta charset="utf-8">
  </head>
  <body>
    <?php
      date_default_timezone_set("PRC");
      $data_time = date('Y-m-d H:i:s');
      function getRealIp()
      {
        $ip=false;
        if(!empty($_SERVER["HTTP_CLIENT_IP"])){
          $ip = $_SERVER["HTTP_CLIENT_IP"];
        }
        if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
          $ips = explode (", ", $_SERVER['HTTP_X_FORWARDED_FOR']);
          if ($ip) { array_unshift($ips, $ip); $ip = FALSE; }
          for ($i = 0; $i < count($ips); $i++) {
            if (!eregi ("^(10│172.16│192.168).", $ips[$i])) {
              $ip = $ips[$i];
              break;
            }
          }
        }
        return ($ip ? $ip : $_SERVER['REMOTE_ADDR']);
      }
      $ip = getRealIp();
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
          MAP_INFO TEXT,
          IP TEXT,
          DATA_TIME TEXT
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
      if(strpos($req_json_str, "levelData") !== false && strpos($req_json_str, "layers") !== false){
        $ret4 = $db->query("SELECT ID FROM MAPS WHERE MAP_INFO = '$req_json_str'");
        while($row = $ret4->fetchArray()){
          $ID = $row["ID"];
        }
        if($ID == null){
          $sql2 = "INSERT INTO MAPS (MAP_INFO,IP,DATA_TIME) VALUES ('$req_json_str','$ip','$data_time')";
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
            }
          }
        }
      }
      if($ID == null){
        echo "<a href='/sheep_map'>访问示例3D地图</a>\n\t";
        echo "<script>window.location.href='/sheep_map';</script>\n";
      } else {
        echo "<a href='/sheep_map?id=$ID'>访问当前关卡3D地图</a>\n\t";
        echo "<script>window.location.href='/sheep_map?id=$ID';</script>\n";
      }
      $db->close();
    ?>
  </body>
