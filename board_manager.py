import pickle
from global_objs import config


class BoardManager:
    @staticmethod
    def create_board(rows, cols, color):
        """
         创建一个rows行cols列，颜色初始为color的绘板
         其中color为颜色的十六进制表示
        """
        return [[color for j in range(cols)] for i in range(rows)]

    def __init__(self):
        self.board = {}

    def load_from_file(self, file):
        with open(file, "rb") as f:
            self.board = pickle.load(f)

    def save_to_file(self, file):
        with open(file, "wb") as f:
            pickle.dump(self.board, f)
    # 获取某群绘板

    def get_board(self, group_id):
        if group_id not in self.board:
            self.board[group_id] = BoardManager.create_board(
                *config.DEFAULT_SIZE, config.DEFAULT_COLOR)
        return self.board[group_id]
