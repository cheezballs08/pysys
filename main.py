#Imports
import os
import pysys
#Imports

#Object definitions
scheduler = pysys.Scheduler.get_instance()

system = pysys.System.get_instance()

logger = pysys.Logger.get_instance()
#Object definitions

#User objects

#Put your objects here

#User objects

#Setup
scheduler.setup_scheduler({}, {})

system.setup_system(loop_period=0.5)
#Setup

#User setup

#Set up anything you want here

#User setup

#Main Loop (Feel free to change this however you want.)
with open("log.txt", "w") as file:
    file.write("")
    
while system.is_active:
    os.system('cls' if os.name == 'nt' else 'clear')
    
    system.run_system()
    
    if system.tick_count == 100:
        system.exit_system()
#Main Loop