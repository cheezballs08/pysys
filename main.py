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
command1 = pysys.Command("Command 1")
command2 = pysys.Command("Command 2")
command3 = pysys.Command("Command 3")
command4 = pysys.Command("Command 4")

subsystem1 = pysys.Subsystem("Subsystem 1")
subsystem2 = pysys.Subsystem("Subsystem 2")
#User objects

#Setup
scheduler.setup_scheduler(
    subsystem_commands_dictionary=
    {
        subsystem1: (command1, command2),
        subsystem2: (command3, command4, command2)
    },
    subsystem_default_command_dicitionary=
    {
        subsystem1: command1,
        subsystem2: command3
    }
    )

system.setup_system(loop_period=0.02)
#Setup

#User setup

scheduler.schedule_command(command4)

#User setup

#Main Loop (Feel free to change this however you want.)
with open("log.txt", "w") as file:
    file.write("")
    
scheduler.remove_duplicate_items() #Just in case, I would advise you to keep this here.

while system.is_active:
    os.system('cls' if os.name == 'nt' else 'clear')
    
    if system.tick_count == 5:
        scheduler.schedule_command(command2)
        
    if system.tick_count == 8:
        scheduler.interrupt_command(command4)
        
    if system.tick_count == 12:
        scheduler.interrupt_command(command2)
    
    system.run_system()
    
    if system.tick_count == 17:
        system.exit_system()
#Main Loop