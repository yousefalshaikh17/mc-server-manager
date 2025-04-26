import unittest
from pathlib import Path
from mc_server_manager import JavaServerManager
        

class TestMinecraftServerRCON(unittest.TestCase):

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

    def test_run_commands(self):
        """
        Test to verify that the ServerManager correctly runs a command on the server through RCON.
        """
        # We attempt to set dificulty to hard.
        success, response = self.manager.run_command('difficulty hard')
        
        # Check if the request was successful
        self.assertTrue(success)
        
        # Check if the output is as expected.
        self.assertEqual(response, "The difficulty has been set to Hard")

    def test_save_world(self):
        """
        Test to verify that the ServerManager properly saves the world through RCON.
        """
        # We attempt to save the world. (Internally this does /save-all)
        success = self.manager.save_world()
        
        # Check if the save was successful
        self.assertTrue(success)

    def test_say(self):
        """
        Test to verify that the ServerManager properly says a message through RCON.
        """
        # We attempt to save the world. (Internally this does /say)
        # /say does not return anything, so there is no text output to check.
        success = self.manager.say("Test")
        
        # Check if the save was successful
        self.assertTrue(success)