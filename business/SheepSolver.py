import copy
import json
#import os
#import sys
#from hepler.FileHelper import FileHelper
from item.Card import Card
from item.CardPosition import CardPosition
from item.ResidualPool import ResidualPool
#from func_timeout import func_set_timeout


class SheepSolver(object):
    def __init__(self, map_data):
        self.map_data = map_data
        slove_map_data = {}
        for level, data_list in map_data["levelData"].items():
            slove_map_data[level] = []
            for data_item in data_list:
                slove_item = {"type": data_item["type"],
                "min_x": data_item["rolNum"],
                "min_y": data_item["rowNum"],
                "max_x": data_item["rolNum"] + 8,
                "max_y": data_item["rowNum"] + 8}
                slove_map_data[level].append(slove_item)
        self._origin_data = slove_map_data
        self._card_count = 0
        self._card_position = CardPosition()
        self._residual_pool = ResidualPool()
        self._pick_list = []
        self._situation_history = set()
        self.picked_list = []

    def init_card_data(self):
        self._origin_data = dict(sorted(self._origin_data.items(), key=lambda item: int(item[0])))
        for level, level_data in self._origin_data.items():
            self._card_count += len(level_data)
            card_list = [Card(item) for item in level_data]
            self._card_position.append_level_card(card_list)
        self._card_position.generate_head_data()

    #@func_set_timeout(300)
    def solve(self, issort, percent):
        #print("\r当前进度为: {}/{}".format(len(self._pick_list), self._card_count), end="")
        if (len(self._pick_list)/self._card_count) >= percent:
            pool_card = copy.deepcopy(self._residual_pool._pool_card)
            for i in pool_card.keys():
                if pool_card[i] == 2:
                    if issort == "true":
                        head_list = sorted(self._card_position.get_head_key_list())
                    elif issort == "reverse":
                        head_list = sorted(self._card_position.get_head_key_list(), reverse=True)
                    else:
                        head_list = self._card_position.get_head_key_list()
                    for j in head_list:
                        original_data = self._card_position.get_card_detail(j)._origin_data
                        if original_data["type"] == i:
                            self._operation_pick_card(j)
                            head_fingerprint = self._card_position.get_head_description()
                            if head_fingerprint in self._situation_history:
                                self._operation_recover_card(j)
                                continue
                            else:
                                self._situation_history.add(head_fingerprint)
                                if self._residual_pool.is_pool_full():
                                    self._operation_recover_card(j)
                                    continue
                                self.solve(issort, percent)
                                if self.picked_list != []:
                                    return True
                                if not self._card_position.is_head_data_empty():
                                    self._operation_recover_card(j)
                                else:
                                    self.picked_list = self._pick_list
                                    return True
                            break
                    break
        if issort == "true":
            head_list = sorted(self._card_position.get_head_key_list())
        elif issort == "reverse":
            head_list = sorted(self._card_position.get_head_key_list(), reverse=True)
        else:
            head_list = self._card_position.get_head_key_list()
        for head_item in head_list:
            self._operation_pick_card(head_item)
            head_fingerprint = self._card_position.get_head_description()
            if head_fingerprint in self._situation_history:
                self._operation_recover_card(head_item)
                continue
            else:
                self._situation_history.add(head_fingerprint)
                if self._residual_pool.is_pool_full():
                    self._operation_recover_card(head_item)
                    continue
                self.solve(issort, percent)
                if self.picked_list != []:
                    return True
                if not self._card_position.is_head_data_empty():
                    self._operation_recover_card(head_item)
                else:
                    self.picked_list = self._pick_list
                    return True

    def test_result(self, pick_list: list):
        for pick_index in pick_list:
            self._operation_pick_card(pick_index)
            print(self._residual_pool.show_pool_state())

    def _operation_pick_card(self, card_index):
        self._card_position.pick_card(card_index)
        card_detail = self._card_position.get_card_detail(card_index)
        self._residual_pool.pick_card(card_detail)
        self._pick_list.append(card_index)

    def _operation_recover_card(self, card_index):
        self._card_position.recover_card(card_index)
        card_detail = self._card_position.get_card_detail(card_index)
        self._residual_pool.recover_card(card_detail)
        self._pick_list.remove(card_index)

    def print_result(self):
        if self.picked_list != []:
            print(json.dumps(self.picked_list))
        else:
            print("牌面无解")

    def get_result(self):
        if self.picked_list != []:
            operations = []
            for i in self.picked_list:
                count = 0
                for data_list in self.map_data["levelData"].values():
                    for data_item in data_list:
                        count += 1
                        if count == i:
                            operations.append(data_item["id"])
                            break
                    if count == i:
                        break
            self.map_data["operations"] = operations
            return self.map_data
        else:
            return "牌面无解"

