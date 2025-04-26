import unittest
from pathlib import Path
import time
from mc_server_manager import JavaServerManager

class TestMinecraftServerControl(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Before starting the tests, we initialize the server manager.
        """
        server_working_directory = Path("./server")
        start_script_path = server_working_directory / "server.jar"

        cls.manager = JavaServerManager.from_server_properties(
            str(server_working_directory),
            str(start_script_path)
        )

    def test_get_processes(self):
        """
        Test to verify that the ServerManager correctly returns the server processes.
        """
        processes = self.manager.get_processes()

        # There should be at least one instance since the server is running.
        self.assertGreater(len(processes), 0)


    def test_get_status_online(self):
        """
        Test to verify that the ServerManager returns the status of the server while it is online.
        """
        # Make sure the server is online
        processes = self.manager.get_processes()
        if len(processes) == 0:
            self.manager.start()
            self.yield_until_server_online()

        status = self.manager.get_status()

        self.assertEqual(status, 'Online')

    def test_get_status_offline(self):
        """
        Test to verify that the ServerManager returns the status of the server while it is offline.
        """
        # Make sure the server is offline
        self.manager.stop(yield_until_closed=True)

        status = self.manager.get_status()

        self.assertEqual(status, 'Offline')

    def test_stop(self):
        """
        Test to verify that the ServerManager correctly shuts down the server.
        """
        self.manager.stop(yield_until_closed=True)

        processes = self.manager.get_processes()

        # There should be no process
        self.assertEqual(len(processes), 0)

    def yield_until_server_online(self, timeout=90):
        """
        Yield until the server is online.
        """
        expiration_time = time.time() + timeout
        status = None
        while expiration_time > time.time():
            if (status:= self.manager.get_status()) != 'Starting':
                break
            time.sleep(0.5)

        return status == 'Online'

    def test_start(self):
        """
        Test to verify that the ServerManager correctly starts the server.
        """
        self.manager.start()

        processes = self.manager.get_processes()

        self.assertGreater(len(processes), 0)

        status = self.manager.get_status()

        # Status should only be Starting, but Online was included just in case.
        self.assertIn(status, ['Starting', 'Online'])

        # Wait until the server has fully started.
        is_online = self.yield_until_server_online()

        self.assertTrue(is_online)

    def test_restart(self):
        """
        Test to verify that the ServerManager correctly restarts the server while it is online.
        """
        self.manager.restart()

        processes = self.manager.get_processes()

        self.assertGreater(len(processes), 0)

        status = self.manager.get_status()

        # Status should only be Starting, but Online was included just in case.
        self.assertIn(status, ['Starting', 'Online'])

        # Wait until the server has fully started.
        is_online = self.yield_until_server_online()
        
        self.assertTrue(is_online)

    def test_restart_online(self):
        """
        Base Test to verify that the ServerManager correctly restarts the server.
        """
        # Make sure the server is online
        processes = self.manager.get_processes()
        if len(processes) == 0:
            self.manager.start()
            self.yield_until_server_online()
        self.test_restart()

    def test_restart_offline(self):
        """
        Test to verify that the ServerManager correctly "restarts" the server while it is offline.
        """
        # Make sure the server is offline
        self.manager.stop(yield_until_closed=True)
        self.test_restart()

    def test_force_stop(self):
        """
        Test to verify that the ServerManager swiftly force stops server.
        """
        # Make sure the server is online
        processes = self.manager.get_processes()
        if len(processes) == 0:
            self.manager.start()
            self.yield_until_server_online()

        self.manager.force_stop()

        processes = self.manager.get_processes()

        self.assertEqual(len(processes), 0)

        status = self.manager.get_status()

        # Status should be Stopped
        self.assertEqual(status, 'Offline')