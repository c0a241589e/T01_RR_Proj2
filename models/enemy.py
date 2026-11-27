# models/enemy.py
import random
from models.character import Character
import random

class Enemy(Character):
    # 【担当：メンバーD】ここに敵のマスターデータを辞書で定義する
    ENEMY_DATA = {
    1: [
        {"name": "スライム", "hp": 5, "attack": 2, "defense": 1, "speed": 2, "reward": 2, "is_boss": False},
        {"name": "コウモリ", "hp": 6, "attack": 3, "defense": 1, "speed": 5, "reward": 3, "is_boss": False}
    ],
    2: [
        {"name": "ゴブリン", "hp": 8, "attack": 4, "defense": 2, "speed": 4, "reward": 4, "is_boss": False},
        {"name": "オーク", "hp": 12, "attack": 6, "defense": 4, "speed": 2, "reward": 6, "is_boss": False}
    ],
    3: [
        {"name": "ドラゴン", "hp": 20, "attack": 10, "defense": 7, "speed": 6, "reward": 10, "is_boss": False},
        {"name": "デーモン", "hp": 16, "attack": 12, "defense": 5, "speed": 9, "reward": 12, "is_boss": False},
        {"name": "魔王", "hp": 38, "attack": 20, "defense": 20, "speed": 20, "reward": 0, "is_boss": True}
    ]
    }

    def __init__(self, name: str, hp: int, attack: int, defense: int, speed: int, reward_points: int, is_boss: bool = False):
        super().__init__(name, hp, attack, defense, speed)
        self.reward_points = reward_points
        self.is_boss = is_boss

    @classmethod
    def create_enemy(cls, turn: int, player_total_stats: int = 0, is_boss: bool = False) -> 'Enemy':
        """
        【担当：メンバーD】
        1. 引数 is_boss に応じて ENEMY_DATA から該当する敵の名前を抽選する
        2. 選ばれた敵の基準ステータスを取得する
        3. 経過ターン(turn)を用いた計算式でステータスを強化する
        4. 強化済みのステータスで Enemy インスタンスを作成し return cls(...) する
        """

        # ボスの場合
        if is_boss:
            candidates = [
                enemy
                for tier_data in cls.ENEMY_DATA.values()
                for enemy in tier_data
                if enemy["is_boss"]
            ]
            base = random.choice(candidates)
            return cls(
                name=base["name"],
                hp=base["hp"],
                attack=base["attack"],
                defense=base["defense"],
                speed=base["speed"],
                reward_points=base["reward"],
                is_boss=True
            )

        # Danger_Levelの計算
        turn_level = (turn // 5) + 1
        player_level = (player_total_stats // 30) + 1
        danger_level = max(1, min(3, max(turn_level, player_level)))

        # Danger_LevelによるTier決定
        if danger_level == 1:
            enemy_tier = random.choices([1, 2], weights=[85, 15])[0]
        elif danger_level == 2:
            enemy_tier = random.choices([1, 2, 3], weights=[15, 70, 15])[0]
        else:
            enemy_tier = random.choices([2, 3], weights=[15, 85])[0]

        # 決定したTierから敵をランダムに選択
        enemy_data = random.choice(cls.ENEMY_DATA[enemy_tier])
        enemy_name = enemy_data["name"]
        base = enemy_data

        # Danger Levelと敵Tierの差によるステータス補正
        if enemy_tier < danger_level:
            enemy_name = "歴戦の" + enemy_name
            status_rate = 1.5
        elif enemy_tier > danger_level:
            enemy_name = "弱った" + enemy_name
            status_rate = 0.6
        else:
            status_rate = 1.0

        # ステータス補正
        hp = max(1, int(base["hp"] * status_rate))
        attack = max(1, int(base["attack"] * status_rate))
        defense = max(1, int(base["defense"] * status_rate))
        speed = max(1, int(base["speed"] * status_rate))

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
