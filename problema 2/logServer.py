import Pyro4
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv(".envLogs")

@Pyro4.expose
class LogServer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.logs = []

    def add_log(self, log_entry):
        self.logs.append(log_entry)
        print(f"Log received: {log_entry}")
        with open(self.log_file, 'a') as file:
            file.write(log_entry + '\n')
        return "Log added successfully"

    def get_logs(self):
        return self.logs

def main():
    logName = os.getenv("LOGNAME")
    serverName = str(os.getenv("LOG_SERVER"))
    log_server = LogServer(logName)
    daemon = Pyro4.Daemon(host=os.getenv("LOG_SERVER_IP"))  # Pyro daemon
    ns = Pyro4.locateNS(host=os.getenv("LOG_SERVER_IP"))  # Locate the name server
    uri = daemon.register(log_server)  # Register the log server object
    print(uri)
    ns.register(serverName, uri)  # Register the object with a name in the name server
    print("Log Server is running.")
    daemon.requestLoop()  # Start the event loop of the server to wait for calls

if __name__ == "__main__":
    main()
