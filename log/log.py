from datetime import datetime 

def write_logs( message: str = ""):
    with open("log\log.txt", mode="a") as log_file:
        content = f" {datetime.now()} - {message} \n"
        log_file.write(content)