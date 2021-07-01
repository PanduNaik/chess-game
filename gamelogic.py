from pieces import *

WHITE = "white"
BLACK = "black"

class Game:
    def __init__(self):
        self.players_turn = WHITE
        self.game_board = {}
        self.dead_pieces = {WHITE: [], BLACK: []}
        self.temp_moves = []

    def validateStart(self, start):
        x = ord(start[0])-65
        y = int(start[1])-1
        start_pos = (x, y)
        if start_pos not in self.game_board:
            return (False, "No Piece Found!", None)
        target = self.game_board[start_pos]
        if target.color != self.players_turn:
            return (False, "It's not your turn! Please wait for your turn", None)
        self.temp_moves = target.getValidMoves(x, y, self.game_board, target.color)
        self.temp_moves = list(map(lambda x: chr(65+x[0]) + str(x[1]+1), self.temp_moves))
        if len(self.temp_moves) == 0:
            return (False, "No valid moves!", self.temp_moves)
        return (True, "valid", self.temp_moves)

    def canSeeKing(self, king_pos, pieces_list):
        for piece, pos in pieces_list:
            if piece.isValidMove(pos, king_pos, self.game_board, piece.color):
                return True
        return False

    def isInCheck(self):
        in_check = {WHITE: False, BLACK: False, 'white_king': None, 'black_king': None}
        king_pos = {WHITE: None, BLACK: None}
        pieces_list = {WHITE: [], BLACK: []}
        for pos, piece in self.game_board.items():
            if type(piece) == King:
                king_pos[piece.color] = pos
            pieces_list[piece.color].append((piece, pos))
        if self.canSeeKing(king_pos[WHITE], pieces_list[BLACK]):
            in_check[WHITE] = True
            in_check['white_king'] = chr(king_pos[WHITE][0] + 65) + str(king_pos[WHITE][1] + 1)
        if self.canSeeKing(king_pos[BLACK], pieces_list[WHITE]):
            in_check[BLACK] = True
            in_check['black_king'] = chr(king_pos[BLACK][0] + 65) + str(king_pos[BLACK][1] + 1)
        return in_check

    def isCheckMate(self, color):
        no_mate = False
        king_pos = None
        pieces_list = {WHITE: [], BLACK: []}
        for pos, piece in self.game_board.items():
            if type(piece) == King and color == piece.color:
                king_pos = pos
            pieces_list[piece.color].append((piece, pos))
        for piece, start_pos in pieces_list[color]:
            moves_list = piece.getValidMoves(start_pos[0], start_pos[1], self.game_board, color)
            for end_pos in moves_list:
                target = None
                if end_pos in self.game_board:
                    target = self.game_board[end_pos]
                self.game_board[end_pos] = piece
                del self.game_board[start_pos]
                if self.isInCheck()[color] == False:
                    no_mate = True
                self.game_board[start_pos] = piece
                if target:
                    self.game_board[end_pos] = target
                else:
                    del self.game_board[end_pos]
                if no_mate:
                    return False
        return True

    def validateEnd(self, start, end):
        res = {'valid': False,
               'self-check': False,
               'opp-check': False,
               'check-mate': False,
               'kill': False,
               'opp-color': None,
               'king-pos': None,
               'start-icon': None,
               'end-icon': None,
               'msg': None}
        start_pos = (ord(start[0])-65, int(start[1])-1)
        end_pos = (ord(end[0])-65, int(end[1])-1)
        target = self.game_board[start_pos]
        res['start-icon'] = target.symbol
        dead_piece = None
        if end_pos in self.game_board:
            dead_piece = self.game_board[end_pos]
        self.game_board[end_pos] = self.game_board[start_pos]
        del self.game_board[start_pos]
        in_check = self.isInCheck()
        if in_check[target.color]:
            self.game_board[start_pos] = self.game_board[end_pos]
            if dead_piece:
                self.game_board[end_pos] = dead_piece
            else:
                del self.game_board[end_pos]
            res['self-check'] = True
            res['msg'] = "Invalid Move! You will get into check"
            return res
        res['valid'] = True
        res['msg'] = "It's a Valid Move!"
        opp_color = BLACK if target.color == WHITE else WHITE
        if dead_piece:
            res['kill'] = True
            res['opp-color'] = opp_color
            res['end-icon'] = dead_piece.symbol
        if in_check[opp_color]:
            res['opp-check'] = True
            res['king-pos'] = in_check['white_king'] if opp_color == WHITE else in_check['black_king']
            res['msg'] = opp_color + " player is in check!"
            if self.isCheckMate(opp_color):
                res['check-mate'] = True
                res['msg'] = "Check n Mate!\n" + opp_color + " player lose!"
                return res
        target.at_initial_pos = False
        if self.players_turn == WHITE:
            self.players_turn = BLACK
        else:
            self.players_turn = WHITE
        return res
