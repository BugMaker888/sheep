from os.path import isfile
from mitmproxy import ctx
from autoSolve import auto_solve
import execjs
import json
import _thread


class Sheep():

    def __init__(self):
        self.seed = [0, 0, 0, 0]
        self.js_code = open("shuffle.js", encoding="utf-8").read()
        self.map_data_path = "./map_data.txt"

    def response(self, flow):
        """ 接口响应方法 """
        if "map_info_ex" in flow.request.path:
            # 获取随机种子的接口，随机种子存储到self.seed中
            response = json.loads(flow.response.content)
            self.seed = response["data"]["map_seed"]
            self.make_map_data()
        elif "maps" in flow.request.path:
            # 获取地图数据的接口，不解析第一关
            if "046ef1bab26e5b9bfe2473ded237b572" in flow.request.path:
                return
            # 保存地图数据
            response = json.loads(flow.response.content)
            with open(self.map_data_path, "w") as f:
                f.write(json.dumps(response, indent=4))
                f.close()
            self.make_map_data()

    def make_map_data(self):
        """ 制作地图数据 """

        print("==========================================")

        # 判断地图文件是否存在
        if not isfile(self.map_data_path):
            return

        # 读取原始地图数据
        map_data = json.loads(open(self.map_data_path).read())

        # 根据"blockTypeData"字段按顺序生成所有类型的方块，存放到数组
        block_type_data = map_data["blockTypeData"]
        block_types = []
        for i in range(1, 16+1):
            block_type = str(i)
            if block_type in block_type_data:
                count = block_type_data[block_type] * 3
                block_types.extend([i] * count)

        # 调用js方法将数组打乱，打乱后的结果和游戏的一样
        block_types = execjs.compile(self.js_code).call("shuffle", block_types, self.seed)
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
                    configs = {"issort":"","percent":0.85,"timeout":180}
                    with open("config.json","w",encoding="utf8") as f:
                        f.write(json.dumps(configs,indent=4))
                else:
                    print("\n将使用配置文件 config.json 的配置求解！")
            except:
                print("\n当前配置文件存在错误，将使用默认配置求解！")
                configs = {"issort":"","percent":0.85,"timeout":180}
                with open("config.json","w",encoding="utf8") as f:
                    f.write(json.dumps(configs,indent=4))
        else:
            print("\n当前配置文件不存在，将使用默认配置求解！")
            configs = {"issort":"","percent":0.85,"timeout":180}
            with open("config.json","w",encoding="utf8") as f:
                f.write(json.dumps(configs,indent=4))
        try:
            print("\n建议同时在新的命令行终端分别同时运行以下命令：\npython3 autoSolve.py -s reverse\npython3 autoSolve.py -p 0\npython3 autoSolve.py -s reverse -p 0\n")
            print("开始求解，请稍等%d秒..."%configs["timeout"])
            _thread.start_new_thread( auto_solve, (map_data,configs["issort"],configs["percent"],configs["timeout"],) )
        except Exception as e:
            print ("Error: 无法启动线程\n%s"%e)

addons = [Sheep()]
