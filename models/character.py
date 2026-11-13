# models/character.py
class Character:
    def __init__(self, name: str, hp: int, attack: int, defense: int, speed: int):
        """
        敵と味方の共通ステータスを保持する。
        """
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed

    def is_alive(self) -> bool:
        """
        生存判定。HPが0より大きければTrueを返す。
        """
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        """
        【担当：メンバーB】
        1. self.hp から amount を引く。
        2. HPが0未満にならないように max(0, hp) で調整する。
        3. 【修正】実際に減ったダメージ量を計算し、return すること。
        """
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        return self.hp