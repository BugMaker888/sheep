> PHP版本，Fork 自 [BugMaker888/sheep](https://github.com/BugMaker888/sheep)<br>
求解算法来自 [NB-Dragon/SheepSolver](https://github.com/NB-Dragon/SheepSolver) ，5分钟内求解成功率暂时不高

> 经过一些调整和测试，四种模式同时尝试有一定概率在短时间内得到解，甚至是多解，建议超过60~90秒就放弃重试！

### 一、运行环境

#### 1、Python3

推荐使用`Anaconda`进行安装，官网：[https://www.anaconda.com](https://www.anaconda.com/) 。

#### 2、~~Node.js~~ web服务 + PHP

~~为了运行`three.js`网页，官网：[https://nodejs.org/zh-cn/download](https://nodejs.org/zh-cn/download/) 。~~

使用`nginx`或`apache`等 web 服务搭配 php 环境以及 sqlite 数据库，具体可以百度。

搭建好 web 服务环境后需要将`sheep.py`脚本中的服务器地址换成你自己的。

用我的也行，不过加载可能比较慢，关卡数据加载失败的话可以多刷新几次。

本人因为想将3d地图放在 vps 上，所以使用的是 nginx 虚拟主机（域名）搭配 php 环境，mitmproxy 抓包放在了本地电脑上。

---

### 二、克隆本项目

使用以下命令将本项目克隆到本地，并进入项目目录：
```
git clone https://github.com/longhuan1999/sheep.git
cd sheep/
```

> MacOS系统使用终端执行，Windows系统使用Powershell。

---

### 三、mitmproxy的配置

`mitmproxy`是一个开源的抓包工具，项目地址为：[https://github.com/mitmproxy/mitmproxy](https://github.com/mitmproxy/mitmproxy) ，最大的优点是可以加载自己写的python代码进行数据处理。

目测不支持国外vps抓包，游戏会检测ip的地理位置。

#### 1、安装

安装Python3后，执行以下命令安装mitmproxy、pyExecJs、func_timeout和requests：
```
pip install mitmproxy pyExecJs func_timeout requests
```

#### 2、启动

~~因为`three.js`和`mitmproxy`都默认使用`8080`端口，所以需要改一下端口运行。~~

将终端切换到本项目目录，执行以下命令加载`sheep.py`插件：
```
mitmweb -p 6666 -s sheep.py
# 默认代理端口是8080，默认web端口是8081，如果出现端口占用情况，参考以下参数
# -p [代理端口]
# --web-port [web端口]
# --web-iface 或 --web-host [web主机名]
# 示例：
mitmweb -p 9998 -s sheep.py --web-port 9999 --web-iface 0.0.0.0
mitmweb -p 9998 -s sheep.py --web-port 9999 --web-host 0.0.0.0
```

执行后浏览器会弹出一个抓包的网页界面。


#### 3、安装证书

接下来使用手机连接电脑的ip以及使用`6666`端口作为代理，就可以抓包了。

设置代理可以参考视频教程 [【4分钟教会你Charles抓包设置抓取电脑HTTPS以及IOS手机抓包-哔哩哔哩】](https://b23.tv/S0d8iYa) 两分钟的地方。

使用手机浏览器访问 [http://mitm.it](http://mitm.it) 安装`mitmproxy`的证书。

苹果手机需要在 <kbd>设置</kbd> - <kbd>通用</kbd> - <kbd>关于本机</kbd> - <kbd>证书信任设置</kbd> 里信任证书。

如果安卓手机安装不了证书，也可以使用电脑的安卓模拟器。


#### 4、使用

~~因为关卡数据每天只会请求一次，所以可以先删除游戏再重新进入。~~

~~手机进入游戏后，电脑刷新网页，就可以看到最新的游戏3d地图了。~~

> ~~因为`sheep.py`默认将地图数据保存到`./three.js/examples/map_data.js`里，如果`three.js/`没放到`sheep/`目录里的话，需要修改`sheep.py`里的路径。~~

目测不支持抖音小游戏版抓包，微信小游戏版支持。

主页面的`再次挑战`会刷新地图，游戏失败后的`重新挑战`不会刷新地图。

你可以在命令行的输出中看出地图是否刷新，3d地图的网页地址也会在命令行输出：

![image](https://user-images.githubusercontent.com/43313501/193447310-8bc58d9b-8548-4c23-a98d-38c2e3804a4f.png)

---

### 四、游戏数据

文件`sheep_map/map_data.js`里面是游戏的关卡数据示例，本项目抓取的关卡地图数据保存在服务器端的 sqlite 文件中。

大致说明一下字段的含义：

``` json
{
    "widthNum": 8,
    "heightNum": 10,
    "levelKey": 90029,
    "blockTypeData": {  //图案类型对应组数
        "1": 6,         //图案1有6*3=18个
        "2": 6,
        "3": 6,
        "4": 6,
        "5": 5
    },
    "levelData": {  //关卡数据
        "1": [      //第1层，也就是最底层
            {
                "id": "1-24-8", //方块id
                "type": 2,      //图案类型
                "rolNum": 24,   //x坐标
                "rowNum": 8,    //y坐标
                "layerNum": 1,  //层数
                "moldType": 1,
                "blockNode": null
            }

            //......
        ]
    },
    "layers": [     //排序后的层数
        "1",
        "2",
        "3",
        "4",
        "5"
    ],
    "oprations": [      //自动求解步骤
        "21-12-28",     //方块id
        "20-44-20",
        "13-44-12",
        "21-44-28",
        "16-44-40",
        "13-20-12",
        "17-28-24",
        "14-24-40"
        //......
    ]
}
```

地图原点在左上角，方块的大小是`8 * 8`，有了这些数据就可以尝试写算法求解了。

如果得到了求解步骤，可以将求解步骤保存到oprations字段，内容为依次点击的方块id，网页可以自动显示求解步骤。