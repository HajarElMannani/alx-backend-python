#!/usr/bin/env python3
'''client.GithubOrgClient class test'''
from parameterized import parameterized
import client
from client import GithubOrgClient, get_json
from unittest.mock import patch, PropertyMock
import unittest


class TestGithubOrgClient(unittest.TestCase):
    '''Test class GithubOrgClient'''
    @patch('client.get_json')
    @parameterized.expand([
        ('google', {'login': 'google'}),
        ('abc', {'login': 'abc'})
    ])
    def test_org(self, org_name, expected, mock_get_json):
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
                new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {'repos_url':
                                     'https://api.github.com/users/google/repos'}
            result = GithubOrgClient('google')
            self.assertEqual(
                result._public_repos_url, 'https://api.github.com/users/google/repos'
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        '''test the method public_repos'''
        test_payload = [
            {'name': 'repo1', 'license': {'key': 'MIT'}},
            {'name': 'repo2', 'license': {'key': 'AFL-3.0'}}
        ]
        mock_get_json.return_value = test_payload
        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = 'https://api.github.com/users/abc/repos'
            result = GithubOrgClient('abc')
            res = result.public_repos() 
            self.assertEqual(result, ['repo1', 'repo2'])
        mock_get_json.assert_called_once_with(
            'https://api.github.com/users/abc/repos')

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ])
    def test_has_license(self, repo, license_key, expected):
        '''test method has_license'''
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
        
