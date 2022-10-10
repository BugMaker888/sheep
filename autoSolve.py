import requests
import time
import json
import argparse
import os
import threading
import ctypes
import inspect
#from func_timeout.exceptions import FunctionTimedOut
from business.SheepSolver import SheepSolver


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
 
 
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def auto_solve(map_data, issort, percent):
    # 自动求解
    sheep_solver = SheepSolver(map_data)
    sheep_solver.init_card_data()
    start_time = time.time()
    if issort != "true" and issort != "reverse" and percent == 0.85:
        threadName = "普通模式"
    elif issort == "reverse" and percent == 0.85:
        threadName = "高层优先模式"
    elif issort != "true" and issort != "reverse" and percent == 0:
        threadName = "优先移除两张相同类型的手牌模式"
    elif issort == "reverse" and percent == 0:
        threadName = "高层优先且优先移除两张相同类型的手牌模式"
    #try:
    thread1 = threading.Thread(target=sheep_solver.solve, name=threadName, args=(issort, percent,))
    #sheep_solver.solve(issort, percent)
    thread1.start()
    print("启动线程：%s"%thread1.getName())
    second = 0
    # while second < 13:
    #     time.sleep(1)
    #     second += 1
    #     print("\r进度：%d/300"%second,end="")
    while True:
        #if (second-10)%5 == 0:
        if second%2 == 0:
            if thread1.is_alive() is False:
                break
        elif second >= 300:
            if thread1.is_alive():
                stop_thread(thread1)
                print("自动求解超时！当前算法有些力不从心，建议放弃挑战并重新开始！")
                print("==========================================")
                exit(0)
        time.sleep(1)
        second += 1
        print("\r进度：%d/300"%second,end="")
    #except FunctionTimedOut:
        #print("自动求解超时！当前算法有些力不从心，建议放弃挑战并重新开始！")
        #self.post_map_data(map_data)
    #else:
    end_time = time.time()
    result = sheep_solver.get_result()
    if result != "牌面无解":
        print("计算用时: {}".format(end_time - start_time))
        with open("map_data_oprations.json","w",encoding="utf8") as f:
            f.write(json.dumps(result, indent=4))
        print("当前关卡自动求解步骤已保存到当前路径下 map_data_oprations.json 文件！")
        print("==========================================")
        post_map_data(result)
    else:
        print("牌面无解！建议放弃挑战并重新开始！")
        print("==========================================")
        #self.post_map_data(map_data)


def post_map_data(map_data):
    # 提交关卡地图数据
    r = requests.post("https://ylgy.endless084.top", data=json.dumps(map_data, indent=4), headers={'Content-Type': 'application/json'})
    r_str = r.text
    url = r_str[r_str.rindex("sheep_map"):r_str.rindex("'")]
    if "id" not in url:
        print(r_str)
        print("\n3D地图生成失败！")
    else:
        url = "https://ylgy.endless084.top/%s"%url
        print("当前关卡3D地图地址：%s"%url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='羊了个羊自动求解')
    parser.add_argument('-s', '--issort', dest='issort', type=str, default="", help="是否对可选牌进行排序，默认不排序。\ntrue：从小到大排序\nreverse：从大到小排序\n为空或者其他：不排序")
    parser.add_argument('-p', '--percent', dest='percent', type=float, default=0.85, help="进度超过多少时优先移除已有两张相同类型的手牌，取值范围0~1。")
    parser.add_argument('-i', '--input', dest='input', type=str, default="map_data.json", help="关卡json数据文件路径，默认当前路径下 map_data.json。")
    args = parser.parse_args()
    if os.path.isfile(args.input):
        with open(args.input, "r", encoding="utf8") as f:
            try:
                map_data = json.loads(f.read())
            except:
                input("文件 %s 内容格式错误，无法读取，请确保文件内容为JSON！"%args.input)
                exit(1)
    else:
        input("文件 %s 不存在，请检查路径！"%args.input)
        exit(1)
    if args.percent > 1 or args.percent < 0:
        input("参数 percent[p] 取值范围为 0~1 !"%args.input)
        exit(1)
    print("开始求解，请稍等5分钟...")
    auto_solve(map_data, args.issort, args.percent)