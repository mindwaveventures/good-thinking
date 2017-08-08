from django.test import TestCase, Client
from wagtail.tests.utils import WagtailPageTests

from wagtail.wagtailcore.models import Page
from wagtail.wagtailforms.models import FormSubmission
from resources.models import ResourcePage, IssueTag, TopicTag, ContentTag, Home, filter_tags, handle_request, valid_request, generate_custom_form

from taggit.models import Tag

class TagsTestCase(WagtailPageTests):
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

class HomeTestCase(TestCase):
    def test_valid_request(self):
        """valid_request :: inputs which are valid in the request"""
        request_ = {'suggestion': 'suggestion'}
        actual = valid_request(request_)
        expected = True

        self.assertEqual(actual, expected)

        request_ = {'email': 'email'}
        actual = valid_request(request_)
        expected = True

        self.assertEqual(actual, expected)

        request_ = {'notAKey': ''}
        actual = valid_request(request_)
        expected = False

        self.assertEqual(actual, expected)

    def test_handle_request(self):
        """handle_request :: redirects to the correct path"""
        class RequestSuggestion(object):
            session = {'suggestion': False}
            path = "/"

        class RequestEmail(object):
            session = {'email': False}
            path = "/"

        class Messages(object):
            def info(_request, field):
                return field
        messages = Messages
        request = RequestSuggestion
        request_dict = {'suggestion': 'suggestion'}
        def cb(path):
            return path

        self.assertEqual(
            '/#suggestion_form',
            handle_request(request, request_dict, cb, messages)
        )

        request = RequestEmail
        request_dict = {'email': 'email'}

        self.assertEqual(
            '/#alphasection',
            handle_request(request, request_dict, cb, messages)
        )

    def test_generate_custom_form_no_submitted_val(self):
        """generate_custom_form :: generates a custom form list for template with no submitted_val"""
        class Field1(object):
            field_type = "multiline"
            default_value = ""
            help_text = ""
            label = "suggestion"
            required = False

        class Field2(object):
            field_type = "email"
            default_value = ""
            help_text = ""
            label = "email"
            required = False

        form_fields = [Field1, Field2]
        request_dict = {}
        messages = []

        actual = generate_custom_form(
            form_fields,
            request_dict,
            messages
        )

        self.assertEqual(
            actual,
            [{
              'field_type': 'multiline',
              'default_value': '',
              'help_text': '',
              'label': 'suggestion',
              'submitted_val': '',
              'required': '',
              'email_submitted': False,
              'suggestion_submitted': False
            },
            {
              'field_type': 'email',
              'default_value': '',
              'help_text': '',
              'label': 'email',
              'submitted_val': '',
              'required': '',
              'email_submitted': False,
              'suggestion_submitted': False
            }]
        )

    def test_generate_custom_form_submitted_val(self):
        """generate_custom_form :: generates a custom form list for template with submitted_val"""
        class Field1(object):
            field_type = "multiline"
            default_value = ""
            help_text = ""
            label = "suggestion"
            required = False

        class Field2(object):
            field_type = "email"
            default_value = ""
            help_text = ""
            label = "email"
            required = False

        form_fields = [Field1, Field2]
        request_dict = {'suggestion': ['suggestion']}
        messages = ['suggestion']

        actual = generate_custom_form(
            form_fields,
            request_dict,
            messages
        )

        self.assertEqual(
            actual,
            [{
              'field_type': 'multiline',
              'default_value': '',
              'help_text': '',
              'label': 'suggestion',
              'submitted_val': 'suggestion',
              'required': '',
              'email_submitted': False,
              'suggestion_submitted': True
            },
            {
              'field_type': 'email',
              'default_value': '',
              'help_text': '',
              'label': 'email',
              'submitted_val': '',
              'required': '',
              'email_submitted': False,
              'suggestion_submitted': True
            }]
        )
