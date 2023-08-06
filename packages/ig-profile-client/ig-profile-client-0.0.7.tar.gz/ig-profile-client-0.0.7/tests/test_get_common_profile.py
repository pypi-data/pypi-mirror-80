import unittest
import requests_mock
import requests
from IgProfileClient import Client
from IgProfileClient import Profile


class GetCommonProfile(unittest.TestCase):

    def setUp(self) -> None:
        self.client = Client()

    @requests_mock.Mocker()
    def test_get_common_profile_success(self, mock):
        expected = {
            "full_name": "Full Name",
            "profile_pic": "https://aaa.domain/some_photo.jpg",
            "follower": 9999,
            "following": 9998
        }
        mock.get(
            "https://www.instagram.com/some_user_profile_name/?__a=1",
            json={
                "graphql": {
                    "user": {
                        "full_name": "Full Name",
                        "edge_followed_by": {
                            "count": 9999
                        },
                        "edge_follow": {
                            "count": 9998
                        },
                        "profile_pic_url_hd": "https://aaa.domain/some_photo.jpg"
                    }
                }
            }
        )
        actual = self.client.get_common_profile("some_user_profile_name")
        self.assertTrue(type(actual) is Profile)
        self.assertEqual(expected, actual.__dict__)

    @requests_mock.Mocker()
    def test_get_common_profile_fail_profile_not_found(self, mock):
        raised = False
        expected = "profile not found"
        mock.register_uri(
            'GET',
            "https://www.instagram.com/not_found/?__a=1",
            status_code=404
        )
        try:
            self.client.get_common_profile("not_found")
        except Exception as e:
            raised = True
            self.assertTrue(expected == str(e))
        self.assertTrue(raised)

    @requests_mock.Mocker()
    def test_get_common_profile_fail_cannot_create_connection(self, mock):
        raised = False
        mock.get(
            "https://www.instagram.com/fail_create_connection/?__a=1",
            exc=requests.exceptions.ConnectionError
        )
        try:
            self.client.get_common_profile("fail_create_connection")
        except requests.exceptions.ConnectionError:
            raised = True
        self.assertTrue(raised)

    def test_get_common_profile_fail_username_is_none(self):
        raised = False
        expected = "username should not be none or empty"
        try:
            self.client.get_common_profile(None)
        except Exception as e:
            raised = True
            self.assertTrue(expected == str(e))
        self.assertTrue(raised)

    def test_get_common_profile_fail_username_is_empty(self):
        raised = False
        expected = "username should not be none or empty"
        try:
            self.client.get_common_profile("")
        except Exception as e:
            raised = True
            self.assertTrue(expected == str(e))
        self.assertTrue(raised)

    def test_get_common_profile_fail_username_is_blank(self):
        raised = False
        expected = "username should not be none or empty"
        try:
            self.client.get_common_profile(" ")
        except Exception as e:
            raised = True
            self.assertTrue(expected == str(e))
        self.assertTrue(raised)
