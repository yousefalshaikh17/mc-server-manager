# **Minecraft Java Server Manager**

A Python tool to manage and interact with Minecraft Java Edition servers.

## **Overview**
The **Minecraft Java Server Manager** provides a simple and powerful way to control Minecraft servers programmatically. It allows you to:
- Start, stop, and restart servers
- Monitor server status (online, starting, anomaly, offline)
- Manage players and send broadcast messages
- Execute remote console (RCON) commands
- Save the world state and gracefully handle shutdowns

This tool uses the [`mcstatus`](https://github.com/py-mine/mcstatus) and [`mcrcon`](https://github.com/Uncaught-Exceptions/MCRcon) libraries to communicate with the server, along with [`system-process-controller`](https://github.com/yousefalshaikh17/system-process-controller), another library authored by me, to manage the server's underlying Java process.

## **Features**
- Start and stop Minecraft servers
- Restart servers if an anomaly is detected
- Ping and query server status and online players
- Execute RCON commands remotely, including built-in implementations like:
   - Save world state with `/save-all`
   - Broadcast server-wide messages with `/say`
- Monitor server health and status

## **Requirements**
- Python 3.10 or higher
- `mcstatus` library for server query and ping
- `mcrcon` library for RCON commands
- [`system-process-controller`](https://github.com/yousefalshaikh17/system-process-controller) library for controlling the server

## **Installation**

You can install the package with this command.

```bash
pip install git+https://github.com/yousefalshaikh17/mc-server-manager.git
```

### OR

Clone and install the package manually.

1. Clone the repository:
```bash
git clone https://github.com/yousefalshaikh17/mc-server-manager.git
cd mc-server-manager
```

2. Install the package using `pip`:
```bash
pip install .
```

## **Usage**

### **JavaServerManager  Class**

The `JavaServerManager` class allows you to easily control Minecraft server instances. You can start, stop, restart servers, and execute commands remotely.

### **Basic Example**

```python
from java_server_manager import JavaServerManager

server_manager = JavaServerManager(
    working_directory="path/to/server",
    start_script_path="path/to/start_script.sh",
    server_ip="127.0.0.1",
    server_port=25565,
    rcon_port=25575,
    rcon_password="your_rcon_password"
)

# Start the server
success, message = server_manager.start()
print(message)

# Check server status
print("Server Status:", server_manager.get_status())

# Send a broadcast message
server_manager.say("Server is now online!")

# Save the world
server_manager.save_world()

# Stop the server
server_manager.stop(yield_until_closed=True)

```

### **Create from server.properties**

You can also automatically load settings from `server.properties`:

```python
server_manager = JavaServerManager.from_server_properties(
    working_directory="path/to/server", # It will check for server.properties here
    start_script_path="path/to/start.sh",
    rcon_password="your_rcon_password"
)
```

### **Methods Available:**
- **`start(ignore_checks=False, force_restart=False)`**: Starts the server.
   - `ignore_checks`: If true, the manager will not check if the server is already online.
   - `force_restart`: Determines whether `force_close()` is called prior to starting.
- **`stop(yield_until_closed=False)`**: Gracefully stops the server via RCON.
   - `yield_until_closed`: Determines whether the server is terminated before starting. Only use this if you want to kill the server process.
- **`restart(force_close=False, save=False)`**: Restarts the server with optional save.
   - `force_close`: Determines whether the server is terminated before restarting. Only use this if you want to kill the server process.
   - `save`: Determines whether the server should attempt to save before restarting.
- **`ping()`**: Pings the server for latency.
- **`get_online_players()`**: Lists currently online players.
- **`run_command(command)`**: Executes a command via RCON.
   - `command`: The command to run on the Minecraft server.
- **`say(message)`**: Broadcasts a message to all players.
   - `message`: The message to say in the server.
- **`save_world()`**: Saves the world via RCON.
- **`force_stop()`**: Forcefully kills the server process if necessary.
- **`get_status()`**: Returns the current server status (Online, Starting, Anomaly, Offline).
- **`is_rcon_working()`**: Checks if RCON is responsive.

## **Testing**

The project includes unit tests to verify the functionality of the `JavaServerManager` class.

### **Running Tests**

1. Run the tests using `unittest`:

```bash
python -m unittest discover -s tests
```

### **Test Methods**

The tests cover the following methods.

#### RCON Functionality
- **`test_run_commands`**: Verifies sending multiple RCON commands to the server.
- **`test_save_world`**: Tests the server's ability to save the world via RCON.
- **`test_say`**: Tests sending a server-wide message using `/say`.

#### Query Functionality
- **`test_ping`**: Verifies the ability to ping the server and get latency.
- **`test_get_online_players`**: Tests retrieving the list of currently online players.

#### Control Functionality
- **`test_get_processes`**: Verifies that server-related processes are correctly identified.
- **`test_get_status_online`**: Tests detecting if the server is online.
- **`test_stop`**: Verifies stopping the server gracefully via RCON.
- **`test_get_status_offline`**: Tests detecting if the server is offline.
- **`test_start`**: Verifies starting the server process.
- **`test_restart_online`**: Tests restarting the server while it is online.
- **`test_force_stop`**: Verifies forcefully stopping the server process.
- **`test_restart_offline`**: Tests restarting the server when it is offline.

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
