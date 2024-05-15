import time
from util import Singleton

class Logger(Singleton):
    
    name: str = "Logger"
    
    def log_to_terminal(self, message: str):
        print(message)
        
    def log_to_file(self, message: str, file_name: str):
        with open(file_name, "a") as file:
            file.write(message + "\n")
            
class Subsystem:
    
    name: str = "Subsystem"
    
    logger: Logger = Logger.get_instance()
    
    def __init__(self, name: str, default_command: "Command"):
        self.name = name
        self.default_command = default_command
        self.current_command: "Command" = None
        self.default_command: "Command" = default_command
        
    def periodic(self):
        self.logger.log_to_terminal(f"{self.name} has executed its periodic function.")
        self.logger.log_to_file(f"{self.name} has executed its periodic function.", "log.txt")
        
class Command:
    
    name: str = "Command"
    
    logger: Logger = Logger.get_instance()
    
    def __init__(self, name: str):
        self.name = name
        self.subsystems: list[Subsystem] = []
        self.is_executing: bool = False
        self.has_initialized: bool = False        
        
    def initialize(self):
        self.logger.log_to_terminal(f"{self.name} has initialized.")
        self.logger.log_to_file(f"{self.name} has initialized.", "log.txt")
        
    def execute(self):
        self.logger.log_to_terminal(f"{self.name} has executed.")
        self.logger.log_to_file(f"{self.name} has executed.", "log.txt")
        
    def finalize(self):
        self.logger.log_to_terminal(f"{self.name} has finalized.")
        self.logger.log_to_file(f"{self.name} has finalized.", "log.txt")
        
    def should_end(self) -> bool:
        False
    
class Scheduler(Singleton):
    
    name: str = "Scheduler"
    
    logger: Logger = Logger.get_instance()
    
    subsystems: list[Subsystem] = []
    
    commands: list[Command] = []
    
    idle_commands: list[Command] = []
    scheduled_commands: list[Command] = []
    executing_commands: list[Command] = []
    finalizing_commands: list[Command] = []
    
    def remove_duplicate_items(self):
        self.commands = list(set(self.commands))
        self.subsystems = list(set(self.subsystems))
        for command in self.commands:
            command.subsystems = list(set(command.subsystems))

    
    def setup_scheduler(self, subsystem_commands_dictionary: dict[Subsystem, tuple[Command]]):
        for subsystem, commands in subsystem_commands_dictionary.items():
            self.subsystems.append(subsystem)
            for command in commands:
                self.commands.append(command)
                self.idle_commands.append(command)
                command.subsystems.append(subsystem)
        self.remove_duplicate_items()
        
    
    def run_subsystem_periodics(self):
        for subsystem in self.subsystems:
            subsystem.periodic()
            
    def interrupt_command(self, command: Command):
        if command in self.executing_commands:
            self.executing_commands.remove(command)
            command.is_executing = False
            self.finalizing_commands.append(command)
    
    def interrupt_commands(self, commands: list[Command]):
        for command in commands:
            self.interrupt_command(command)

    def check_command_ends(self):
        for command in self.executing_commands:
            if command.should_end():
                self.interrupt_command(command)
                
    def check_subsystem_default_commands(self):
        for subsystem in self.subsystems:
            if subsystem.default_command in self.idle_commands and subsystem.current_command is None:
                self.schedule_command(subsystem.default_command)
    
    def schedule_command(self, command: Command):
        if command in self.idle_commands:
            for subsystem in command.subsystems:
                if subsystem.current_command is not command:
                    self.interrupt_command(subsystem.current_command)
                    subsystem.current_command = command
            self.scheduled_commands.append(command)
            self.idle_commands.remove(command)
                    
    def schedule_commands(self, commands: list[Command]):
        for command in commands:
            self.schedule_command(command)
            
    def execute_commands(self):
        for command in self.scheduled_commands:
            if command.has_initialized is False:
                command.initialize()
            self.executing_commands.append(command)
            self.scheduled_commands.remove(command)
            command.is_executing = True
            
        for command in self.executing_commands:
            command.execute()
            command.is_executing = True
            
    def finalize_commands(self):
        for command in self.finalizing_commands:
            command.finalize()
            command.is_executing = False
            for subsystem in command.subsystems:
                if subsystem.current_command is command:
                    subsystem.current_command = None
            self.finalizing_commands.remove(command)
            self.idle_commands.append(command)
            
class System(Singleton):
    
    name: str = "System"
    
    logger: Logger = Logger.get_instance()
    
    scheduler: Scheduler = Scheduler.get_instance()
    
    is_active: bool = False
    
    loop_period: float = 1.0
    
    tick_count: int = -1
    
    start_time: float = 0.0
    
    current_time: float = 0.0
    
    time_elapsed: float = 0.0
    
    loop_start_time: float = 0.0
    
    time_since_last_loop: float = 0.0
    
    def setup_system(self, loop_period: float):
        self.is_active = True
        self.loop_period = loop_period
        self.start_time = time.time()
        
    def update_time(self):
        self.current_time = time.time()
        self.time_since_last_loop = self.current_time - self.loop_start_time
        self.time_elapsed = self.current_time - self.start_time
        
    def run_system(self):
        self.tick_count += 1
        
        self.loop_start_time = time.time()
        self.update_time()
        
        self.logger.log_to_terminal(f"Loop Started, Tick: {self.tick_count}, Current time: {self.time_elapsed}")
        self.logger.log_to_file(f"Loop Started, Tick: {self.tick_count}, Current time: {self.time_elapsed}", "log.txt")
        
        self.scheduler.run_subsystem_periodics()
        self.scheduler.check_subsystem_default_commands()
        self.scheduler.check_command_ends()
        self.scheduler.finalize_commands()
        self.scheduler.execute_commands()
        
        self.update_time()
        
        self.logger.log_to_terminal(f"Loop Ended, Tick: {self.tick_count}, Current time: {self.time_elapsed}")
        self.logger.log_to_terminal("")
        self.logger.log_to_file(f"Loop Ended, Tick: {self.tick_count}, Current time: {self.time_elapsed} \n", "log.txt")
        
        if self.loop_period > self.time_since_last_loop:
            time.sleep(self.loop_period - self.time_since_last_loop)
        else:
            self.logger.log_to_terminal(f"Loop Period Exceeded, Current Tick: {self.tick_count}, Current Time: {self.time_elapsed}")
            self.logger.log_to_file(f"Loop Period Exceeded, Current Tick: {self.tick_count}, Current Time: {self.time_elapsed}", "log.txt")
            
    def exit_system(self):
        self.is_active = False
        self.logger.log_to_file(f"System has exited after {self.tick_count} ticks and {self.time_elapsed} seconds", "log.txt")
        self.logger.log_to_terminal(f"System has exited after {self.tick_count} ticks and {self.time_elapsed} seconds")