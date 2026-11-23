"""
    0  1  2  3  4  5  6  7
0   a8 b8 c8 d8 e8 f8 g8 h8
1   a7 b7 c7 d7 e7 f7 g7 h7
2   a6 b6 c6 d6 e6 f6 g6 h6
3   a5 b5 c5 d5 e5 f5 g5 h5
4   a4 b4 c4 d4 e4 f4 g4 h4
5   a3 b3 c3 d3 e3 f3 g3 h3
6   a2 b2 c2 d2 e2 f2 g2 h2
7   a1 b1 c1 d1 e1 f1 g1 h1
"""


class Square:

    def __init__(self, file=-1, rank=-1, empty=True):
        self.file = file
        self.rank = rank

        # For drawing a piece's legal moves as grey circles / rings
        self.empty = empty

    def __hash__(self):
        return hash((self.file, self.rank))

    def __str__(self) -> str:
        if self.file < 0 or self.rank < 0:
            return '-'
        file = 'abcdefgh'[self.file]
        rank = '87654321'[self.rank]
        return file + rank

    def __eq__(self, other: 'Square') -> bool:
        return self.file == other.file and self.rank == other.rank

    def coords(self, flip=False) -> tuple[int, int]:
        if not flip:
            return self.file, self.rank
        return 7 - self.file, 7 - self.rank

    def is_light_square(self) -> bool:
        return (self.file + self.rank) % 2 == 0
