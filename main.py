import os
from pysys import *
"""Object definitons"""

command1 = Command("Command1")
command2 = Command("Command2")

subsystem = Subsystem("Subsystem", command2)

scheduler = Scheduler.get_instance()

system = System.get_instance()

"""Setup"""
scheduler.setup_scheduler({
    subsystem: (command1, command2)
})

system.setup_system(loop_period=1)
"""Loop"""

with open("log.txt", "w") as file:
    file.write("")

while system.is_active:
    os.system('cls' if os.name == 'nt' else 'clear')
    
    system.run_system()
    
    if system.tick_count == 2:
        scheduler.schedule_command(command1)
        
    if system.tick_count == 10:
        scheduler.interrupt_command(command1)
        
    if system.tick_count == 20:
        system.exit_system()