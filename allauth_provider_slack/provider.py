from urlparse import urljoin

from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class SlackAccount(ProviderAccount):
    def get_profile_url(self):
        team_url = self.account.extra_data.get('team_url', '')
        name = self.account.extra_data.get('name', '')
        if team_url and name:
            return urljoin(team_url, 'team/{}'.format(name))
        return ''

    def get_avatar_url(self):
        return self.account.extra_data.get(
            'profile', {}).get('image_original', '')

    def to_str(self):
        dflt = super(SlackAccount, self).to_str()
        return '%s (%s)' % (
            self.account.extra_data.get('user', ''),
            dflt,
        )


class SlackProvider(OAuth2Provider):
    id = 'slack'
    name = 'Slack'
    package = 'allauth_provider_slack'
    account_class = SlackAccount

    def extract_uid(self, data):
        return str(data['user_id'])

    def extract_common_fields(self, data):
        profile = data['profile']
        return dict(username=data['name'],
                    first_name=profile.get('first_name'),
                    last_name=profile.get('last_name'),
                    email=profile.get('email')
                    )


providers.registry.register(SlackProvider)
