from django.test import TestCase

from app.models.jury_report import JuryReport


class JuryReportTestCase(TestCase):
    def test(self):
        story_of_game = "lol"
        points = {1: 1, 2: 1}
        status = 1
        jury_report = JuryReport.objects.create(story_of_game=story_of_game, points=points, status=status)

        self.assertEquals(story_of_game, str(jury_report.story_of_game))
        self.assertEquals(str(points), str(jury_report.points))
        self.assertEquals(status, jury_report.status)
