import unittest
from unittest.mock import Mock, patch
from datetime import datetime

class TournamentTest(unittest.TestCase):

    @patch('model_tournament.datetime')
    def test_start(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        system_mock = Mock()
        players_mock = Mock()
        start_time = datetime(2023, 1, 1, 12, 0)
        system_mock.calculate_places(system_mock.run_tournament(), players_mock)
        running_results_status = True

        self.assertEqual(start_time, datetime(2023, 1, 1, 12, 0, 0))
        system_mock.run_tournament.assert_called_once()
        system_mock.calculate_places.assert_called_once_with(
            system_mock.run_tournament.return_value, players_mock)
        self.assertTrue(running_results_status)

    @patch('model_tournament.datetime')
    def test_end(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 1, 1, 13, 0, 0)
        end_time = datetime(2023, 1, 1, 13, 0)
        running_results_status = False

        self.assertEqual(end_time, datetime(2023, 1, 1, 13, 0, 0))
        self.assertFalse(running_results_status)


if __name__ == '__main__':
    unittest.main()
