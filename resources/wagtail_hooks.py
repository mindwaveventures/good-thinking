from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html
from wagtail.wagtailcore.whitelist import attribute_rule, check_url

from wagtail.wagtailcore import hooks


@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('css/wagtail.css')
    )


@hooks.register('insert_editor_js')
def enable_source():
    return format_html(
        """
        <script>
            registerHalloPlugin('hallohtml');
        </script>
        """
    )


@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    return {
        'a': attribute_rule({
            'href': check_url, 'id': True, 'class': True, 'style': True
        }),
        'button': attribute_rule({'id': True, 'class': True, 'style': True})
    }
