import Pyro4
from datetime import datetime

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
    log_server = LogServer("logs.txt")
    daemon = Pyro4.Daemon()  # Pyro daemon
    ns = Pyro4.locateNS()  # Locate the name server
    uri = daemon.register(log_server)  # Register the log server object
    ns.register("example.logserver", uri)  # Register the object with a name in the name server
    print("Log Server is running.")
    daemon.requestLoop()  # Start the event loop of the server to wait for calls

if __name__ == "__main__":
    main()
