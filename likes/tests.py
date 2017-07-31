from django.test import TestCase, Client
from wagtail.tests.utils import WagtailPageTests

from likes.models import Likes
from likes.views import save_like

from wagtail.wagtailcore.models import Page
from resources.models import ResourcePage

class LikeTestCase(WagtailPageTests):
    def setUp(self):
        parent = Page.objects.get(url_path='/home/')
        page = ResourcePage(title='Title!', slug='test', body='...')
        parent.add_child(instance=page)

    def test_like_resource(self):
        """Liking a resource"""
        c = Client()
        id = ResourcePage.objects.get(slug='test').id
        response = c.post('/like/', {'id': id, 'like': 1})
        like = Likes.objects.get(user_ip="127.0.0.1", resource_id=id)

        self.assertEqual(like.like_value, 1)

    def test_dislike_resource(self):
        """Disliking a resource"""
        c = Client()
        id = ResourcePage.objects.get(slug='test').id
        response = c.post('/like/', {'id': id, 'like': -1})
        like = Likes.objects.get(user_ip="127.0.0.1", resource_id=id)

        self.assertEqual(like.like_value, -1)

    def test_undoing_like(self):
        """Liking a resource twice should undo like"""
        c = Client()
        id = ResourcePage.objects.get(slug='test').id
        response = c.post('/like/', {'id': id, 'like': 1})
        response_2 = c.post('/like/', {'id': id, 'like': 1})

        self.assertRaises(Likes.DoesNotExist, Likes.objects.get, user_ip="127.0.0.1", resource_id=id)

    def test_undoing_dislike(self):
        """Disliking a resource twice should undo dislike"""
        c = Client()
        id = ResourcePage.objects.get(slug='test').id
        response = c.post('/like/', {'id': id, 'like': -1})
        response_2 = c.post('/like/', {'id': id, 'like': -1})

        self.assertRaises(Likes.DoesNotExist, Likes.objects.get, user_ip="127.0.0.1", resource_id=id)

    def test_like_then_dislike(self):
        """Liking a then disliking should dislike"""
        c = Client()
        id = ResourcePage.objects.get(slug='test').id
        response = c.post('/like/', {'id': id, 'like': 1})
        response_2 = c.post('/like/', {'id': id, 'like': -1})

        like = Likes.objects.get(user_ip="127.0.0.1", resource_id=id)

        self.assertEqual(like.like_value, -1)

    def test_dislike_then_like(self):
        """Disliking a then liking should like"""
        c = Client()
        id = ResourcePage.objects.get(slug='test').id
        response = c.post('/like/', {'id': id, 'like': -1})
        response_2 = c.post('/like/', {'id': id, 'like': 1})

        like = Likes.objects.get(user_ip="127.0.0.1", resource_id=id)

        self.assertEqual(like.like_value, 1)
