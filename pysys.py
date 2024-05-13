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
    
    def __init__(self, name: str):
        self.name = name
        
    def periodic(self):
        self.logger.log_to_terminal(f"{self.name} has executed its periodic function.")
        self.logger.log_to_file(f"{self.name} has executed its periodic function.", "log.txt")