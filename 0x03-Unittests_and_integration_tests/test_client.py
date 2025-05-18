#!/usr/bin/env python3
'''client.GithubOrgClient class test'''
from parameterized import parameterized
import client
from client import GithubOrgClient
from unittest.mock import patch
import unittest


class TestGithubOrgClient(unittest.TestCase):
    '''Test class GithubOrgClient'''
    @patch('client.get_json')
    @parameterized.expand([
        ('google', {'login': 'google'}),
        ('abc', {'login': 'abc'})
    ])
    def test_org(self, mock_get_json, org_name, expected):
        '''test the org method'''
        mock_get_json.return_value = expected
        thing = GithubOrgClient(org_name)
        result = thing.org()
        self.assertEqual(result, expected)
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org_name)
        )

    def test_public_repos_url(self):
        '''test GithubOrgClient._public_repos_url'''
        with patch.object(
                GithubOrgClient,
                'org',
                return_value={repos_url:
                              'https://api.github.com/users/google/repos'}
        ) as mock_org:
            result = GithubOrgClient('google')._public_repos-url
            self.assertEqual(
                ressult, 'https://api.github.com/users/google/repos',
            )

    @patch('client.get_json')
    def test_public_repos(self, license, mock_get_json):
        '''test the method public_repos'''
        with patch.object(GithubOrgClient,
                          'public_repos',
                          return_value=["repo1"]) as mock_method:
            result = GithubOrgClient().public_repos()
            self.assertEqual(result, "repo1")
        mock_get_json.assert_called_once()
