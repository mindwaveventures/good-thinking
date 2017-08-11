from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase, Tag


class TopicTag(TaggedItemBase):
    content_object = ParentalKey('resources.ResourcePage', related_name='tagged_topic_items')

class IssueTag(TaggedItemBase):
    content_object = ParentalKey('resources.ResourcePage', related_name='tagged_issue_items')

class ReasonTag(TaggedItemBase):
    content_object = ParentalKey('resources.ResourcePage', related_name='tagged_reason_items')

class ContentTag(TaggedItemBase):
    content_object = ParentalKey('resources.ResourcePage', related_name='tagged_content_items')

class HiddenTag(TaggedItemBase):
    content_object = ParentalKey('resources.ResourcePage', related_name='tagged_hidden_items')

class ExcludeTag(TaggedItemBase):
    content_object = ParentalKey('resources.Home', related_name='tagged_exclude_items')
