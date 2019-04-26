#!/usr/bin/env python3
import sys
import time
import random
import chess

def recursive_minimax(board, depth, my_turn):
  if depth == 0 or board.is_checkmate():
    return [board, evaluate(board)]

  if my_turn:
    if depth >= 3:
      winner = [None, 1000]
      for move in board.legal_moves:
        new_board = board.copy()
        new_board.push(move)
        mm = recursive_minimax(new_board, depth-1, False)
        if mm[1] < winner[1]:
          winner = mm
      return winner
    else:
      winner = [None, -1000]
      best_moves = []
      for move in board.legal_moves:
        new_board = board.copy()
        new_board.push(move)
        best_moves.append([new_board, evaluate(new_board)])
      best_moves.sort(key=lambda x: x[1])
      for move in best_moves:
        mm = recursive_minimax(move[0], depth-1, False)
        if mm[1] > winner[1]:
          winner = mm
      return mm
  else:
    winner = [None, 1000]
    best_moves = []
    for move in board.legal_moves:
      new_board = board.copy()
      new_board.push(move)
      best_moves.append([new_board, evaluate(new_board)])
    best_moves.sort(key=lambda x: x[1], reverse=True)
    best_moves = best_moves[0:4]
    for move in best_moves:
      mm = recursive_minimax(move[0], depth-1, True)
      if mm[1] < winner[1]:
        winner = mm
    return winner

def evaluate(board):
  turn = board.turn
  score = 0

  for pawn in board.pieces(chess.PAWN, turn):
    score += 1

  for knight in board.pieces(chess.KNIGHT, turn):
    score += 3

  for bishop in board.pieces(chess.BISHOP, turn):
    score += 3

  for rook in board.pieces(chess.ROOK, turn):
    score += 5

  for queen in board.pieces(chess.QUEEN, turn):
    score += 9
  
  for king in board.pieces(chess.KING, turn):
    score += 100

  # the other side
  for pawn in board.pieces(chess.PAWN, (not turn)):
    score -= 1

  for knight in board.pieces(chess.KNIGHT, (not turn)):
    score -= 3

  for bishop in board.pieces(chess.BISHOP, (not turn)):
    score -= 3

  for rook in board.pieces(chess.ROOK, (not turn)):
    score -= 5

  for queen in board.pieces(chess.QUEEN, (not turn)):
    score -= 9
  
  for king in board.pieces(chess.KING, (not turn)):
    score -= 100

  return score

def get_move(board, limit=None):
  start = time.time()
  mm_winner = recursive_minimax(board,3,True) 
  last_move = None
  while board != mm_winner[0]:
    last_move = mm_winner[0].pop()
  print(time.time() - start)
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
      
