import os
import pysys
"""Object definitons"""
scheduler = pysys.Scheduler.get_instance()

system = pysys.System.get_instance()

logger = pysys.Logger.get_instance()

subsystem1 = pysys.Subsystem("Subsystem 1", None)
subsystem2 = pysys.Subsystem("Subsystem 2", None)

command1 = pysys.Command("Command 1")
command2 = pysys.Command("Command 2")
command3 = pysys.Command("Command 3")


"""Setup"""

scheduler.setup_scheduler({
   subsystem1: (command1,),
    subsystem2: (command2,)
})

system.setup_system(loop_period=0.5)
"""Loop"""

with open("log.txt", "w") as file:
    file.write("")

    
while system.is_active:
    os.system('cls' if os.name == 'nt' else 'clear')
    
    system.run_system()
    
    if system.tick_count == 10:
        scheduler.schedule_command(command1)
        
    if system.tick_count == 15:
        scheduler.schedule_command(command2)
    
    if system.tick_count == 100:
        system.exit_system()