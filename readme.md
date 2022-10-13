
> 目前的安装教程和b站视频区别较大，以本页面的教程为准。

### 一、运行环境

#### 1、Python3

推荐使用`Anaconda`进行安装，官网：[https://www.anaconda.com](https://www.anaconda.com/) 。

#### 2、Node.js

用来安装网页服务器以及防止`pyExecJs`库报错，官网：[https://nodejs.org/zh-cn/download](https://nodejs.org/zh-cn/download/) 。

#### 3、Git

Windows系统需要手动安装`git`，官网：[https://gitforwindows.org](https://gitforwindows.org/) 。

---

### 二、克隆本项目

使用以下命令将本项目克隆到本地，并进入项目目录：
```
git clone https://github.com/BugMaker888/sheep.git
cd sheep/
```

> MacOS系统使用终端执行，Windows系统使用Powershell。

---

### 三、启动网页服务器

在本项目目录下分别执行以下命令启动网页服务器：
```
cd html/
npm install -g live-server
live-server
```

执行后会浏览器会自动打开3d地图网页。

---

### 四、mitmproxy的配置

[mitmproxy](https://github.com/mitmproxy/mitmproxy)是一个开源的抓包工具，可以加载自己写的Python代码进行数据处理。

#### 1、安装

执行以下命令安装`mitmproxy`：
```
pip install mitmproxy
```

由于插件使用到了`pyExecJs`库，所以还需要执行：
```
pip install pyExecJs
```

#### 2、启动

新开一个终端，切换到本项目目录，执行以下命令启动抓包工具并加载`sheep.py`插件：
```
mitmweb -p 6666 -s sheep.py
```

执行后浏览器会弹出一个抓包的网页界面。

接下来使用手机连接电脑的ip以及使用`6666`端口作为代理，就可以抓包了。

> 设置代理可以参考视频教程 [【4分钟教会你Charles抓包设置抓取电脑HTTPS以及IOS手机抓包-哔哩哔哩】](https://b23.tv/S0d8iYa) 两分钟的地方。

#### 3、安装证书

使用手机浏览器访问 [http://mitm.it](http://mitm.it) 安装`mitmproxy`的证书。

苹果手机需要在 <kbd>设置</kbd> - <kbd>通用</kbd> - <kbd>关于本机</kbd> - <kbd>证书信任设置</kbd> 里信任证书。

如果安卓手机安装不了证书，也可以使用电脑的夜神模拟器，安装安卓5系统。

也可以使用Windows版微信的小程序。

#### 4、使用

因为关卡数据每天只会请求一次，所以可以先删除游戏再重新进入。

手机进入游戏后，电脑刷新网页，就可以看到最新的游戏3d地图了。

---

### 五、游戏数据

文件`html/map_data.js`里面保存着游戏的关卡数据。

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

如果得到了求解步骤，可以将求解步骤保存到`oprations`字段，内容为依次点击的方块id，网页可以自动显示求解步骤。
