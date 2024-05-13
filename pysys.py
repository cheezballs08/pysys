import time
from util import Singleton

class Logger(Singleton):
    
    name: str = "Logger"
    
    def log_to_terminal(self, message: str):
        print(message)
        
    def log_to_file(self, message: str, file_name: str):
        with open(file_name, "a") as file:
            file.write(message)
            
class Subsystem:
    
    name: str = "Subsystem"
    
    logger: Logger = Logger.get_instance()
    
    current_command: "Command" = None
    
    default_command: "Command" = None
    
    def __init__(self, name: str, default_command: "Command"):
        self.name = name
        self.default_command = default_command
        
    def periodic(self):
        self.logger.log_to_terminal(f"{self.name} has executed its periodic function.")
        self.logger.log_to_file(f"{self.name} has executed its periodic function.", "log.txt")
        
class Command:
    
    name: str = "Command"
    
    logger: Logger = Logger.get_instance()
    
    subsystems: list[Subsystem] = []
    
    is_executing: bool = False
    
    def __init__(self, name: str):
        self.name = name
        
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
        pass
    
class Scheduler(Singleton):
    
    name: str = "Scheduler"
    
    logger: Logger = Logger.get_instance()
    
    subsystems: list[Subsystem] = []
    
    commands: list[Command] = []
    
    idle_commands: list[Command] = []
    scheduled_commands: list[Command] = []
    executing_commands: list[Command] = []
    finalizing_commands: list[Command] = []
    
    def setup_scheduler(self, subsystem_commands_dictionary: dict[Subsystem, tuple[Command]]):
        for subsystem, commands in subsystem_commands_dictionary.items():
            self.subsystems.append(subsystem)
            for command in commands:
                command.subsystems.append(subsystem)
                self.commands.append(command)
                self.idle_commands.append(command)
    
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
            if command in self.executing_commands:
                self.interrupt_command(command)
                
    def check_subsystem_default_commands(self):
        for subsystem in self.subsystems:
            if subsystem.default_command in self.idle_commands:
                self.schedule_command(subsystem.default_command)
    
    def schedule_command(self, command: Command):
        if command in self.idle_commands:
            for subsystem in command.subsystems:
                if subsystem.current_command is not command:
                    self.interrupt_command(subsystem.current_command)
                    subsystem.current_command = command
                    
    def schedule_commands(self, commands: list[Command]):
        for command in commands:
            self.schedule_command(command)
            
    def execute_commands(self):
        for command in self.executing_commands:
            command.execute()
            command.is_executing = True
            
    def finalize_commands(self):
        for command in self.finalizing_commands:
            command.finalize()
            command.is_executing = False
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
        self.logger.log_to_file(f"Loop Ended, Tick: {self.tick_count}, Current time: {self.time_elapsed}", "log.txt")
        
        if self.loop_period > self.time_since_last_loop:
            time.sleep(self.loop_period - self.time_since_last_loop)
        else:
            self.logger.log_to_terminal(f"Loop Period Exceeded, Current Tick: {self.tick_count}, Current Time: {self.time_elapsed}")
            self.logger.log_to_file(f"Loop Period Exceeded, Current Tick: {self.tick_count}, Current Time: {self.time_elapsed}", "log.txt")
            
        def exit_system(self):
            self.is_active = False
            self.logger.log_to_file(f"System has exited after {self.tick_count} ticks and {self.time_elapsed} seconds", "log.txt")
            self.logger.log_to_terminal(f"System has exited after {self.tick_count} ticks and {self.time_elapsed} seconds")