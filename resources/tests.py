from django.test import TestCase, Client
from wagtail.tests.utils import WagtailPageTests

from wagtail.wagtailcore.models import Page
from resources.models import ResourcePage, IssueTag, TopicTag, ContentTag, filter_tags

from taggit.models import Tag

class LikeTestCase(WagtailPageTests):
    def setUp(self):
        parent = Page.objects.get(url_path='/home/')
        page = ResourcePage(title='Title!', slug='test', body='...')
        page_2 = ResourcePage(title='Page Title 2', slug='test2', body='...')
        parent.add_child(instance=page)
        parent.add_child(instance=page_2)
        resource_tags = [
            (IssueTag, Tag.objects.create(name='insomnia')),
            (IssueTag, Tag.objects.create(name='sleep-deprivation')),
            (ContentTag, Tag.objects.create(name='long-term-solution')),
            (TopicTag, Tag.objects.create(name='depression')),
        ]
        resource_tags_2 = [
            (IssueTag, Tag.objects.create(name='anxiety')),
            (IssueTag, Tag.objects.create(name='depressed')),
            (ContentTag, Tag.objects.create(name='blog')),
        ]

        for (tag_type, tag) in resource_tags:
            tag_type.objects.create(content_object=page, tag=tag)

        for (tag_type, tag) in resource_tags_2:
            tag_type.objects.create(content_object=page_2, tag=tag)

    def test_filtering_issues_by_topic(self):
        """Filtering issues by topic"""
        all_issue_tags = IssueTag.objects.all();

        depression = Tag.objects.get(name='depression')

        filtered_issue_tags, _filtered_reason_tags, _filtered_content_tags = filter_tags(ResourcePage.objects.filter(topic_tags=depression), 'depression')

        self.assertEqual(len(all_issue_tags), 4)
        self.assertEqual(len(filtered_issue_tags), 2)

    def test_filtering_content_by_topic(self):
        """Filtering content by topic"""
        all_content_tags = ContentTag.objects.all();

        depression = Tag.objects.get(name='depression')

        _filtered_issue_tags, _filtered_reason_tags, filtered_content_tags = filter_tags(ResourcePage.objects.filter(topic_tags=depression), 'depression')

        self.assertEqual(len(all_content_tags), 2)
        self.assertEqual(len(filtered_content_tags), 1)
