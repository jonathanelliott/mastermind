# No longer needed
#
# def use_mask(mask, ls):
#   """
#   Given a mask (a list of booleans of the same length as the given list), keep only those elements of the list where the corresponding element of the mask is True.
#   """
#   return [x for i, x in enumerate(ls) if mask[i]]

# def remove_blacks(self, guess, code):
#   mask = [guess[i] != code[i] for i in range(self.num_pegs)]
#   # only keep those elements of 'guess' and 'code' which do not give black pegs
#   return use_mask(mask, guess), use_mask(mask, code)