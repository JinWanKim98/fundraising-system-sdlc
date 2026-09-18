import unittest
from unittest.mock import patch
from app import create_app
from control.view_platform_report_controller import view_platform_report_controller

class AccessTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_category_read_routes_require_management(self):
        for route in ['/categories/home', '/categories', '/categories/view']:
            self.assertEqual(self.client.get(route).status_code, 302)
        with self.client.session_transaction() as session:
            session['account_id'] = 1
            session['profile_id'] = 3
        for route in ['/categories/home', '/categories', '/categories/view']:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 302)
            self.assertNotIn('/login', response.location)
        with self.client.session_transaction() as session:
            session['profile_id'] = 4
        with patch('control.view_fundraising_category_controller.view_fundraising_category_controller.viewFundraisingCategory', return_value=[]):
            self.assertEqual(self.client.get('/categories').status_code, 200)
            self.assertEqual(self.client.get('/categories/view').status_code, 200)

class ReportDateTests(unittest.TestCase):
    def test_invalid_dates_stop_before_database(self):
        controller = view_platform_report_controller()
        with patch('control.view_platform_report_controller.PlatformReport') as report:
            for value in ['2025-02-29', 'garbage', '2024-13-01']:
                self.assertFalse(controller.generateDailyReport(value)[0])
            self.assertFalse(controller.generateWeeklyReport('2024-02-30', '2024-03-02')[0])
            self.assertFalse(controller.generateWeeklyReport('2024-03-02', '2024-03-01')[0])
            for year in ['0', '10000', 'bad']:
                self.assertFalse(controller.generateMonthlyReport('2', year)[0])
            report.generateDailyReport.assert_not_called()
            report.generateWeeklyReport.assert_not_called()
            report.generateMonthlyReport.assert_not_called()
            self.assertTrue(controller.generateDailyReport('2024-02-29')[0])
            report.generateDailyReport.assert_called_once_with('2024-02-29')
