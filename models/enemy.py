# models/enemy.py
from models.character import Character
import random

class Enemy(Character):
    # 【担当：メンバーD】ここに敵のマスターデータを辞書で定義する
    ENEMY_DATA = {
        "スライム": {"hp": 5, "attack": 2, "defense": 1, "speed": 2, "reward": 2, "is_boss": False},
        "ゴブリン": {"hp": 8, "attack": 4, "defense": 2, "speed": 4, "reward": 4, "is_boss": False},
        "魔王": {"hp": 38, "attack": 20, "defense": 20, "speed": 20, "reward": 0, "is_boss": True}
    }

    def __init__(self, name: str, hp: int, attack: int, defense: int, speed: int, reward_points: int, is_boss: bool = False):
        super().__init__(name, hp, attack, defense, speed)
        self.reward_points = reward_points
        self.is_boss = is_boss

    @classmethod
    def create_enemy(cls, turn: int, is_boss: bool = False) -> 'Enemy':
        """
        【担当：メンバーD】
        1. 引数 is_boss に応じて ENEMY_DATA から該当する敵の名前を抽選する
        2. 選ばれた敵の基準ステータスを取得する
        3. 経過ターン(turn)を用いた計算式でステータスを強化する
        4. 強化済みのステータスで Enemy インスタンスを作成し return cls(...) する
        """
        candidates = [
            name for name, data in cls.ENEMY_DATA.items()
            if data["is_boss"] == is_boss
        ]

        # 敵をランダムに選択
        enemy_name = random.choice(candidates)

        # 選ばれた敵の基準ステータスを取得
        base = cls.ENEMY_DATA[enemy_name]

        if is_boss:
            hp = base["hp"]
            attack = base["attack"]
            defense = base["defense"]
            speed = base["speed"]
        else:
            growth = turn // 3  # 3ターンごとに +1 段階
            hp = base["hp"] + growth * 2
            attack = base["attack"] + growth
            defense = base["defense"] + growth // 2
            speed = base["speed"] + growth // 2

        # 4. インスタンス生成
        return cls(
            name=enemy_name,
            hp=hp,
            attack=attack,
            defense=defense,
            speed=speed,
            reward_points=base["reward"],
            is_boss=is_boss,
        )
