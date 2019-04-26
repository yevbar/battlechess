#!/usr/bin/env python3
import sys
import time
import random
import chess

def recursive_minimax(board, depth, my_turn):
  if depth == 0 or board.is_checkmate():
    return [board, evaluate(board)]

  if my_turn:
    winner = [None, 1000]
    for move in board.legal_moves:
      new_board = chess.Board(board.fen())
      new_board.push(move)
      mm = recursive_minimax(new_board, depth-1, False)
      if mm[1] < winner[1]:
        winner = mm
    return winner
  else: # not my_turn
    winner = [None, 1000]
    for move in board.legal_moves:
      new_board = chess.Board(board.fen())
      new_board.push(move)
      mm = recursive_minimax(new_board, depth-1, True)
      print("here is mm")
      print(mm)
      print("here is winner")
      print(winner)
      if mm[1] < winner[1]:
        winner = mm

def evaluate(board):
  if board is None:
    return -1000
  score = 0
  _PAWN = 1
  _KNIGHT = 3
  _BISHOP = 3
  _ROOK = 5
  _QUEEN = 9
  _KING = 100

  turn = board.turn

  for pawn in board.pieces(chess.PAWN, turn):
    score += _PAWN

  for knight in board.pieces(chess.KNIGHT, turn):
    score += _KNIGHT

  for bishop in board.pieces(chess.BISHOP, turn):
    score += _BISHOP

  for rook in board.pieces(chess.ROOK, turn):
    score += _ROOK

  for queen in board.pieces(chess.QUEEN, turn):
    score += _QUEEN
  
  for king in board.pieces(chess.KING, turn):
    score += _KING

  # the other side
  for pawn in board.pieces(chess.PAWN, (not turn)):
    score -= _PAWN

  for knight in board.pieces(chess.KNIGHT, (not turn)):
    score -= _KNIGHT

  for bishop in board.pieces(chess.BISHOP, (not turn)):
    score -= _BISHOP

  for rook in board.pieces(chess.ROOK, (not turn)):
    score -= _ROOK

  for queen in board.pieces(chess.QUEEN, (not turn)):
    score -= _QUEEN
  
  for king in board.pieces(chess.KING, (not turn)):
    score -= _KING

  return score

def get_move(board, limit=None):
  # TODO: Fill this in with an actual chess engine
  output = None
  
  moves = list(board.legal_moves)
  mm_winner = recursive_minimax(board,1,True) 
  last_move = None
  while board != mm_winner[0]:
    # print("this is the board")
    # print(board)
    # print("this is the mm_winner")
    # print(mm_winner[0])
    last_move = mm_winner[0].pop()
  return last_move

if __name__ == "__main__":
  while 1:
    cmd = input().split(" ")

    if cmd[0] == "uci":
      print("uciok")
    elif cmd[0] == "ucinewgame":
      pass
    elif cmd[0] == "isready":
      print("readyok")
    elif cmd[0] == "position":
      if cmd[1] == "startpos":
        board = chess.Board()
        if len(cmd) > 2 and cmd[2] == "moves":
          for m in cmd[3:]:
            board.push(chess.Move.from_uci(m))
    elif cmd[0] == "go":
      if len(cmd) > 1 and cmd[1] == "movetime":
        move = get_move(board, limit=int(cmd[2]))
      else:
        move = get_move(board)
      print("bestmove %s" % move)
    elif cmd[0] == "quit":
      exit(0)
      
