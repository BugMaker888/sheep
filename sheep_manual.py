from os.path import isfile
from autoSolve import auto_solve
from subprocess import Popen, PIPE, STDOUT
import execjs
import json
import _thread


def cmd(command):
    subp = Popen(args=command, shell=True, encoding='utf8', stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    subp.wait()
    if subp.poll() == 0:
        output = ""
        for i in (subp.communicate()[0]).split("\n"):
            if "进度" in i and output == "":
                output += "\n%s：\033[0m"%i[:i.index("进度")]
            elif "超时" in i:
                output += "\033[0;33;40m%s"%i[i.index("自动求解超时"):]
            elif "无解" in i:
                output += "\033[0;33;40m%s"%i[i.index("牌面无解"):]
            elif "计算用时" in i:
                output += "\033[0;32;40m%s | "%i[i.index("计算用时"):]
            elif "当前关卡3D地图地址" in i:
                output += "%s"%i
            elif "地图生成失败" in i:
                output += "%s"%i
        print(output)
    else:
        print("失败")
        print(subp.communicate()[0])


js_code = open("shuffle.js", encoding="utf-8").read()

# 原始地图数据, 从 maps 接口获取到的数据
map_data_path = "./map_data.txt"

# 随机种子，从 map_info_ex 接口"data"字段下的"map_seed"获取到的数据，默认种子为：seed = [0, 0, 0, 0]
seed = [3270836840, 3431855579, 3015956679, 1737139174]

""" 制作地图数据 """

print("==========================================")

# 判断原始地图数据文件是否存在
if not isfile(map_data_path):
    input("原始地图数据文件不存在！")
    exit(1)

# 读取原始地图数据
map_data = json.loads(open(map_data_path).read())

# 根据"blockTypeData"字段按顺序生成所有类型的方块，存放到数组
block_type_data = map_data["blockTypeData"]
block_types = []
for i in range(1, 16+1):
    block_type = str(i)
    if block_type in block_type_data:
        count = block_type_data[block_type] * 3
        block_types.extend([i] * count)

# 调用js方法将数组打乱，打乱后的结果和游戏的一样
block_types = execjs.compile(js_code).call("shuffle", block_types, seed)
print(block_types)

# 将游戏的层数排序
level_data = map_data["levelData"]
layers = list(level_data.keys())
layers.sort(key=lambda x:int(x))

# 为了方便three.js按顺序读取层数，所以将层数保存起来
map_data["layers"] = layers

# 将打乱后的图案按顺序填充到每个方块的"type"字段里
index = 0
for layer in layers:
    for block_data in level_data[layer]:
        if block_data["type"] > 0:
            continue
        block_data["type"] = block_types[index]
        index += 1

print("==========================================")
# 保存关卡数据到文件
with open("map_data.json", "w", encoding="utf8") as f:
    f.write(json.dumps(map_data, indent=4))
print("已将当前关卡数据保存到当前路径下 map_data.json 文件！")
# 同步进行自动求解
if isfile("config.json"):
    try:
        with open("config.json","r",encoding="utf8") as f:
            configs = json.loads(f.read())
        if "issort" not in configs or "percent" not in configs or "timeout" not in configs or ("timeout" in configs and type(configs["timeout"]) != int) or ("percent" in configs and type(configs["percent"]) != float):
            print("\n当前配置文件存在错误，将使用默认配置求解！")
            configs = {"issort":"","percent":0.85,"timeout":60}
            with open("config.json","w",encoding="utf8") as f:
                f.write(json.dumps(configs,indent=4))
        else:
            print("\n将使用配置文件 config.json 的配置求解！")
    except:
        print("\n当前配置文件存在错误，将使用默认配置求解！")
        configs = {"issort":"","percent":0.85,"timeout":60}
        with open("config.json","w",encoding="utf8") as f:
            f.write(json.dumps(configs,indent=4))
else:
    print("\n当前配置文件不存在，将使用默认配置求解！")
    configs = {"issort":"","percent":0.85,"timeout":60}
    with open("config.json","w",encoding="utf8") as f:
        f.write(json.dumps(configs,indent=4))

issort = configs["issort"]
percent = configs["percent"]
timeout = configs["timeout"]

if issort != "true" and issort != "reverse" and percent == 0.85:
    threadName = "普通模式"
    command1 = "python3 autoSolve.py -s reverse -t %d"%timeout
    command2 = "python3 autoSolve.py -p 0 -t %d"%timeout
    command3 = "python3 autoSolve.py -s reverse -p 0 -t %d"%timeout
elif issort == "reverse" and percent == 0.85:
    threadName = "高层优先模式"
    command1 = "python3 autoSolve.py -t %d"%timeout
    command2 = "python3 autoSolve.py -p 0 -t %d"%timeout
    command3 = "python3 autoSolve.py -s reverse -p 0 -t %d"%timeout
elif issort != "true" and issort != "reverse" and percent == 0:
    threadName = "优先移除两张相同类型的手牌模式"
    command1 = "python3 autoSolve.py -s reverse -t %d"%timeout
    command2 = "python3 autoSolve.py -t %d"%timeout
    command3 = "python3 autoSolve.py -s reverse -p 0 -t %d"%timeout
elif issort == "reverse" and percent == 0:
    threadName = "高层优先且优先移除两张相同类型的手牌模式"
    command1 = "python3 autoSolve.py -s reverse -t %d"%timeout
    command2 = "python3 autoSolve.py -p 0 -t %d"%timeout
    command3 = "python3 autoSolve.py -t %d"%timeout
else:
    threadName = "自定义模式"
    command1 = "python3 autoSolve.py -s reverse -t %d"%timeout
    command2 = "python3 autoSolve.py -p 0 -t %d"%timeout
    command3 = "python3 autoSolve.py -s reverse -p 0 -t %d"%timeout
    command4 = "python3 autoSolve.py -p 0 -t %d"%timeout

try:
    _thread.start_new_thread( cmd, (command1,))
    _thread.start_new_thread( cmd, (command2,))
    _thread.start_new_thread( cmd, (command3,))
    if threadName == "自定义模式":
        _thread.start_new_thread( cmd, (command4,))
except Exception as e:
    print ("Error: 无法启动线程\n%s"%e)

#print("\n建议同时在新的命令行终端分别同时运行以下命令：\npython3 autoSolve.py -s reverse\npython3 autoSolve.py -p 0\npython3 autoSolve.py -s reverse -p 0\n")
print("开始求解，请稍等%d秒..."%timeout)
auto_solve(map_data, issort, percent, timeout, threadName)