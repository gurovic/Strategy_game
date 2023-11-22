from django.test import TestCase
from unittest.mock import patch, Mock

from invoker.filesystem import File, _get_path, write_file, delete_file, delete_directory

from pathlib import Path


class TestFunctions(TestCase):
    def test_str_get_path(self):
        path = __file__
        self.assertEquals(_get_path(path), Path(path))

    def test_path_get_path(self):
        path = Path(__file__)
        self.assertEquals(_get_path(path), path)

    @patch("pathlib.Path.write_bytes")
    def test_write_file(self, mock_write_bytes: Mock):
        write_file("test.txt", b"test")
        mock_write_bytes.assert_called_with(b"test")

    @patch("pathlib.Path.unlink")
    def test_delete_file(self, mock_unlink: Mock):
        delete_file("test.txt")
        mock_unlink.assert_called()

    @patch("shutil.rmtree")
    def test_delete_directory(self, mock_rmtree: Mock):
        delete_directory("test")
        mock_rmtree.assert_called_with(Path("test"), ignore_errors=True)


class TestFile(TestCase):
    def test_load(self):
        file = Path(__file__)

        self.assertEquals(File(file.name, file.read_bytes()), File.load(file))

    @patch("invoker.filesystem.write_file")
    def test_make(self, mock_write_file: Mock):
        file = File.load(__file__)
        file.make("test")

        mock_write_file.assert_called_once_with(Path("test") / file.name, file.source)

    @patch("pathlib.Path.exists")
    @patch("invoker.filesystem.write_file")
    @patch("invoker.filesystem.delete_file")
    def test_make_exists(self, mock_delete_file: Mock, mock_write_file: Mock, mock_exists: Mock):
        mock_exists.side_effect = [True, False]

        file = File.load(__file__)
        file.make("test")

        path = Path("test") / file.name
        mock_delete_file.assert_called_once_with(path)
        mock_write_file.assert_called_once_with(path, file.source)
