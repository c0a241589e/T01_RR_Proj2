# models/partner_monster.py
from models.character import Character
import random

class PartnerMonster(Character):
    def __init__(self):
        """
        【担当：メンバーD】
        初期ステータスのランダム生成。
        - hp=10 で親クラス(Character)を初期化する
        - attack, defense, speed を 2〜6 の乱数で生成してセットする
        """

        super().__init__(name="相棒", hp=10, attack=random.randint(2, 6), defense=random.randint(2, 6), speed=random.randint(2, 6),)
        # ここに乱数処理を書く
        


    def heal(self, amount: int) -> None:
        """
        【担当：メンバーC】
        回復処理。
        - self.hp に amount を足す
        - 最大HP (self.max_hp) を超えないように調整する
        """
        pass

    def boost_single_stat(self, target: str, points: int) -> None:
        """
        【担当：メンバーC】育成用
        引数 target ("attack", "defense", "speed"のいずれか) のステータスに points を加算する。
        """
        pass

    def distribute_reward(self, distribution: dict) -> None:
        """
        【担当：メンバーC】戦闘勝利時用
        引数 distribution (例: {"hp": 1, "attack": 2...}) の中身を取り出し、
        それぞれのステータスに加算する。hp の場合は max_hp も同時に上げる。
        """
        pass