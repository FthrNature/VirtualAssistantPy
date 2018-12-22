################################################################################
# Module: mod_date_time.py
#
# Example Query:
#   "what is todays date?"
#   "what time is it?"
#   "what day is it?"
#   "what is today?"
################################################################################
from datetime import datetime
import re

EXCLUSIVE = True

################################################################################
# score() - attempts to determine if this module is appropriate to our inputs
################################################################################
def score(category="NONE", query="", q_words=[]):
   if re.search("(what|tell me) .*(date|time|day) ", query):
      return True
   if re.search(" is today ", query):
      return True
   return False

################################################################################
# run() - if this module is applicable, this will run our code
################################################################################
def run(category="NONE", query="", q_words=[]):
   if re.search(" in ", query):
      print("need to parse this location...")
   if re.search("(date|day)", query):
      return datetime.now().strftime("Today is %A, %B %d %Y")
   return datetime.now().strftime("It is %H:%M:%S")
