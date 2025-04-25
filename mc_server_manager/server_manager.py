import subprocess
from process_controller import ProcessController
from mcstatus import JavaServer
import math
import time
import threading
from mcrcon import MCRcon

class JavaServerManager:
    def __init__(self, working_directory, start_script_path, server_ip="127.0.0.1", server_port=25565, max_start_time=180, name="Java Server", connection_timeout=5, rcon_port=25575, rcon_password=""):
        """
        Initializes the JavaServerManager instance.

        Parameters:
        - working_directory (str): Path to the server directory.
        - start_script_path (str): Path to the server start script (run.bat).
        - server_ip (str): IP address of the Minecraft server.
        - server_password (str or None): RCON password for remote command execution.
        - max_start_time (int): Maximum wait time for server startup.
        - name (str): Name of the server instance.
        - connection_timeout (int): Timeout in seconds for server status checks.
        - server_port (int): The main Minecraft server port (default: 25565).
        - rcon_port (int or None): The RCON port for remote commands (default: 25575).
        """
        # JavaServer does some address checks internally to verify validity, so it is run first.
        self.server = JavaServer(server_ip, port=server_port, timeout=connection_timeout)
        self.name = name
        self.working_directory = working_directory
        self.start_script = start_script_path
        self.ip = server_ip
        self.server_port = server_port
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password
        self.max_start_time = max_start_time
    
    def get_online_players(self):
        """
        Retrieves a list of currently online players using the Query protocol.

        Returns:
        - list of str: Player names if server is available, otherwise None.
        """
        try:
            return self.server.query().players.names
        except:
            return None
        
    def ping(self):
        """
        Pings the Minecraft server using the Query protocol.

        Returns:
        - float: Server latency in milliseconds if server is available, otherwise None.
        """
        try:
            return self.server.ping()
        except:
            return None
        
    def get_processes(self):
        """
        Finds all active Minecraft server processes running in the specified working directory.

        Returns:
        - list of Process objects matching the Java process running in the server directory.
        """
        filter = {'name': 'java.exe', 'cwd': self.working_directory}
        return ProcessController.find_processes(filter)
    
    def force_stop(self):
        """
        Forcefully terminates the Minecraft server process.

        Returns:
        - bool: True if at least one process was successfully terminated, otherwise False.
        """
        processes = self.get_processes()
        success_flag = any(process.terminate() for process in processes)
        return success_flag
    
    def get_status(self):
        """
        Determines the current status of the server.

        Returns:
        - str: "Online", "Starting", "Anomaly", or "Offline".
        """
        processes = self.get_processes()
        for process in processes:
            if process.is_running():
                if self.ping() is None:
                    delta_time = math.floor(process.get_runtime())
                    return "Starting" if delta_time <= self.max_start_time else "Anomaly"
                return "Online"
        return "Offline"
        
    def start(self, ignore_checks=False, force_restart=False):
        """
        Starts the Minecraft server.

        Parameters:
        - ignore_checks (bool): If True, starts the server without verifying its current status.
        - force_restart (bool): If True, stops any running instance before starting a new one.

        Returns:
        - tuple (bool, str): Success flag and a status message.
        """
        if not ignore_checks:
            status = self.get_status()

            if status in ['Online', 'Starting']:
                return False, f"Server is already running or starting ({status})."

            if status == "Anomaly":
                self.restart(force_close=True, save=True)
                return True, "Server restarted after anomaly."

        if force_restart:
            self.force_stop()

        subprocess.Popen(["cmd", "/c", self.start_script], creationflags=subprocess.CREATE_NEW_CONSOLE)
        return True, "Server started."
    
    def restart(self, force_close=False, save=False):
        """
        Restarts the Minecraft server.

        Parameters:
        - force_close (bool): If True, forcefully terminates the server before restarting.
        - save (bool): If True, saves the world before restarting.

        Returns:
        - tuple (bool, str): Success flag and a status message.
        """
        if save:
            self.save_world()
        if force_close:
            self.force_stop()
        else:
            self.stop(yield_until_closed=True)
            time.sleep(1)
        return self.start()
    
    def run_command(self, command):
        """
        Sends an RCON command to the server.

        Parameters:
        - command (str): The command to execute via RCON.

        Returns:
        - tuple (bool, str): Success flag and the output from the command execution.
        """

        success = False
        try:
            # Uses with to safely disconnect socket
            with MCRcon(self.ip, self.rcon_password, self.rcon_port) as mcr:
                output = mcr.command(command)
                success = True
        except Exception as E:
            output = str(E)
        
        return success, output
    
    def is_rcon_working(self):
        """
        Checks if RCON is responsive by sending a command.

        Returns:
        - bool: True if RCON is working, otherwise False.
        """
        success, _ = self.run_command("list")
        return success  
    
    def save_world(self):
        """
        Saves the current world state via RCON. Equivalent to using /save-all.

        Returns:
        - bool: True if the save command was successful, otherwise False.
        """
        success, output = self.run_command("save-all")
        print(f"[Save Attempt] Success: {success}\n{output}")
        return success
    
    def say(self, message):
        """
        Broadcasts a message to all players on the server using RCON. Equivalent to using /say.

        Parameters:
        - message (str): The message to send.

        Returns:
        - bool: True if the message was sent successfully, otherwise False.
        """
        success, output = self.run_command(f"say {message}")
        print(f"[Say Attempt] Success: {success}\n{output}")
        return success
    
    def stop(self, yield_until_closed=False):
        """
        Gracefully stops the server using RCON. Equivalent to using /stop.

        Parameters:
        - yield_until_closed (bool): If True, waits until the server process is fully terminated.

        Returns:
        - bool: True if the stop command was successful, otherwise False.
        """
        if self.get_status() == "Offline":
            return False

        success, output = self.run_command("stop")
        print(f"[Stop Attempt] Success: {success}\n{output}")

        def force_close():
            timeout_time = time.time() + 10
            processes = self.get_processes()
            while processes:
                for process in processes:
                    if not process.is_running():
                        processes.remove(process)
                        continue
                    if time.time() > timeout_time:
                        process.terminate()
        
        if yield_until_closed:
            force_close()
        else:
            threading.Thread(target=force_close).start()

        return success