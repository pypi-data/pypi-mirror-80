import requests
import json

base_url = 'https://www.instagram.com/{}/?__a=1'


class Client:

    def get_common_profile(self, username):
        """
        Get Instagram common profile by username

        Arguments:
            - username: ``str``

        Return Profile that including full_name, profile_pic, follower and following
        """
        if not username or username.isspace():
            raise Exception('username should not be none or empty')
        return self._get_profile(
            self._send_request(username)
        )

    @staticmethod
    def _send_request(username):
        return requests.get(base_url.format(username))

    @staticmethod
    def _get_profile(response):
        if response.status_code == 404:
            raise Exception('profile not found')
        response.raise_for_status()
        profile_response = json.loads(response.content, encoding='utf-8')
        return Profile(
            profile_response['graphql']['user']['full_name'],
            profile_response['graphql']['user']['profile_pic_url_hd'],
            profile_response['graphql']['user']['edge_followed_by']['count'],
            profile_response['graphql']['user']['edge_follow']['count']
        )


class Profile:
    def __init__(self, full_name, profile_pic, follower, following):
        self.full_name = full_name
        self.profile_pic = profile_pic
        self.follower = follower
        self.following = following
