import os
import pysys
"""Object definitons"""
scheduler = pysys.Scheduler.get_instance()

system = pysys.System.get_instance()

logger = pysys.Logger.get_instance()

"""Setup"""

scheduler.setup_scheduler({}, {})

system.setup_system(loop_period=0.5)
"""Loop"""

with open("log.txt", "w") as file:
    file.write("")
    
while system.is_active:
    os.system('cls' if os.name == 'nt' else 'clear')
    
    system.run_system()
    
    if system.tick_count == 100:
        system.exit_system()