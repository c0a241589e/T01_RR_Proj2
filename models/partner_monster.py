# models/partner_monster.py
class PartnerMonster:
    def __init__(self):
        """
        【担当：メンバーD】
        初期ステータスを設定する。
        - hpを10に固定
        - attack, defense, speedを2〜6の範囲でランダムに決定する（randomモジュールを使用）
        """
        self.hp: int = 10
        self.attack: int = 0  # 後で乱数処理に書き換える
        self.defense: int = 0
        self.speed: int = 0

    def take_damage(self, amount: int) -> int:
        """
        【担当：メンバーB】
        ダメージを受ける処理。
        - self.hp から amount を引く
        - HPが0未満にならないように調整する
        - 実際に減ったダメージ量を return する
        """
        pass

    def boost_stats(self, target: str, points: int) -> None:
        """
        【担当：メンバーC】
        指定されたステータスを強化する。
        - targetが "attack" なら self.attack += points
        - defense, speed も同様に処理する
        """
        pass