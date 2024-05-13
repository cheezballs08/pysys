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
            
    def finalize_commands(self):
        for command in self.finalizing_commands:
            command.finalize()
            command.is_executing = False
            self.finalizing_commands.remove(command)
            self.idle_commands.append(command)