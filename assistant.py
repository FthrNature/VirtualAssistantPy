import sys
import os
import re
import operator                    # for sorting our modules
import glob                        # for loading our modules
from threading import Thread       # for checking periodic tasks
import time                        # for checking periodic tasks
from datetime import datetime, timedelta

################################################################################
# Our Assistant Class
################################################################################
class Assistant:
   #############################################################################
   # __init__() - initialization routines, things that only need to be done once
   #  'module_path' - defaults to a subdirectory named ".../MODULES" in the
   #      current directory.  You could override this (eg. for testing purposes)
   #############################################################################
   def __init__(self, module_path=''):
      self.DEBUG_LEVEL = 0
      self.RUN_LEVEL = 1
      self.dir_name = os.path.dirname(os.path.realpath(__file__))
      self.modules_dir = self.dir_name + "\\MODULES\\"
      self.lists_dir = self.dir_name + "\\LISTS\\"
      self.modules_dict = {}
      self.import_modules()
      self.my_lists = []
      self.import_lists()
      self.my_timers = []

      t = Thread(target=self.timed_events)
      t.start()

      self.output("How can I help you today?")

   #############################################################################
   # import_modules() - finds and loads functionality modules, if called again
   #     it will force a reload of all modules (useful for testing purposes).
   #############################################################################
   def import_modules(self):
      sys.path.append(self.modules_dir)
      os.chdir(self.modules_dir)

      #for module in self.modules_dict:
      #   module_obj = self.modules_dict[module]
      #   reload(module_obj)

      for module in glob.glob("mod_*.py"):
         if module[:-3] in self.modules_dict:
            print("Reloading " + module)
            reload(self.modules_dict[module[:-3]])
         else:
            print("Importing new module:  " + module)
            self.modules_dict[module[:-3]] = (__import__(module[:-3]))

   #############################################################################
   # import_modules() - finds and loads functionality modules, if called again
   #     it will force a reload of all modules (useful for testing purposes).
   #############################################################################
   def import_lists(self):
      os.chdir(self.lists_dir)
      for mylist in glob.glob("list_*.txt"):
         print("Reading in your " + mylist[5:-4] + " list")
         with open(mylist, 'r') as f:
            lines = f.read().splitlines()
         self.my_lists.append(lines)
      print("Lists have been imported.")
            
   #############################################################################
   # timed_events() - periodic tasks done by our Assistant
   #  'sleep_seconds' - detrmines how long we will sleep between checks.  Our
   #      loop will run no more than once per minute, but this determines how
   #      frequently we check to see if our main thread is terminating.
   #      Valid values are between 2 and 60 seconds per iteration.
   #      This guarantees processing is only done between 60 and 118 seconds.
   #############################################################################
   def timed_events(self):
      MY_TICK = 0
      sleep_seconds = 3
      ITER_PER_MINUTE = int(60 / sleep_seconds)
      # check to see if we are quitting
      while self.RUN_LEVEL == 1:
         time.sleep(sleep_seconds) 
         current_time = datetime.now()
         
         MY_TICK = (MY_TICK + 1) % ITER_PER_MINUTE
         if MY_TICK == 0:
            # we should hit this block of code once per minute.
            # this is where we check our periodic tasks:
            #   calendar appointments
            #   hourly or periodic tasks
            #   reminders, etc...
            MY_TICK = 0
            
         # check to see if any timers have expired...
         if len(self.my_timers) > 0:
            index = 0
            for temp in self.my_timers:
               timer = temp[0]
               elapsed_time = timer - current_time
               if elapsed_time < timedelta(0):
                  print("!!!!! DING !!!!! " + temp[1])
                  del self.my_timers[index]
               index += 1

   #############################################################################
   # cleanup() - stop our background timer, and any other cleanup tasks
   #############################################################################
   def cleanup(self):
      os.chdir(self.lists_dir)
      for mylist in self.my_lists:
         print(mylist)
         with open("list_" + str(mylist[0]) + ".txt", 'w') as f:
            for item in mylist:
               f.write(str(item) + '\n')
   
      print("Please wait while we cleanup...")
      self.RUN_LEVEL = 0

   #############################################################################
   # execute() - Picks the best module to handle a User Request
   #  'query' - our user input, we will look for keywords in this query to try
   #      to determine which of our loaded modules will handle this request.
   #      Only the most applicable module will handle the request.
   #############################################################################
   def execute(self, query):
      # cleanup our inputs
      for punctuation in ['.', '?', '!', ',', ';', '\'', '\"']:
         query = query.replace(punctuation, " ")
      q_words = query.split(" ")

      ### SYSTEM COMMANDS ######################################################
      # [exit | [turn| power] off | restart | reload]
      # [sleep | stop | [mute | quiet | shut up] | unmute] [for x minutes]
      # [help | what can you do? | what can you show me?]
      # [debug | nodebug]
      ##########################################################################
      if len(q_words) == 1:
         if q_words[0] == "exit":
            self.RUN_LEVEL = 0
            return "Exiting."
         elif q_words[0] == "restart" or q_words[0] == "reload":
            self.import_modules()
            return "We have reloaded all modules."
         elif q_words[0] == "debug":
            return "Debug mode enabled."
            self.DEBUG_LEVEL = 1
         elif q_words[0] == "nodebug":
            return "Debug mode disabled."
            self.DEBUG_LEVEL = 0
      elif len(q_words) == 2:
         if (q_words[0] == "turn" or q_words[0] == "power") and q_words[1] == "off":
            self.RUN_LEVEL = 0
            return "Exiting."

      ### LISTS ################################################################
      # make a list [named | called] <listname>
      # [delete | clear] [my] <listname> list
      # [read | show me] [what's on] [my] <listname>
      # add <item> to [my] <listname>
      # [remove | check off] <item> from [my] <listname>
      # [I need | remind me] to <task>
      # I need to buy <item>
      ##########################################################################
      if re.search("^show .*lists", query):
         for mylist in self.my_lists:
            print(mylist)
         return
      elif re.search(" list", query):
         if re.search("^(make|create) a", query):
            temp = query.replace("make a ", "").replace("create a ", "").replace(" list", "")
            self.my_lists.append([temp])
            return("we are creating a list")
      
      temp = 0
      for mylist in self.my_lists:
         if re.search(str(mylist[0]), query) and re.search("list", query):
            if re.search("^delete ", query):                  
               del self.my_lists[temp]
               # we should always retain our "todo" and "shopping" lists, clear but don't delete these
               if str(mylist) == "todo" or str(mylist) == "shopping":
                  self.my_lists.append([str(mylist[0])])
               else:
                  if os.path.exists("list_" + mylist[0] + ".txt"):
                     os.chdir(self.lists_dir)
                     os.remove("list_" + mylist[0] + ".txt")
               return("Done")
            if re.search("^clear ", query):
               del self.my_lists[temp]
               self.my_lists.append([str(mylist[0])])
               return("Done")
            if re.search("^(show (me|my)|read|whats on) ", query):
               return("\n".join(mylist[1:]))
            if re.search("^add ", query):
               item = query.replace("add ", "").replace("to my ", "").replace(str(mylist[0]),"").replace(" list", "").strip()
               my_newlist = mylist
               my_newlist.append(item)
               del self.my_lists[temp]
               self.my_lists.append(my_newlist)
               return("I have added " + item + " to your " + str(mylist[0]) + " list.")
            if re.search("^(remove|delete) ", query):
               item = query.replace("remove ", "").replace("from my ", "").replace(str(mylist[0]),"").replace(" list", "").strip()
               my_newlist = mylist
               mylist.remove(item)
               del self.my_lists[temp]
               self.my_lists.append(my_newlist)
               return("I have removed " + item + " from your " + str(mylist[0]) + " list.")
         temp += 1
      
      ### TIMERS and ALARMS ####################################################
      # timers are short period events scheduled to expire within this session
      # set [a | an] [alarm | timer] for <time>
      # --- sleep [for <time>]
      # --- [cancel | acknowledge]
      # remind me to <description> [in <time> | when I get to <place>]
      ##########################################################################
      if re.search(" (timer|alarm)", query):
         if re.search("^set ", query):
            my_newtime = datetime.now()
            temp = 60
            description = ""
            counter = 0
            for word in q_words:
               counter += 1
               if word.isdigit():
                  temp = int(word)
               elif word == "s" or word == "sec" or word == "seconds":
                  my_newtime += timedelta(seconds=temp)
                  temp = 0
               elif word == "m" or word == "min" or word == "minutes":
                  my_newtime += timedelta(minutes=temp)
                  temp = 0
               elif word == "h" or word == "hr" or word == "hours":
                  my_newtime += timedelta(hours=temp)
                  temp = 0
               elif re.search(":", word):
                  temp2 = word.split(":")
                  if len(temp2) == 3:
                     if re.search(" alarm ", query):
                        my_newtime = datetime.now().replace(hour=int(temp2[0]), minute=int(temp2[1]), second=int(temp2[2]))
                     else:
                        my_newtime += timedelta(hours=int(temp2[0]), minutes=int(temp2[1]), seconds=int(temp2[2]))
                  else:
                     if re.search(" alarm ", query):
                        my_newtime = datetime.now().replace(hour=int(temp2[0]), minute=int(temp2[1]), second=0)
                     else:
                        my_newtime += timedelta(minutes=int(temp2[0]), seconds=int(temp2[1]))
               elif word == "named" or word == "called" or word == "to":
                  description = " ".join(q_words[counter:])
                  
            my_newtimer = [my_newtime, description]
            self.my_timers.append(my_newtimer)
            return "A timer has been added for " + str(my_newtime)[11:19]
         if re.search("^show ", query):
            if len(self.my_timers) == 0:
               return "You don't have any timers currently set."
            temp_output = ""
            for temp in self.my_timers:
               timer = temp[0]
               description = temp[1]
               if len(description) > 0:
                  temp_output += "You have a timer set for " + str(timer)[12:19] + " to " + description + "\n"
            return temp_output
               
      ### CALENDAR TASKS #######################################################
      # set [up] [a | an] [meeting | appointment | reminder] for <date/time>
      # what is [going on | on my calendar] [today | tomorrow | <day> | <date>]
      # when is my next meeting?
      # [when is | what day] is [<date> | <event> | <holiday> | <contacts birthday/anniversary>]      
      ##########################################################################

      ### LOADED MODULES #######################################################
      for module in self.modules_dict:
         module_obj = self.modules_dict[module]
         if module_obj.score("NONE", query, q_words) == True:
            if self.DEBUG_LEVEL > 0:
               print("   --> executing " + module + ".run(" + query + ")")
            return module_obj.run("NONE", query, q_words)
         
      return "I'm sorry, I don't know what to do with that request: " + query

   #############################################################################
   # output() - communicates results to the user in some way...
   #############################################################################
   def output(self, output_str):
      # speak, output to screen and/or logging

      ##### normal text output (to the screen)
      print(output_str)
      print("")

   #############################################################################
   # main_loop() - the main program loop
   #############################################################################
   def main_loop(self):
      self.output("Hi there, how can I help you?")
      while self.RUN_LEVEL != 0:
         input_string = input(">>> ").lower().strip()  # was raw_input() in previous python version
         self.output(self.execute(input_string))
      self.cleanup()

################################################################################
# The main loop
################################################################################
if __name__ == "__main__":
   CONTINUE = 1
   ai = Assistant()
   ai.main_loop()
