from django.test import TestCase


class IntegrationTest(TestCase):
    def test_upload(self, file):
        report = FileLoader(file)
        TestCase.assertEqual(report.compiler_report.status, "OK", "Failed")

    def test_creating_battle(self, game, players, creator):
        battle = Battle(game, players, creator)

    def test_run(self, game, players, creator):
        battle = Battle(game, players, creator)
        battle.run()
        TestCase.assertEqual(battle.report, "OK", "Failed")
    def test_create_response(self):
        pass

    def test_response_in_views(self):
        pass
