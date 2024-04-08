from unittest.mock import patch, Mock
import shutil
import unittest
import subprocess

from invoker.invoker_multi_request import InvokerMultiRequest
from invoker.invoker_request import InvokerRequest
from invoker.invoker import NormalProcess
from app.classes.jury import Jury


class TestJury(unittest.TestCase):
    shutil.copyfile("app/classes/jury_original_test_files/data_player_1.txt", "media/jury_test_files/data_player_1.txt")
    shutil.copyfile("app/classes/jury_original_test_files/data_player_2.txt", "media/jury_test_files/data_player_2.txt")
    shutil.copyfile("app/classes/jury_original_test_files/data_player_3.txt", "media/jury_test_files/data_player_3.txt")
    shutil.copyfile("app/classes/jury_original_test_files/data_player_4.txt", "media/jury_test_files/data_player_4.txt")
    shutil.copyfile("app/classes/jury_original_test_files/save_data.txt", "media/jury_test_files/save_data.txt")
    shutil.copyfile("app/classes/jury_original_test_files/save_data_1.txt", "media/jury_test_files/save_data_1.txt")
    shutil.copyfile("app/classes/jury_original_test_files/save_data_2.txt", "media/jury_test_files/save_data_2.txt")

    process = None

    def notify_processes(self, processes):
        self.process = processes

    def test_perform_play_command_ended(self):
        # play_command = "status: end points: player1: 5 player2: 4 story_of_game: smth"
        # play_command1 = bytes(play_command, 'utf-8')
        # play_command2 = play_command.encode('utf-8')

        play_file = open("media/jury_test_files/data_player_1.txt", 'r')
        play_mock_process = NormalProcess(Mock(), label="play")
        play_mock_process.stdout = play_file
        strategy_mock_process_1 = NormalProcess(Mock(), label="player1")
        strategy_mock_process_2 = NormalProcess(Mock(), label="player2")

        play_invoker_request = InvokerRequest("command", process_callback=play_mock_process)
        play_invoker_request.label = "play"
        play_process = play_invoker_request.process_callback

        strategy_invoker_request1 = InvokerRequest("command1", process_callback=strategy_mock_process_1)
        strategy_invoker_request1.label = "player1"
        strategy_invoker_request2 = InvokerRequest("command2", process_callback=strategy_mock_process_2)
        strategy_invoker_request2.label = "player2"
        strategy_processes = [strategy_invoker_request1.process_callback, strategy_invoker_request2.process_callback]

        invoker_multi_request = InvokerMultiRequest(
            [play_invoker_request, strategy_invoker_request2, strategy_invoker_request1])

        jury = Jury(invoker_multi_request)

        class getNotify():
            def __init__(self, IMR, UC, JR):
                self.IMR_test = IMR
                self.upper_class = UC
                self.jury = JR
                ...

            def notify(self, process):
                self.IMR_test.send_process()
                self.jury.perform_play_comand()

                points_dict = {"player1": 5, "player2": 4}

                self.upper_class.assertEqual(jury.jury_report.status, "OK")
                self.upper_class.assertEqual(jury.jury_report.story_of_game, "smth")
                self.upper_class.assertEqual(jury.jury_report.points, points_dict)

        notify_return = getNotify(invoker_multi_request, self, jury)

        invoker_multi_request.subscribe(jury)
        invoker_multi_request.subscribe(notify_return)
        invoker_multi_request.start()

    def test_perform_play_command_playing(self):
        # play_command = "status: play data: player1: None player2: 4"

        play_file = open("media/jury_test_files/data_player_2.txt", 'r')
        play_file_save = open("media/jury_test_files/save_data.txt", 'a+')
        strategy_file_1 = open("media/jury_test_files/data_player_3.txt", 'r')
        strategy_file_save_1 = open("media/jury_test_files/save_data_1.txt", 'a+')
        strategy_file_2 = open("media/jury_test_files/data_player_4.txt", 'r')
        strategy_file_save_2 = open("media/jury_test_files/save_data_2.txt", 'a+')

        play_mock_process = NormalProcess(Mock(), label="play")
        play_mock_process.stdout = play_file
        play_mock_process.stdin = play_file_save
        strategy_mock_process_1 = NormalProcess(Mock(), label="player1")
        strategy_mock_process_1.stdout = strategy_file_1
        strategy_mock_process_1.stdin = strategy_file_save_1
        strategy_mock_process_2 = NormalProcess(Mock(), label="player2")
        strategy_mock_process_2.stdout = strategy_file_2
        strategy_mock_process_2.stdin = strategy_file_save_2

        play_invoker_request = InvokerRequest("command", process_callback=play_mock_process)
        play_invoker_request.label = "play"

        strategy_invoker_request1 = InvokerRequest("command1", process_callback=strategy_mock_process_1)
        strategy_invoker_request1.label = "player1"
        strategy_invoker_request2 = InvokerRequest("command2", process_callback=strategy_mock_process_2)
        strategy_invoker_request2.label = "player2"

        invoker_multi_request = InvokerMultiRequest(
            [play_invoker_request, strategy_invoker_request2, strategy_invoker_request1])

        jury = Jury(invoker_multi_request)

        invoker_multi_request.subscribe(jury)
        invoker_multi_request.send_process()

        jury.perform_play_command()

        # play_file_check = open("media/jury_test_files/save_data.txt", 'r')
        # strategy_file_check_1 = open("media/jury_test_files/save_data_1.txt", 'r')
        # strategy_file_check_2 = open("media/jury_test_files/save_data_2.txt", 'r')

        self.assertEqual(jury.jury_report.status, "")
        self.assertEqual(play_mock_process.stdin.read(), "")
        self.assertEqual(strategy_file_save_1.read(), "")
        self.assertEqual(strategy_file_save_2.read(), "")

        play_file_check = open("media/jury_test_files/save_data.txt", 'r+')
        strategy_file_check_1 = open("media/jury_test_files/save_data_1.txt", 'r+')
        strategy_file_check_2 = open("media/jury_test_files/save_data_2.txt", 'r+')

        self.assertEqual(play_file_check.read(), "\n377\n")
        self.assertEqual(strategy_file_check_1.read(), "")
        self.assertEqual(strategy_file_check_2.read(), "4\n")

        play_file_check.truncate(0)
        strategy_file_check_1.truncate(0)
        strategy_file_check_2.truncate(0)
