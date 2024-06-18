import Pyro4
from datetime import datetime

def generate_log_entry(action, details):
    timestamp = datetime.now().isoformat()
    return f"{timestamp} - {action} - {details}"

def main():
    # Connect to the name server
    ns = Pyro4.locateNS()
    uri = ns.lookup("example.logserver")
    log_server = Pyro4.Proxy(uri)  # Create a proxy for the log server object

    print("Connected to the Log Server.")
    while True:
        action = input("Enter the action: ")
        details = input("Enter the details: ")
        log_entry = generate_log_entry(action, details)
        response = log_server.add_log(log_entry)
        print(response)
        cont = input("Do you want to add another log? (yes/no): ")
        if cont.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
