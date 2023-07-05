class GoString():  # 棋链是一系列同色且相连的棋子
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = stones
        self.liberties = liberties

    def remove_liberty(self, point):
        self.liberties.remove(point)

    def add_liberty(self, point):
        self.liberties.add(point)

    def merged_with(self, go_string):  # 返回一条新的棋链，包含两条棋链的所有棋子
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones
        )

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties


class Board():  # 棋盘初始化魏一个空网络，其尺寸由行数和列数这两个参数决定
    def __int__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}

    def place_stone(self, player, point):
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        for neighbor in point.neighbors():
            if not self.is_on_grid(neighbor):
                continue
            neighbor_string = self._grid.get(neighbor)
            if neighbor_string is None:
                liberties.append(neighbor)
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)
        new_string = GoString(player, [point], liberties)
        for same_color_string in adjacent_same_color:  # 合并任何同色相邻的棋链
            new_string = new_string.merged_with(same_color_string)
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string
        for other_color_string in adjacent_opposite_color:  # 减少对方相邻棋链的气
            other_color_string.remove_liberty(point)
        for other_color_string in adjacent_opposite_color:  # 如果对方的某条棋链气尽了，就提走它们
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)

    def is_on_grid(self, point):
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols

    def get(self, point):  # 返回棋盘某个交叉点的内容：如果该交叉点已经落子，则返回对应的Play对象：否则返回None
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color

    def get_go_string(self, point):  # 返回一个交叉点上的整条棋链：如果棋链中的一颗棋子落在这个交叉点上，则返回它的GoString对象：否则返回None
        string = self._grid.get(point)
        if string is None:
            return None
        return string

    def _remove_string(self, string):
        for point in string.stones:
            for neighbor in point.neighbors():  # 提走一条棋链可以为其他棋链增加气数
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    neighbor_string.add_liberty(point)
            self._grid[point] = None


class Move():  # 这里可以设置棋手在回合中所能采取的任一种动作: is_play、is_pass 或 is_resign
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):  # 这个动作是在棋盘上落下一颗棋子
        return Move(point=point)

    @classmethod
    def pass_trun(cls):  # 这个动作是跳过回合
        return Move(is_pass=True)

    @classmethod
    def resign(cls):  # 这个动作是直接认输
        return Move(is_resign=True)
