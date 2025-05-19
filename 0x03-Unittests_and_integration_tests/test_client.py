#!/usr/bin/env python3
'''client GithubOrgClient class test'''
from parameterized import parameterized, parameterized_class
from requests import HTTPError
import client
from client import GithubOrgClient
from unittest.mock import patch, Mock
import unittest
from fixtures import TEST_PAYLOAD


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
                    'https://api.github.com/orgs/x/repos'}
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
                    'https://api.github.com/orgs/x/repos'}
        mock_get_json.side_effect = [mock_org, test_payload]
        result = GithubOrgClient('abc')
        res = result.public_repos()
        self.assertEqual(res, ['repo1', 'repo2'])
        mock_get_json.assert_call_once_with(
            'https://api.github.com/orgs/x/repos')

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ])
    def test_has_license(self, repo, license_key, expected):
        '''test method has_license'''
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([{'org_payload': TEST_PAYLOAD[0][0],
                       'repos_payload': TEST_PAYLOAD[0][1],
                       'expected_repos': TEST_PAYLOAD[0][2],
                       'apache2_repos': TEST_PAYLOAD[0][3],
                       }])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    '''Class that tests Integration GithubOrgClien'''
    @classmethod
    def setUpClass(cls) -> None:
        '''setting up the class'''
        payload_route = {
            'https://api.github.com/orgs/x/repos': cls.repos_payload,
            'https://api.github.com/orgs/x': cls.org_payload,
        }

        def get_payload(url):
            if url in payload_route:
                return Mock(**{'json.return_value': payload_route[url]})
            return HTTPError
        cls.get_patcher = patch('requests.get', side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        '''test for GithubOrgClient.public_repos'''
        self.assertEqual(GithubOrgClient('x').public_repos(),
                        self.expected_repos,)

    def test_public_repos_with_license(self) -> None:
        '''test public_repos with the
        argument license="apache-2.0"'''
        self.assertEqual(
            GithubOrgClient('x').public_repos(license="apache-2.0"),
            self.apache2_repos,)

    @classmethod
    def tearDownClass(cls) -> None:
        '''tear down the class'''
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()
