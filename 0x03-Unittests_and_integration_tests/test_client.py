#!/usr/bin/env python3
'''client GithubOrgClient class test'''
from parameterized import parameterized
import client
from client import GithubOrgClient
from unittest.mock import patch
import unittest


class TestGithubOrgClient(unittest.TestCase):
    '''Test class GithubOrgClient'''
    @parameterized.expand([
        ('google', {'login': 'google'}),
        ('abc', {'login': 'abc'})
    ])
    def test_org(self, org_name, expected):
        '''test the org method'''
        with patch('client.get_json', return_value=expected) as mock_get_json:
            thing = GithubOrgClient(org_name)
            result = thing.org
            self.assertEqual(result, expected)
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/{}".format(org_name)
            )

    def test_public_repos_url(self):
        '''test GithubOrgClient._public_repos_url'''
        mock_org = {'repos_url':
                    'https://api.github.com/users/x/repos'}
        with patch(
                'client.get_json',
                return_value=mock_org):
            obj = GithubOrgClient('x')
            result = obj._public_repos_url
            self.assertEqual(
                result, mock_org['repos_url'])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        '''test the method public_repos'''
        test_payload = [
            {'name': 'repo1', 'license': {'key': 'MIT'}},
            {'name': 'repo2', 'license': {'key': 'AFL-3.0'}}
        ]
        mock_org = {'repos_url':
                    'https://api.github.com/users/x/repos'}
        mock_get_json.side_effect = [mock_org, test_payload]
        result = GithubOrgClient('abc')
        res = result.public_repos() 
        self.assertEqual(res, ['repo1', 'repo2'])
        mock_get_json.assert_any_call(
            'https://api.github.com/users/x/repos')
        self.assertEqual(mock_get_json.call_count, 1)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ])
    def test_has_license(self, repo, license_key, expected):
        '''test method has_license'''
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
        
if __name__ == "__main__":
    unittest.main()
