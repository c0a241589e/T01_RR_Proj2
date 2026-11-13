# models/enemy.py
import random
from models.character import Character

class Enemy(Character):
    # 【担当：メンバーD】ここに敵のマスターデータを辞書で定義する
    ENEMY_DATA = {
        "スライム": {"hp": 5, "attack": 2, "defense": 1, "speed": 2, "reward": 2, "is_boss": False},
        "ゴブリン": {"hp": 8, "attack": 4, "defense": 2, "speed": 4, "reward": 4, "is_boss": False},
        "魔王": {"hp": 30, "attack": 10, "defense": 10, "speed": 8, "reward": 0, "is_boss": True}
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
        # ENEMY_DATA から is_boss が一致する敵を抽選し、報酬ポイントを取得する
        candidates = [name for name, data in cls.ENEMY_DATA.items() if data["is_boss"] == is_boss]
        name = random.choice(candidates)
        reward = cls.ENEMY_DATA[name]["reward"]

        # ※ステータスは仮の値（メンバーDが ENEMY_DATA ＋ターン補正で実装予定）
        if is_boss:
            return cls(
                name=name, hp=10, attack=5, defense=5, speed=5, reward_points=reward, is_boss=True
            )

        else:
            return cls(
                name=name, hp=3, attack=2, defense=1, speed=2, reward_points=reward, is_boss=False
            )