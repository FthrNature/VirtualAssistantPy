# VirtualAssistantPy
A virtual assistant in Python, includes Lists, Timers, and external modules.

This is my first attempt to create a Virtual Assistant in Python.

At the moment it responds to text input, I've experimented with Speech, but it still needs more work.

Input options - currently we support only Text inputs.  
I would like to include other options including Speech and automated tasking.

Desired Functionality
<p>      ### SYSTEM COMMANDS ######################################################
      # [exit | [turn| power] off | restart | reload]
      # [sleep | stop | [mute | quiet | shut up] | unmute] [for x minutes]
      # [help | what can you do? | what can you show me?]
      # [debug | nodebug]
      ##########################################################################

      ### LISTS ################################################################
      # make a list [named | called] <listname>
      # [delete | clear] [my] <listname> list
      # [read | show me] [what's on] [my] <listname>
      # add <item> to [my] <listname>
      # [remove | check off] <item> from [my] <listname>
      # [I need | remind me] to <task>
      # I need to buy <item>
      ##########################################################################

      ### TIMERS and ALARMS ####################################################
      # timers are short period events scheduled to expire within this session
      # set [a | an] [alarm | timer] for <time>
      # --- sleep [for <time>]
      # --- [cancel | acknowledge]
      # remind me to <description> [in <time> | when I get to <place>]
      ##########################################################################

      ### CALENDAR TASKS #######################################################
      # set [up] [a | an] [meeting | appointment | reminder] for <date/time>
      # what is [going on | on my calendar] [today | tomorrow | <day> | <date>]
      # when is my next meeting?
      # [when is | what day] is [<date> | <event> | <holiday> | <contacts birthday/anniversary>]      
      ##########################################################################

Output options<p>
Currently we support Text output.
Speech output has been experimented with, but I'm not happy with the overhead at the moment. 
I would also like to include report options including gisting and webscraping.     
