# views/views.py
class Views:
    @staticmethod
    def show_message(text: str) -> None:
        print(text)

    @staticmethod
    def get_player_input(prompt: str) -> str:
        return input(f"{prompt} > ")

    @staticmethod
    def show_battle_status(monster, enemy) -> None:
        """
        【担当：メンバーB】
        お互いのHPやステータスをターミナルにわかりやすくprintする。
        """
        pass

    @staticmethod
    def show_training_options(points: int) -> None:
        """
        【担当：メンバーC】
        「〇〇pt獲得！」と、現在のステータスをprintして割り振りを促す。
        """
        pass