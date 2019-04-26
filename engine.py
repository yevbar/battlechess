#!/usr/bin/env python3
import sys
import time
import random
import chess

def recursive_minimax(board, depth, my_turn):
  if depth == 0 or board.is_checkmate():
    return [board, evaluate(board)]

  if my_turn:
    winner = [None, -1000]
    for move in board.legal_moves:
      new_board = board
      new_board.push(move)
      mm = recursive_minimax(new_board, depth-1, False)
      if mm[1] > winner[1]:
        winner = mm
    return winner
  else: # not my_turn
    winner = [None, 1000]
    for move in board.legal_moves:
      new_board = board
      new_board.push(move)
      mm = recursive_minimax(new_board, depth-1, True)
      if mm[1] < winner[1]:
        winner = mm
    return winner

def minimax(board):
  depth = 3
  chain = []

  counter = 0
  while counter < depth:
    move_scores = []
    for move in board.legal_moves:
      board.push(move)
      move_scores.append([move, evaluate(board)])
      board.pop()
    move_scores  = sorted(move_scores, key=lambda x: x[1], reverse=(counter%2!=0))
    print("here are the move_scores")
    for a_move in move_scores:
      print(a_move)
    print("we are done printing move_scores")
    best = move_scores[0]
    # print(best)
    chain.append(move_scores[0])
    counter += 1

  print("this is what the current chain looks like")
  for thing in chain:
    print(thing)
  chain.sort(key=lambda x: x[1])
  return chain[0][0]
      
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
    #print(pawn)
    score += _PAWN

  for knight in board.pieces(chess.KNIGHT, turn):
    #print(knight)
    score += _KNIGHT

  for bishop in board.pieces(chess.BISHOP, turn):
    #print(bishop)
    score += _BISHOP

  for rook in board.pieces(chess.ROOK, turn):
    #print(rook)
    score += _ROOK

  for queen in board.pieces(chess.QUEEN, turn):
    #print(queen)
    score += _QUEEN
  
  for king in board.pieces(chess.KING, turn):
    #print(king)
    score += _KING

  # the other side
  for pawn in board.pieces(chess.PAWN, (not turn)):
    #print(pawn)
    score -= _PAWN

  for knight in board.pieces(chess.KNIGHT, (not turn)):
    #print(knight)
    score -= _KNIGHT

  for bishop in board.pieces(chess.BISHOP, (not turn)):
    #print(bishop)
    score -= _BISHOP

  for rook in board.pieces(chess.ROOK, (not turn)):
    #print(rook)
    score -= _ROOK

  for queen in board.pieces(chess.QUEEN, (not turn)):
    #print(queen)
    score -= _QUEEN
  
  for king in board.pieces(chess.KING, (not turn)):
    #print(king)
    score -= _KING

  return score

def get_move(board, limit=None):
  # TODO: Fill this in with an actual chess engine
  output = None
  
  moves = list(board.legal_moves)
  print("We are checking out the pieces at hand")
  # print(board.piece_map)
  # for move in moves:
    # print(move)
  print("The score is")
  # print(evaluate(board))
  minimax(board)
    
  #print("playing", move, file=sys.stderr)
  # output = random.choice(list(board.legal_moves))
  # output = minimax(board)
  # minimax winner
  mm_winner = recursive_minimax(board, 1, True)
  last_move = None
  while board != mm_winner:
    last_move = mm_winner.pop()
  return last_move

if __name__ == "__main__":
  while 1:
    cmd = input().split(" ")
    #print(cmd, file=sys.stderr)

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
      
