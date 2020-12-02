import random
from jonathan import *

colours = ["R","Y","B","G","W","K"]
num_pegs = 4

def valid_guess(guess, valid_length=4):
  return len(guess) == valid_length and all(x in colours for x in guess)

def clue2(guess,code): #luke's way of assigning score pegs
  guess_copy = [ g for g in guess ]
  code_copy = [ c for c in code ]
  score =[0,0] # blacks, whites

  for i, peg in enumerate(guess_copy): #black pegs
    if peg==code_copy[i] or code_copy[i] == "z": # z denotes it could be anything
      code_copy[i] = "x"
      guess_copy[i]= "x"
      score[0]+=1

  for i, peg in enumerate(guess_copy): # white pegs
    if (peg in code_copy and not peg == "x") or ("z" in code_copy and not peg == "x"):
      code_copy[code_copy.index(peg)]="x"
      peg = "x"
      score[1]+=1

  #print(f"BLACKS: {score[0]}")
  #print(f"WHITES: {score[1]}")
  return score
      
def play(max_guesses=10, show_code=True):
  print("(Using Luke's way of assigning score pegs)")
  code_pegs = "".join(random.choices(colours, k=num_pegs))
  
  if show_code:
    print("Easy Mode")
    print(code_pegs)
  if max_guesses < 3:
    print("Super Hard Mode")

  num_guesses = 0
  guess = None

  while num_guesses < max_guesses:
    guess = input("Please guess a code: ").upper()
    if guess == "Q":
      return "You quit"
    if not valid_guess(guess):
      print("Please enter a valid guess")
      continue
    num_guesses += 1
    print(clue2(guess,code_pegs))
    if guess == code_pegs:
      return "Well done: you win!"
  return "Too many guesses: you lose"

def player():
    possible_code = [["r","g","b","y","o"],["r","g","b","y","o"],["r","g","b","y","o"],["r","g","b","y","o"]]

    code = "wybr"
    guesses =["gyrr","ybby","byrr"]
    scores = [[1,1],[1,0],[0,1]]

    for n, current_guess in enumerate(guesses):#n is the row we are about to pin pegs down on
      if scores[n][0] == 0:#no black pegs
        for i, peg in enumerate(current_guess):#i is the peg in that row
          possible_code[i].remove(peg)
          
      
      if scores[n][0] == 1:
        contradictions=[0,0,0,0]
        for i, peg in enumerate(current_guess):#i is the peg in that row
          assumed_code=["z","z","z","z"]
          assumed_code[i] = peg

          for j, current_guess in enumerate(guesses):# j is then row we are checking for contradictions
            if clue2(current_guess,assumed_code)[0] > scores[j][0] or clue2(current_guess,assumed_code)[1] > scores[j][1]:
              if not peg == "x":
                print(i,peg)
                possible_code[i].remove(peg)
                contradictions[i] = 1

      if sum(contradictions + scores[n][0])==4:
        #pin blakc pegs where contracitions == 0
        print("contradictions found")
        print(contradictions)#this test should reslut in [0,1,1,1]
        pass

def test(cases=10000):
  # test the methods of assigning score pegs against each other
  assert num_pegs == 4
  game = Game()

  def _run_tests(cases):
    for i in range(cases):
      g = "".join(random.choices(colours, k=num_pegs))
      c = "".join(random.choices(colours, k=num_pegs))
      if clue2(g,c) != list(game.clue(g,c)):
        print(g,c,"Failed")
        return False
    return True
  
  if _run_tests(cases):
    print(f"{cases} tests passed.")