import requests

from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)

from .provider import SlackProvider


class SlackOAuth2Adapter(OAuth2Adapter):
    provider_id = SlackProvider.id
    access_token_url = 'https://slack.com/api/oauth.access'
    authorize_url = 'https://slack.com/oauth/authorize'
    auth_test_url = 'https://slack.com/api/auth.test'
    profile_url = 'https://slack.com/api/users.info'
    supports_state = True

    def complete_login(self, request, app, token, **kwargs):
        extra_data = self.get_user_info(token)
        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)

    def get_user_info(self, token):
        info = {}
        resp = requests.get(
            self.auth_test_url,
            params={'token': token.token}
        )
        resp = resp.json()

        if not resp.get('ok'):
            raise OAuth2Error()

        info['team_url'] = resp['url']
        info['user_id'] = resp['user_id']
        info['team_id'] = resp['team_id']

        user = requests.get(
            self.profile_url,
            params={'token': token.token, 'user': resp['user_id']}
        )

        user = user.json()
        if not user['ok']:
            raise OAuth2Error()

        info.update(user['user'])
        return info


oauth2_login = OAuth2LoginView.adapter_view(SlackOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(SlackOAuth2Adapter)
