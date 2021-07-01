chess_cardinals = [(1, 0), (0, 1), (-1, 0), (0, -1)]
chess_diagonals = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

class Piece:
    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol
        self.position = None
        self.at_initial_pos = True

    def __repr__(self):
        return self.symbol

    def __str__(self):
        return self.symbol

    def getValidMoves(self, x, y, game_board, color):
        # implementation in derived classes
        return

    def isValidMove(self, start_pos, end_pos, game_board, color):
        # checks if wished ending position is present in valid moves
        if end_pos in self.getValidMoves(start_pos[0], start_pos[1], game_board, color):
            return True
        return False

    def isInBounds(self, x, y):
        if x >= 0 and x < 8 and y >= 0 and y < 8:
            return True
        return False

    def isNotConflicting(self, x, y, game_board, piece_color):
        if self.isInBounds(x, y) and (((x, y) not in game_board) or game_board[(x, y)].color != piece_color):
            return True
        return False

    def getContinuousMoves(self, x, y, game_board, piece_color, base_moves):
        moves = []
        for x_base, y_base in base_moves:
            x_temp, y_temp = x + x_base, y + y_base
            while self.isInBounds(x_temp, y_temp):
                target_piece = game_board.get((x_temp, y_temp), None)
                if target_piece is None:
                    moves.append((x_temp, y_temp))
                elif target_piece.color != piece_color:
                    moves.append((x_temp, y_temp))
                    break
                else:
                    break
                x_temp, y_temp = x_temp + x_base, y_temp + y_base
        return moves


class King(Piece):
    def getKingMoves(self, x, y):
        return [(x + 1, y), (x + 1, y + 1), (x + 1, y - 1), (x, y + 1), (x, y - 1), (x - 1, y), (x - 1, y + 1), (x - 1, y - 1)]

    def getValidMoves(self, x, y, game_board, color):
        return [(xx, yy) for xx, yy in self.getKingMoves(x, y) if self.isNotConflicting(xx, yy, game_board, color)]


class Queen(Piece):
    def getValidMoves(self, x, y, game_board, color):
        return self.getContinuousMoves(x, y, game_board, color, chess_diagonals + chess_cardinals)


class Bishop(Piece):
    def getValidMoves(self, x, y, game_board, color):
        return self.getContinuousMoves(x, y, game_board, color, chess_diagonals)


class Knight(Piece):
    def getKnightMoves(self, x, y):
        return [(x+1, y+2), (x-1, y+2), (x+1, y-2), (x-1, y-2), (x+2, y+1), (x-2, y+1), (x+2, y-1), (x-2, y-1)]

    def getValidMoves(self, x, y, game_board, color):
        return [(xx, yy) for xx, yy in self.getKnightMoves(x, y) if self.isNotConflicting(xx, yy, game_board, color)]


class Rook(Piece):
    def getValidMoves(self, x, y, game_board, color):
        return self.getContinuousMoves(x, y, game_board, color, chess_cardinals)


class Pawn(Piece):
    def __init__(self, color, symbol, direction):
        self.color = color
        self.symbol = symbol
        self.direction = direction
        self.at_initial_pos = True

    def getValidMoves(self, x, y, game_board, color):
        moves = []
        if (x + 1, y + self.direction) in game_board and self.isNotConflicting(x + 1, y + self.direction, game_board, color):
            moves.append((x + 1, y + self.direction))
        if (x - 1, y + self.direction) in game_board and self.isNotConflicting(x - 1, y + self.direction, game_board, color):
            moves.append((x - 1, y + self.direction))
        if (x, y + self.direction) not in game_board:
            moves.append((x, y + self.direction))
        if self.at_initial_pos and (x, y + (2 * self.direction)) not in game_board:
            moves.append((x, y + (2 * self.direction)))
        return moves
