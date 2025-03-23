import time
import psutil
import threading

class ProcessController():
    """
    A class to manage and monitor system processes.
    """

    def __init__(self, process):
        """
        Initializes the ProcessController with a given psutil Process object.

        Parameters:
        - process (psutil.Process): The psutil Process object to manage.
        """
        if not isinstance(process, psutil.Process):
            raise TypeError("The process must be an instance of psutil.Process")
        
        # Only PID and create time are stored for memory-efficiency.
        self.pid = process.pid
        self.create_time = process.create_time()
        
    @staticmethod
    def find_processes(filters=None):
        """
        Finds and returns a list of ProcessController instances matching the provided filters.
        
        Parameters:
        - filters (dict?): A dictionary containing filter criteria as key-value pairs.
          The available filter keys are:
            - 'pid' (int): The process ID (PID) to filter by.
            - 'name' (str): The name of the executable for the process (e.g., 'python.exe').
            - 'cwd' (str): The current working directory of the process (e.g., 'D:/server').
            - 'username' (str): The username under which the process is running (e.g., 'admin').
            - 'create_time' (float): The creation time of the process (seconds since epoch).
            - 'cmdline' (list[str]): The list of command line arguments of the process.
        
        Returns:
        - List of Process objects matching the criteria.

        """
        if filters is not None and not isinstance(filters, dict):
            raise TypeError("The filters must be a dictionary")
        
        if filters is None:
            filters = {}

        processes = []
        # Iterate through all processes
        for process in psutil.process_iter(['pid', 'name', 'cwd', 'username', 'create_time', 'cmdline']):
            match = True
            # Check each key-value pair in the filters
            for key, value in filters.items():
                if key not in process.info or process.info[key] != value:
                    match = False
                    break

            if match:
                processes.append(ProcessController(process))
        
        return processes
    
    def get_runtime(self):
        """
        Returns the time (in seconds) since the process was created.
        """
        return time.time() - self.create_time
    
    def get_process(self):
        """
        Returns the psutil Process object or None if unavailable.
        """
        try:
            process = psutil.Process(self.pid)
            # Create time is used to verify that another process hasn't reused the PID
            if process.create_time() == self.create_time:
                return process
        except psutil.NoSuchProcess:
            pass
        except psutil.AccessDenied:
            print(f"Access denied to process with PID: {self.pid}")
        return None

    def is_running(self):
        """
        Returns whether the process is running.
        """
        process = self.get_process()
        return process is not None and process.is_running()
    
    def get_cpu_usage(self, interval=0.1):
        """
        Returns process CPU usage percentage (averaged over `interval`).
        """
        if not isinstance(interval, (float, int)):
            raise TypeError("The interval must be a number (float or int)")

        process = self.get_process()
        return process.cpu_percent(interval=interval) if process else None

    def get_memory_usage_mb(self):
        """
        Returns the process memory usage in MB.
        """
        process = self.get_process()
        return round(process.memory_info().rss / (1024 * 1024), 2) if process else None
    
    def close(self):
        """
        Attempts to terminate the process safely.
        """
        process = self.get_process()
        if process is not None:
            try:
               process.terminate()
               return True
            except psutil.NoSuchProcess:
                return True
            except (psutil.AccessDenied, psutil.TimeoutExpired, psutil.ZombieProcess, psutil.Error) as e:
                print(f"An error occurred: {e}")
        return False
    
    def terminate(self):
        """
        Wrapper method around close to terminate the process safely.
        """
        return self.close()
    
    def terminate_after(self, delay, daemon=False):
        """
        Schedules the process for termination after a specified delay.

        Parameters:
        - delay (float): The time (in seconds) to wait before terminating the process.
        - daemon (bool): Whether the termination should be executed in a separate thread (default: False).
        """
        if not isinstance(delay, (float, int)):
            raise TypeError("The delay must be a number (float or int)")
        
        if not isinstance(daemon, bool):
            raise TypeError("daemon value must be a boolean.")

        def delayed_termination():
            time.sleep(delay)
            self.terminate()
        
        thread = threading.Thread(target=delayed_termination, daemon=daemon)
        thread.start()

    def restart(self):
        """
        Restarts the process if it is running, terminating and then starting a new instance with the same command line and working directory.
        """
        process = self.get_process()
        if process:
            try:
                # Store cmdline before termination
                cmdline = process.cmdline()
                cwd = process.cwd()

                # If the process stopped before the restart, cancel restart attempt.
                if not process.is_running():
                    return False
                
                self.terminate()
                
                # Wait for thread to die
                while self.is_running():
                    time.sleep(0.1)

                # Start thread
                new_process = psutil.Popen(cmdline, cwd=cwd)
                self.pid = new_process.pid
                self.create_time = new_process.create_time
                return True
            except Exception as e:
                print(f"Error restarting process {self.pid}: {e}")
        return False
