import sys
import os
import time

POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2
DEFAULT_MODE = 0
ADDITION_OP = 1
MULTIPLY_OP = 2
INPUT_OP = 3
OUTPUT_OP = 4
JUMP_IF_TRUE_OP = 5
JUMP_IF_FALSE_OP = 6
LESS_THAN_OP = 7
EQUALS_OP = 8
RELATIVE_BASE_OFFSET_OP = 9
HALT_OP = 99

class Computer():
  def __init__(self, program):
    self._program = program
    self.reset_memory()

  def _modeless_read(self, pointer):
    return self._memory.get(int(pointer)) or '0'

  def read(self, mode, pointer):
    if mode == POSITION_MODE:
      position = int(self._modeless_read(pointer))
      return self._modeless_read(position)
    elif mode == IMMEDIATE_MODE:
      return self._modeless_read(pointer)
    elif mode == RELATIVE_MODE:
      offset = int(self._modeless_read(pointer))
      return self._modeless_read(offset + self._relative_base)

  def write(self, mode, pointer, value):
    if mode == POSITION_MODE or mode == IMMEDIATE_MODE:
      address = int(self._modeless_read(pointer))
    if mode == RELATIVE_MODE:
      address = int(self._modeless_read(pointer)) + self._relative_base

    self._memory[address] = str(value)

  def reset_memory(self):
    instructions = self._program.split(',')
    memory = {}

    for i in range(len(instructions)):
      memory[i] = instructions[i]

    self._memory = memory
    self._pointer = 0
    self._relative_base = 0

  def run(self, input_value = None):
    i = self._pointer

    while True:
      instruction = self._modeless_read(i)
      op_code = int(instruction[-2:])
      param_modes = instruction[:-2][::-1]
      param_1_mode = int(param_modes[0]) if len(param_modes) else DEFAULT_MODE
      param_2_mode = int(param_modes[1]) if len(param_modes) > 1 else DEFAULT_MODE
      param_3_mode = int(param_modes[2]) if len(param_modes) > 2 else DEFAULT_MODE

      if op_code == ADDITION_OP:
        value_1 = self.read(param_1_mode, i + 1)
        value_2 = self.read(param_2_mode, i + 2)

        self.write(param_3_mode, i + 3, int(value_1) + int(value_2))

        i += 4
      elif op_code == MULTIPLY_OP:
        value_1 = self.read(param_1_mode, i + 1)
        value_2 = self.read(param_2_mode, i + 2)

        self.write(param_3_mode, i + 3, int(value_1) * int(value_2))

        i += 4
      elif op_code == INPUT_OP:
        value = input_value
        #print(value)

        self.write(param_1_mode, i + 1, value)

        i += 2
      elif op_code == OUTPUT_OP:
        value = self.read(param_1_mode, i + 1)
        #print(value)

        i += 2

        self._pointer = i
        return value
      elif op_code == JUMP_IF_TRUE_OP:
        value_1 = self.read(param_1_mode, i + 1)
        value_2 = self.read(param_2_mode, i + 2)

        if int(value_1) != 0:
          i = int(value_2)
        else:
          i += 3
      elif op_code == JUMP_IF_FALSE_OP:
        value_1 = self.read(param_1_mode, i + 1)
        value_2 = self.read(param_2_mode, i + 2)

        if int(value_1) == 0:
          i = int(value_2)
        else:
          i += 3
      elif op_code == LESS_THAN_OP:
        value_1 = self.read(param_1_mode, i + 1)
        value_2 = self.read(param_2_mode, i + 2)

        self.write(param_3_mode, i + 3, '1' if int(value_1) < int(value_2) else '0')

        i += 4
      elif op_code == EQUALS_OP:
        value_1 = self.read(param_1_mode, i + 1)
        value_2 = self.read(param_2_mode, i + 2)

        self.write(param_3_mode, i + 3, '1' if value_1 == value_2 else '0')

        i += 4
      elif op_code == RELATIVE_BASE_OFFSET_OP:
        value = self.read(param_1_mode, i + 1)

        self._relative_base += int(value)

        i += 2
      elif op_code == HALT_OP:
        return

program = sys.stdin.read()
computer = Computer(program)

BOARD_WIDTH = 41
BOARD_HEIGHT = 25
EMPTY = ' '
WALL = '+'
BLOCK = 'X'
PADDLE = '='
BALL = 'o'

board = []
ball_position = None
paddle_position = None
next_move = '0'
score = '0'

# try to align paddle with ball
def find_next_move(ball, paddle):
  if ball[0] < paddle[0]:
    return '-1'
  elif ball[0] > paddle[0]:
    return '1'
  else:
    return '0'

def draw_board(board, score, filename):
  visualization = ''

  for i in range(BOARD_WIDTH * BOARD_HEIGHT):
    visualization += board[i]

    if i > 1 and (i + 1) % BOARD_WIDTH == 0:
      visualization += '\n'

  visualization += 'SCORE: '+score
  #f = open('board/'+filename+'.txt','w+')
  #f.write(visualization)
  #f.close()
  sys.stdout.write(visualization)
  sys.stdout.flush()

# first set of outputs draw the initial board
for _ in range(BOARD_WIDTH * BOARD_HEIGHT):
  x = computer.run(next_move)
  y = computer.run(next_move)
  tile_id = computer.run(next_move)

  if tile_id == '0':
    board.append(EMPTY)
  elif tile_id == '1':
    board.append(WALL)
  elif tile_id == '2':
    board.append(BLOCK)
  elif tile_id == '3':
    board.append(PADDLE)
    paddle_position = (int(x), int(y))
  elif tile_id == '4':
    board.append(BALL)
    ball_position = (int(x), int(y))

next_move = find_next_move(ball_position, paddle_position)

# read the initial score
for _ in range(1):
  x = computer.run(next_move)
  y = computer.run(next_move)
  score = computer.run(next_move)

draw_board(board, score, '0')
i = 1

# play the game until it halts
while True:
  x = computer.run(next_move)
  y = computer.run(next_move)
  tile_id = computer.run(next_move)

  if x == None:
    break

  time.sleep(0.01)
  os.system('cls' if os.name == 'nt' else 'clear')

  if x == '-1':
    score = tile_id

  index = (int(y) * BOARD_WIDTH) + int(x)

  if tile_id == '0':
    board[index] = EMPTY
  elif tile_id == '1':
    board[index] = WALL
  elif tile_id == '2':
    board[index] = BLOCK
  elif tile_id == '3':
    board[index] = PADDLE
    paddle_position = (int(x), int(y))
  elif tile_id == '4':
    board[index] = BALL
    ball_position = (int(x), int(y))

  next_move = find_next_move(ball_position, paddle_position)
  draw_board(board, score, str(i))
  i += 1
