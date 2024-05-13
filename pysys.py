from util import Singleton

class Logger(Singleton):
    
    name: str = "Logger"
    
    def log_to_terminal(self, message: str):
        print(message)
        
    def log_to_file(self, message: str, file_name: str):
        with open(file_name, "a") as file:
            file.write(message)