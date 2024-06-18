import Pyro4
from datetime import datetime

def generate_log_entry(action, inicio, fin, player, team):
    timestamp = datetime.now().isoformat()
    return f"{timestamp} | {action} | {inicio} | {fin} | {player} | {team}"

def main():
    # Connect to the name server
    ns = Pyro4.locateNS()
    uri = ns.lookup("example.logserver")
    log_server = Pyro4.Proxy(uri)  # Create a proxy for the log server object

    print("Connected to the Log Server.")
    while True:
        action = input("Enter the action: ")
        inicio = input("Enter the start time: ")
        fin = input("Enter the end time: ")
        player = input("Enter the player name: ")
        team = input("Enter the team name: ")
        log_entry = generate_log_entry(action, inicio, fin, player, team)
        response = log_server.add_log(log_entry)
        print(response)
        cont = input("Do you want to add another log? (yes/no): ")
        if cont.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
