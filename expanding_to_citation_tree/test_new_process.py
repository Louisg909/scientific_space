
import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import requests
import time

import commands as pm
from new_process import get_paper_details, paper_in_db, add_paper_db, add_reference_db, build_citation_tree

class TestPaperFunctions(unittest.TestCase):

    @patch('requests.get')
    def test_get_paper_details_success(self, mock_get):
        paper_id = 'test_id'
        expected_result = {
            'title': 'Test Paper',
            'abstract': 'This is a test abstract.',
            'references': []
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected_result

        result = get_paper_details(paper_id)
        self.assertEqual(result, expected_result)

    @patch('requests.get')
    def test_get_paper_details_failure(self, mock_get):
        paper_id = 'test_id'
        mock_get.return_value.status_code = 404

        result = get_paper_details(paper_id)
        self.assertIsNone(result)

    @patch('commands.grab')
    def test_paper_in_db(self, mock_grab):
        paper_details = {
            'title': 'Test Paper',
            'abstract': 'This is a test abstract.',
            'authors': [{'name': 'Alice'}, {'name': 'Bob'}],
            'year': '2023',
            'fieldsOfStudy': ['Computer Science']
        }
        mock_grab.return_value = [('Test Paper', 'This is a test abstract.', '2023')]

        result = paper_in_db(paper_details)
        self.assertTrue(result)

        mock_grab.return_value = None
        result = paper_in_db(paper_details)
        self.assertFalse(result)

    @patch('sqlite3.connect')
    def test_add_reference_db(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        parent_id = 1
        child_id = 2
        add_reference_db(parent_id, child_id)

        mock_conn.cursor().execute.assert_called_once_with('''
            INSERT INTO references (parent_id, child_id)
            VALUES (?, ?)
        ''', (parent_id, child_id))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('new_process.get_paper_details')
    @patch('new_process.paper_in_db')
    @patch('new_process.add_paper_db')
    @patch('new_process.add_reference_db')
    def test_build_citation_tree(self, mock_add_reference_db, mock_add_paper_db, mock_paper_in_db, mock_get_paper_details):
        paper_id = 'test_id'
        paper_details = {
            'title': 'Test Paper',
            'abstract': 'This is a test abstract.',
            'references': [{'paperId': 'ref_id1'}, {'paperId': 'ref_id2'}]
        }
        mock_get_paper_details.return_value = paper_details
        mock_paper_in_db.return_value = False
        mock_add_paper_db.return_value = 1

        result = build_citation_tree(paper_id, depth=2)
        self.assertEqual(result, 1)
        mock_add_reference_db.assert_any_call(1, None)  # Check that add_reference_db was called

        # Test with a depth of 0
        result = build_citation_tree(paper_id, depth=0)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
