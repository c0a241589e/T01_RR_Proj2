# views/views.py
from typing import Dict, Any

class Views:
    @staticmethod
    def show_message(text: str) -> None:
        """ 汎用的なメッセージ表示 """
        print(text)

    @staticmethod
    def get_player_input(prompt: str) -> str:
        """ 汎用的な入力受け付け """
        return input(f"{prompt} > ")

    @staticmethod
    def show_map(map_data, hints: dict) -> None:
        """
        【担当：リーダー】
        5x5のマップの現在地と、上下左右のヒントを表示する。
        """
        pass

    @staticmethod
    def show_battle_status(monster, enemy) -> None:
        """
        【担当：メンバーB】
        プレイヤーと敵の現在のHP・ステータスを比較できるように表示する。
        """
        pass

    @staticmethod
    def show_training_options(points: int) -> None:
        """
        【担当：メンバーC】
        「〇〇pt獲得！」と現在のステータスを表示し、割り振りを促す。
        """
        pass

    @staticmethod
    def show_event_options(event_data: Dict[str, Any]) -> None:
        """
        【担当：メンバーC】
        イベントのテキストと選択肢を表示する。
        """
        pass