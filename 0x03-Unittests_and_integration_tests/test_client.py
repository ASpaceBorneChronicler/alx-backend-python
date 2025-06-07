import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import Mock, patch

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD

class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google"),
        ("abc")
        ])
    @patch('client.GithubOrgClient.org')
    def test_org(self, org_name, mock_org):
        test_class = GithubOrgClient(org_name)
        test_class.org()
        self.assertEqual(test_class._org_name, org_name)
        mock_org.assert_called_once()

        @patch('utils.GithubOrgClient.org')
        def  test_public_repos_url(self, mock_org):
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }
            
            test_class = GithubOrgClient("google")
            result = test_class._public_repos_url
            
            self.assertEqual(result, "https://api.github.com/orgs/google/repos")
            mock_org.assert_called_once()

    @patch('utils.requests.get')
    @patch('client.GithubOrgClient.org')
    def test_public_repos(self, mock_org, mock_get):
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        mock_response = Mock()
        mock_response.json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        mock_get.return_value = mock_response

        test_class = GithubOrgClient("google")
        result = test_class.public_repos()
        self.assertEqual(result, ["repo1", "repo2"])
        mock_get.assert_called_once()

    
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license"),
        ({"license": {"key": "other_license"}}, "my_license")
    ])
    def test_has_lisense(self, repo, license_key):
        test_class = GithubOrgClient("google")
        result = test_class.has_license(repo, license_key)
        self.assertEqual(result, True)

@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1], 
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient that mocks external requests only"""
    
    @classmethod
    def setUpClass(cls):
        """Set up class-level fixtures and start the requests patcher"""
        
        def side_effect_function(url):
            """Returns appropriate fixture based on URL"""
            mock_response = Mock()
             
            if url == "https://api.github.com/orgs/google/repos":
                mock_response.json.return_value = cls.repos_payload
            else:
                # For any other URL, return empty response
                mock_response.json.return_value = {}
            
            return mock_response
        
        # Start the patcher for requests.get
        cls.get_patcher = patch('requests.get', side_effect=side_effect_function)
        cls.get_patcher.start()
    
    @classmethod 
    def tearDownClass(cls):
        """Stop the requests patcher"""
        cls.get_patcher.stop()


if __name__ == '__main__':
    unittest.main()
        