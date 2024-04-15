from unittest.mock import patch, Mock
import shutil
import unittest
import os
import subprocess

from django.test import TestCase

from invoker.invoker_multi_request import InvokerMultiRequest
from invoker.invoker_request import InvokerRequest
from invoker.invoker import NormalProcess
from app.classes.jury import Jury, GameState
from ..launcher import Launcher


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

    @patch("app.classes.jury.Jury.get_processes")
    def test_get_invoker_requests(self, mock_get_processes: Mock):
        play_invoker_request = InvokerRequest("command")
        play_invoker_request.label = "play"

        strategy_invoker_request1 = InvokerRequest("command1")
        strategy_invoker_request1.label = "player1"
        strategy_invoker_request2 = InvokerRequest("command2")
        strategy_invoker_request2.label = "player2"

        invoker_multi_request = InvokerMultiRequest(
            [play_invoker_request, strategy_invoker_request1, strategy_invoker_request2])

        jury = Jury(invoker_multi_request)

        self.assertEqual(jury.play_invoker_request, play_invoker_request)
        self.assertEqual(jury.strategies_invoker_requests, [strategy_invoker_request1, strategy_invoker_request2])

    def test_get_processes(self):
        play_mock_process = NormalProcess(Mock(), label="play")
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
        invoker_multi_request.subscribe(jury)

        class getNotify():
            def __init__(self, IMR, UC):
                self.IMR_test = IMR
                self.upper_class = UC
                ...

            def notify(self, process):
                self.IMR_test.send_process()
                self.upper_class.assertEqual(jury.play_process, play_process)
                self.upper_class.assertEqual(jury.strategies_process, strategy_processes)

        notify_return = getNotify(invoker_multi_request, self)

        invoker_multi_request.subscribe(jury)
        invoker_multi_request.subscribe(notify_return)
        invoker_multi_request.start()

    @patch('app.classes.jury.Jury.__init__')
    def test_perform_play_command(self, mock_init: Mock):
        class GetInvokerMultiRequestCallback:
            def __init__(self, jury: Jury, UC):
                self.jury = jury
                self.upper_class = UC

            def notify(self, reports):
                pass

            def notify_processes(self, processes):
                jury = self.jury
                jury.perform_play_command()
                print(jury.game_state)
                print(jury.points)
                print(jury.story_of_game)

                self.upper_class.assertEqual(jury.jury_report.status, "OK")
                self.upper_class.assertEqual(jury.jury_report.story_of_game, "smth")
                #self.upper_class.assertEqual(jury.jury_report.points, points_dict)

        mock_init.return_value = None
        jury = Jury()
        jury.strategies_process = []
        jury.game_state = GameState.PLAY

        def play_process_callback(process):
            jury.play_process = process

        def strategy_process_callback(process):
            jury.strategies_process.append(process)

        play = os.path.abspath("app/classes/jury_test/play.epy")
        str1 = os.path.abspath("app/classes/jury_test/str1.epy")
        str2 = os.path.abspath("app/classes/jury_test/str2.epy")

        play_ir = Launcher(play, process_callback=play_process_callback)
        str1_ir = Launcher(str1, process_callback=strategy_process_callback)
        str2_ir = Launcher(str2, process_callback=strategy_process_callback)

        imr = InvokerMultiRequest([play_ir, str1_ir, str2_ir])
        get_imr_callback = GetInvokerMultiRequestCallback(jury, self)
        imr.subscribe(get_imr_callback)
        imr.start()

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
