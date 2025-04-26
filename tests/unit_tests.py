import unittest

from test_server_rcon import TestMinecraftServerRCON
from test_server_query import TestMinecraftServerQuery
from test_server_control import TestMinecraftServerControl

def make_suite():
    """
    make a unittest TestSuite object
        Returns
            (unittest.TestSuite)
    """
    suite = unittest.TestSuite()

    # First RCON is tested
    suite.addTest(TestMinecraftServerRCON('test_run_commands'))
    suite.addTest(TestMinecraftServerRCON('test_save_world'))
    suite.addTest(TestMinecraftServerRCON('test_say'))

    # Then query is tested
    suite.addTest(TestMinecraftServerQuery('test_ping'))
    suite.addTest(TestMinecraftServerQuery('test_get_online_players'))

    # Then process control methods are tested
    suite.addTest(TestMinecraftServerControl('test_get_processes'))
    suite.addTest(TestMinecraftServerControl('test_get_status_online'))
    suite.addTest(TestMinecraftServerControl('test_stop'))
    suite.addTest(TestMinecraftServerControl('test_get_status_offline'))
    suite.addTest(TestMinecraftServerControl('test_start'))
    suite.addTest(TestMinecraftServerControl('test_restart_online'))
    suite.addTest(TestMinecraftServerControl('test_force_stop'))
    suite.addTest(TestMinecraftServerControl('test_restart_offline'))

    return suite

def run_all_tests():
    """
    run all tests in the TestSuite
    """
    unittest.main(defaultTest='make_suite')

if __name__ == '__main__':
    run_all_tests()