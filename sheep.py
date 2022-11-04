from mitmproxy import ctx
import requests
import datetime
import execjs
import json
import os
import warnings
warnings.filterwarnings('ignore')


class Sheep():

    def __init__(self):
        self.js_code = open("shuffle.js", encoding="utf-8").read()
        self.map_data_dir = "./map_data"
        self.make_dir(self.map_data_dir)

    def response(self, flow):
        """ 接口响应方法 """
        if "game/map_info_ex" in flow.request.path or \
           "topic/game_start" in flow.request.path:
            # 获取地图信息
            response = json.loads(flow.response.content)
            self.make_map_data(response["data"])

    def make_dir(self, path):
        """ 创建目录 """
        if not os.path.exists(path):
            os.makedirs(path)

    def get_map_data(self, map_info):
        """ 获取游戏地图原始数据 """
        level2_map_md5 = map_info["map_md5"][1]
        map_data_path = f"{self.map_data_dir}/{level2_map_md5}.txt"
        print("地图数据文件路径:", map_data_path)

        # 从本地文件读取原始地图数据
        if os.path.isfile(map_data_path):
            map_data = json.loads(open(map_data_path).read())
            return map_data

        # 从服务器请求地图数据
        try:
            print("从服务器请求地图数据")
            map_data_url = f"https://cat-match-static.easygame2021.com/maps/{level2_map_md5}.txt"
            sesstion = requests.Session()
            sesstion.trust_env = False
            response = sesstion.get(map_data_url, verify=False, timeout=10)
            map_data = response.json()
            with open(map_data_path, "w") as f:
                f.write(json.dumps(map_data, indent=4))
                f.close()
            return map_data
        except Exception as e:
            print(e)

    def make_map_data(self, map_info):
        """ 制作地图数据 """

        print("==========================================")

        # 获取原始地图数据
        map_data = self.get_map_data(map_info)
        if not map_data:
            print("获取不到地图数据")
            return

        # 根据"blockTypeData"字段按顺序生成所有类型的方块，存放到数组
        block_type_data = map_data["blockTypeData"]
        block_types = []
        for i in range(1, 16+1):
            block_type = str(i)
            if block_type in block_type_data:
                count = block_type_data[block_type] * 3
                block_types.extend([i] * count)

        # 调用js方法将数组打乱，打乱后的结果和游戏的一样
        map_seed = map_info["map_seed"]
        block_types = execjs.compile(self.js_code).call(
            "shuffle", block_types, map_seed)
        print(block_types)

        # 将游戏的层数排序
        level_data = map_data["levelData"]
        layers = list(level_data.keys())
        layers.sort(key=lambda x: int(x))

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

        # 保存地图数据
        data_string = f"const map_data = {json.dumps(map_data, indent=4)};"
        with open("./html/map_data.js", "w") as f:
            f.write(data_string)
            f.close()

        print("==========================================")


addons = [Sheep()]
