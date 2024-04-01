import sys

from django.test import TestCase

from app.launcher import Launcher, NotSupportedExtension


class TestLauncher(TestCase):
    class LaunchTest(Launcher):
        pass

    def test_not_supported_launch(self):
        self.assertRaises(NotSupportedExtension, self.LaunchTest, "compiled.fuck")

    def test_CPP_launch(self):
        launcher = self.LaunchTest("compiled.ecpp")
        if sys.platform == "linux":
            self.assertEquals(launcher.command, "chmod +x compiled.ecpp ; compiled.ecpp")
        else:
            self.assertEqual(launcher.command, "compiled.ecpp")

    def test_PYTHON_launch(self):
        launcher = self.LaunchTest("compiled.epy")
        if sys.platform == "linux":
            self.assertEquals(launcher.command, "python3 compiled.epy")
        else:
            self.assertEqual(launcher.command, "python compiled.epy")
