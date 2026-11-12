import os, sys, io
import M5
from M5 import *
from hardware import Timer

import random


# DATA CLASSES

# A direction.
# Enumeration.
class AbsoluteDirection:
  up = 0
  right = 1
  down = 2
  left = 3

# A relative direction.
# Enumeration.
class RelativeDirection:
  left = 0
  right = 1

# The given absolute direction rotated in
# the given relative direction.
def rotate(absolute_direction, relative_direction):
  result = absolute_direction
  if relative_direction == RelativeDirection.left:
    result -= 1
    if result < 0:
      result = 3
  else:
    result += 1
    if result > 3:
      result = 0
  return result

# A location on the grid.
# Immutable.
class Location:
  # The minimum in-bounds x value (inclusive).
  min_x = 0
  # The first out-of-bounds x value (exclusive).
  max_x = 16
  # The minimum in-bounds y value (inclusive).
  min_y = 0
  # The first out-of-bounds y value (exclusive).
  max_y = 12

  # A Location with the given x and y coordinates.
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  # A copy of this Location moved in the given direction.
  def move(self, direction):
    if direction == AbsoluteDirection.up:
      return Location(self.x, self.y - 1)
    elif direction == AbsoluteDirection.right:
      return Location(self.x + 1, self.y)
    elif direction == AbsoluteDirection.down:
      return Location(self.x, self.y + 1)
    else: # direction == AbsoluteDirection.left
      return Location(self.x - 1, self.y)

  # Whether this location is in bounds.
  def in_bounds(self):
    return (
      self.x >= Location.min_x and
      self.x < Location.max_x and
      self.y >= Location.min_y and
      self.y < Location.max_y
    )


# GRAPHICS

class Graphics:
  @classmethod
  def clear_screen(_):
    M5.Lcd.clear()

  @classmethod
  def color_location(_, location, color):
    grid_tile_size = 20
    M5.Lcd.fillRect(
      x = location.x * grid_tile_size,
      y = location.y * grid_tile_size,
      w = grid_tile_size,
      h = grid_tile_size,
      color = color,
    )


# LOGIC

# A snake.
class Snake:
  def __init__(self):
    self.locations = [
      Location(1, 5),
      Location(2, 5),
      Location(3, 5),
    ]
    self.direction = AbsoluteDirection.right

  def render(self):
    for location in self.locations:
      Graphics.color_location(location, 0x11FF11)

  def turn(self, relative_direction):
    self.direction = rotate(self.direction, relative_direction)

  # Returns whether the game is over.
  def move_and_render(self, apple):
    current_head_location = self.locations[-1]
    new_head_location = current_head_location.move(self.direction)

    consumed_apple = new_head_location == apple.location

    if not new_head_location.in_bounds():
      return True
    
    if not consumed_apple:
      old_tail_location = self.locations.pop(0)
      Graphics.color_location(old_tail_location, 0x000000)

    if new_head_location in self.locations:
      return True

    self.locations.append(new_head_location)

    if consumed_apple:
      apple.teleport_and_render(self)

    # We must render this after the apple teleports,
    # since the apple will leave black in its place.
    Graphics.color_location(new_head_location, 0x11FF11)

    return False

# A apple. (Dennis the Menace reference.)
class Apple:
  def __init__(self):
    self.location = Location(10, 5)

  def render(self):
    Graphics.color_location(self.location, 0xFF1111)

  def teleport_and_render(self, snake):
    available_locations = [
      Location(i, j)
      for i in range(Location.max_x)
      for j in range(Location.max_y)
    ]
    for location in snake.locations:
      available_locations.remove(location)
    Graphics.color_location(self.location, 0x000000)
    self.location = random.choice(available_locations)
    Graphics.color_location(self.location, 0xFF1111)


# A game. Exposes high-level reset and input functions.
class Game:
  def __init__(self):
    self.reset()

  # Reset the game.
  def reset(self):
    self.active = False

    self.turn_queue = []

    self.snake = Snake()
    self.apple = Apple()

    Graphics.clear_screen()
    self.snake.render()
    self.apple.render()

  # Start the game.
  def start(self):
    if self.active:
      return

    self.active = True

  # Move the snake and update game state accordingly.
  def tick(self):
    if not self.active:
      return

    if self.turn_queue:
      relative_direction = self.turn_queue.pop(0)
      self.snake.turn(relative_direction)

    game_over = self.snake.move_and_render(self.apple)
    if game_over:
      self.reset()

  # Register a left input from the user.
  def register_input_left(self):
    if not self.active:
      return

    if len(self.turn_queue) < 2:
      self.turn_queue.append(RelativeDirection.left)

  # Register a right input from the user.
  def register_input_right(self):
    if not self.active:
      return

    if len(self.turn_queue) < 2:
      self.turn_queue.append(RelativeDirection.right)


# STATE

# Initialized in `setup`.
game = None
ticker = Timer(0)


# EVENTS

def on_ticker_tick(_):
  game.tick()

def on_btna_pressed(_):
  game.register_input_left()

def on_btnb_pressed(_):
  game.start()

def on_btnc_pressed(_):
  game.register_input_right()


# CORE

def setup():
  global game

  M5.begin()

  game = Game()

  ticker.init(mode=Timer.PERIODIC, period=200, callback=on_ticker_tick)
  BtnA.setCallback(type=BtnA.CB_TYPE.WAS_PRESSED, cb=on_btna_pressed)
  BtnB.setCallback(type=BtnB.CB_TYPE.WAS_PRESSED, cb=on_btnb_pressed)
  BtnC.setCallback(type=BtnC.CB_TYPE.WAS_PRESSED, cb=on_btnc_pressed)

def loop():
  M5.update()


# MAIN

if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")
