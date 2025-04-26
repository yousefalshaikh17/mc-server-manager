import unittest
from pathlib import Path
from mc_server_manager import JavaServerManager
        

class TestMinecraftServerQuery(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Before starting the tests, we initialize the server manager.
        """
        server_working_directory = Path("./server")
        start_script_path = server_working_directory / "server.jar"


        cls.manager = JavaServerManager.from_server_properties(
            server_working_directory,
            start_script_path
        )     

    def test_ping(self):
        """
        Test to verify that the ServerManager correctly pings the server.
        """
        latency_ms = self.manager.ping()
        
        self.assertIsNotNone(latency_ms)
        self.assertIsInstance(latency_ms, float)
        self.assertGreaterEqual(latency_ms, 0)        

    def test_get_online_players(self):
        """
        Test to verify that the ServerManager correctly retrieves a list of players.
        """
        online_players = self.manager.get_online_players()
        
        self.assertIsNotNone(online_players)
        self.assertIsInstance(online_players, list)

        # It is assumed that the server will be empty, so therefore the list will be empty.
        # @TODO: If it is possible to simulate a player joining, do implement.
        self.assertListEqual(online_players, [])
