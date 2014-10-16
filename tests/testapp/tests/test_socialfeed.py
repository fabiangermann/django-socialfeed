from django.test import TestCase

from socialfeed.models import Subscription
from django.contrib.auth.models import User


class SocialfeedTest(TestCase):
    def setUp(self):
        """ Add admin user and log in """
        self.user = User.objects.create_user('admin', '', 'supersecure')
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

        self.client.login(username='admin', password='supersecure')

    def test_adminform(self):
        url = '/admin/socialfeed/subscription/add/'
        response = self.client.get(url)
        form = response.context_data['adminform']

        self.assertEqual(form.form.fields.keys(), ['title', 'provider'])

        response = self.client.post(url, {
            'title': 'Test',
            'provider': 'socialfeed.providers.twitter_stream',
            '_continue': 'Save and continue editing'
        })
