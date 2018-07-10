import sys, os
import random

here = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(here)
import Gacha

class GachaSimulation(Gacha.Gacha):
  def __init__(self):
    super().__init__()


  def roll_normal_gacha(self):
    character_list = self.get_list(self.get_rank_normal())
    return random.choice(character_list)

  def roll_special_gacha(self):
    character_list = self.get_list(self.get_rank_special())
    return random.choice(character_list)

  def is_completed(self, c_list):
    for key in c_list:
      if c_list[key] == 0:
        return False

    return True

  def roll_gacha_until_complete(self):
    #獲得したキャラを記憶しておく辞書作成
    self.got_character_list = {}

    #初期化
    for character in self.get_list(1):
      self.got_character_list[character] = 0

    for character in self.get_list(2):
      self.got_character_list[character] = 0

    for character in self.get_list(3):
      self.got_character_list[character] = 0

    gacha_count = 1

    while(1):
      #ノーマルガチャを9回
      for var in range(0, 9):
        self.got_character_list[self.roll_normal_gacha()] += 1

      #10回目のガチャを1回
      self.got_character_list[self.roll_special_gacha()] += 1

      if not self.is_completed(self.got_character_list):
        gacha_count += 1
        continue

      break

    return gacha_count


  def roll10(self):
    get_chara_list = []

    for var in range(0, 9):
      get_chara_list.append(self.roll_normal_gacha())

    get_chara_list.append(self.roll_special_gacha())

    return get_chara_list


if __name__ == '__main__':
  gs = GachaSimulation()

#  for i in range(0, 100000):
#    completed_count = gs.roll_gacha_until_complete()
#    print (completed_count)

  get_chara_list = gs.roll10()
  print (get_chara_list)

