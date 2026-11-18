# models/enemy.py
import random
from models.character import Character
import random

class Enemy(Character):
    # 【担当：メンバーD】ここに敵のマスターデータをTier（階層）管理の辞書構造で定義する
    ENEMY_DATA = {
        1: [
            {"name": "スライム", "hp": 5, "attack": 2, "defense": 1, "speed": 2, "reward": 2},
            # TODO: Tier 1（序盤・弱め）の敵データを追加する
        ],
        2: [
            {"name": "ゴブリン", "hp": 8, "attack": 4, "defense": 2, "speed": 4, "reward": 4},
            # TODO: Tier 2（中盤・中堅）の敵データを追加する
        ],
        3: [
            # TODO: Tier 3（終盤・強敵）の敵データを追加する
        ],
        "boss": [
            {"name": "魔王", "hp": 38, "attack": 20, "defense": 20, "speed": 20, "reward": 0},
            # TODO: ボス敵データを追加・調整する
        ],
    }

    def __init__(self, name: str, hp: int, attack: int, defense: int, speed: int, reward_points: int, is_boss: bool = False):
        super().__init__(name, hp, attack, defense, speed)
        self.reward_points = reward_points
        self.is_boss = is_boss

    @classmethod
    def create_enemy(cls, turn: int, player_total_stats: int = 0, is_boss: bool = False) -> 'Enemy':
        """
        【担当：メンバーD】
        1. turn と player_total_stats から Danger Level (1〜3) を算出する
        2. 確率(70%, 15%, 15%)で抽選Tierを決定する
        3. Danger Level と Tier の差分から「二つ名」を付与し、ステータス倍率補正をかける
        4. 補正後のステータスでインスタンスを生成しreturnする
        """
        # TODO: 1. turn と player_total_stats から Danger Level (1〜3) を算出する
        # TODO: 2. is_boss が True なら "boss" Tier、False なら確率(70%, 15%, 15%)で抽選Tierを決定し、敵データを抽選する
        # TODO: 3. Danger Level と Tier の差分から「二つ名」を付与し、ステータス倍率補正をかける
        # TODO: 4. 補正後のステータスで Enemy インスタンスを生成し return cls(...) する
        pass
