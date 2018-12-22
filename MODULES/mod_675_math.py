################################################################################
# Module: mod_.py
#
# Example Query:
#   ""
################################################################################
from functools import reduce
import operator
import re

EXCLUSIVE = False

################################################################################
# score() - attempts to determine if this module is appropriate to our inputs
################################################################################
def score(category="NONE", query="", q_words=[]):
   myscore = 0
   if re.search("factor", query):
      return True
   if re.search(" (prime|composite|perfect) number ", query):
      return True
   return False

################################################################################
# run() - if this module is applicable, this will run our code
################################################################################
def run(category="NONE", query="", q_words=[]):
   OUTSTRING = ""
   for x in query.split():
      if x.isdigit():
         n = int(x)
         factors = sorted(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

         if len(factors) == 2:
            OUTSTRING += "The factors of " + str(n) + " are: 1, and " + str(n) + ".  It is a prime number.\n"
         elif (sum(factors[:-1])) == n:
            OUTSTRING += "The factors of " + str(n) + " are: " + ", ".join(str(x) for x in factors[:-1]) + ", and " + str(n) + ".  It is a perfect number.\n"
         else:
            OUTSTRING += "The factors of " + str(n) + " are: " + ", ".join(str(x) for x in factors[:-1]) + ", and " + str(n) + ".  It is a composite number.\n"

   if len(OUTSTRING) == 0:
      return "I can only determine the factors of integers."

   return OUTSTRING