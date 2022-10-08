import time
import json
from business.SheepSolver import SheepSolver
from func_timeout import func_set_timeout
from func_timeout.exceptions import FunctionTimedOut

if __name__ == '__main__':
    with open("map_data.json","r",encoding="utf8") as f:
        map_data = json.loads(f.read())
    sheep_solver = SheepSolver(map_data)
    sheep_solver.init_card_data()
    start_time = time.time()
    try:
        sheep_solver.solve()
        end_time = time.time()
        sheep_solver.print_result()
        print("计算用时: {}".format(end_time - start_time))
    except FunctionTimedOut:
        print("算法自动求解超时！建议放弃挑战并重新开始！")
