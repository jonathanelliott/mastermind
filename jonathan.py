import random
import string
from collections import Counter, defaultdict
from itertools import product
from anytree import Node, RenderTree

def test_player(cases=10, num_pegs=4, colours="RYBGWK", show_working=False):
  for _ in range(cases):
    g = Game(num_pegs, colours)
    c = Player(g)
    c.run(show_working)
    print()

class Game:
  def __init__(self, num_pegs=4, colours="RYBGWK"):
    self.colours = colours
    self.num_pegs = num_pegs
    self.code = ''.join(random.choices(self.colours, k=self.num_pegs))
    # print(f"Game with {num_pegs} pegs and {len(colours)} colours ({','.join(colours)}) created.")

  def set_code(self, code=None):
    if code:
      self.code = code
    else:
      # regenerate random code
      self.code = ''.join(random.choices(self.colours, k=self.num_pegs))
  
  def valid_guess(self, guess):
    return len(guess) == self.num_pegs and all(x in self.colours for x in guess)

  def blacks(self, guess, code):
    # number of black pegs is the number of indices where the guess and the code agree
    # sum of a list of booleans is the number of times True appears
    return sum([guess[i] == code[i] for i in range(self.num_pegs)])

  def whites(self, guess, code):
    # number of white pegs is intersection of multisets (Counters) representing guess and code, minus the number of black pegs (since black pegs are essentially a special sort of white peg)
    return len(list((Counter(guess) & Counter(code)).elements())) - self.blacks(guess,code)

  def clue(self, guess, code=None):
    if not code:
      code = self.code
    if type(guess) == str:
      guess = guess.upper()
    return self.blacks(guess, code), self.whites(guess, code)
    # f"BLACKS: {self.blacks(guess, code)}\nWHITES: {self.whites(guess, code)}"

  def play(self, max_guesses=10, show_code=False):
    # print("(Using Jonathan's way of assigning score pegs)")
    print(f"{self.num_pegs} pegs, {len(self.colours)} colours ({','.join(self.colours)})")
    self.set_code()

    if show_code:
      print("Easy Mode")
      print(self.code)
    if max_guesses < 3:
      print("Hard Mode")

    num_guesses = 0
    guess = None

    while num_guesses < max_guesses:
      guess = input("Please guess a code: ").upper()
      if guess == "Q":
        return "You quit"
      if not self.valid_guess(guess):
        print("Please enter a valid guess")
        continue
      num_guesses += 1
      b, w = self.clue(guess)
      # print(f"BLACKS: {b}, WHITES: {w}")
      # print(f"●: {b}, ○: {w}")
      print('●' * b + '○' * w)
      if b == self.num_pegs:
        print("Code was:", self.code)
        return "Well done: you win!"
    print("Code was:", self.code)
    return "Too many guesses: you lose"

class Player:
  def __init__(self, game, strategy=0):
    self.game = game
    self.strategy = strategy

  def refresh(self):
    self.game.set_code()

  def run(self, show_working=True):
    if self.strategy == 0:
      log = list(zip(*self.naive()))
      print("Naive strategy")
    elif self.strategy == 1:
      print("Knuth algorithm (guaranteed at most 5 guesses)")
      log = list(zip(*self.knuth()))
    if show_working:
      for guess, (b,w), n in log:
        print(f"{n} possible code(s) remaining")
        print(f"Guessing {guess}...")
        print('●' * b + '○' * w)
    print(f"Solution found in {len(log)} guesses: {log[-1][0]}")

  def naive(self):
    g = self.game
    S = list(product(g.colours, repeat=g.num_pegs))
    # need list here because random.choice needs to know len
    guess = random.choice(S)
    guesses, clues, possible = [], [], []
    # possible is the number of possible solutions remaining
    while g.blacks(guess, g.code) < g.num_pegs:
      guess = ''.join(random.choice(S))
      b, w = g.clue(guess)
      guesses.append(guess)
      clues.append((b,w))
      possible.append(len(S))
      S = [ s for s in S if g.clue(guess, s) == (b,w) ]
    return guesses, clues, possible
  
  def knuth(self, randomise=True):
    # Based on the description of Knuth's minimax algorithm on Wikipedia
    g = self.game
    # assert g.num_pegs == 4
    c1, c2 = g.colours[:2]
    guess = c1 * 2 + c2 * 2
    b, w = g.clue(guess)
    all_codes = list(product(g.colours, repeat=g.num_pegs))
    # possible_scores = product(range(g.num_pegs + 1), repeat=2)
    S = all_codes.copy()
    guesses, clues, possible = [''.join(guess)], [(b,w)], [len(S)]
    while g.blacks(guess, g.code) < g.num_pegs:
      S = { s for s in S if g.clue(guess, s) == (b,w) }
      scores = {}
      for c in all_codes:
        # hits = { bw: 0 for bw in possible_scores if sum(bw) <= g.num_pegs }
        hits = defaultdict(int)
        for s in S:
          b, w = g.clue(c, s)
          hits[(b,w)] += 1
        scores[c] = len(S) - max(hits.values())
      max_scores = { c for c in scores if scores[c] == max(scores.values()) }
      if S & max_scores:
        # try to pick from S if possible
        if randomise:
          guess = random.choice(list(S & max_scores))
        else:
          guess = list(S & max_scores)[0]
      else:
        if randomise:
          guess = random.choice(list(max_scores))
        else:
          guess = list(max_scores)[0]
      guess = ''.join(guess)
      b, w = g.clue(guess)
      guesses.append(guess)
      clues.append((b,w))
      possible.append(len(S))
    return guesses, clues, possible

  # Consider hard-coding Figure 1 from Knuth paper for speed