from urllib.parse import parse_qs

from django.shortcuts import render

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailforms.models import AbstractForm
from forms.models import CmsFormField

class FormField(CmsFormField):
    parental_key = 'FeedbackPage'
    custom_panels = True

class FeedbackPage(AbstractForm):
    alphatext = RichTextField(blank=True, help_text="Why to take part in the alpha")

    content_panels = AbstractForm.content_panels + [
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('alphatext', classname="full"),
    ]

    # to see how the serve function has been edited, see the original function here:
    # https://github.com/wagtail/wagtail/blob/master/wagtail/wagtailforms/models.py#L238
    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form(request.POST, page=self, user=request.user)

            if form.is_valid():
                self.process_form_submission(form)

                # render the landing_page
                # TODO: It is much better to redirect to it
                return render(
                    request,
                    self.get_landing_page_template(request),
                    self.get_context(request)
                )
        else:
            form = self.get_form(page=self, user=request.user)

        # custom
        custom_form = []

        vals = FormField.objects.all().filter(page_id=form.page.id)

        for val in vals:
            dict = {}
            dict['before_input'] = val.before_input
            dict['after_input'] = val.after_input
            dict['field_type'] = val.field_type
            dict['default_value'] = val.default_value
            dict['label'] = val.label

            # TODO: look at a nicer way to fetch errors and submitted_val
            
            request_dict = parse_qs(request.body.decode('utf-8'))

            if val.field_type == 'radio':
                choices_list = []
                choices = val.choices.split(",")
                for choice in choices:
                    try:
                        submitted_val = request_dict[val.label][0]
                    except:
                        submitted_val = False
                    choice = 'checked' if choice == submitted_val else ''
                    choices_list.append({'val': choice, 'checked': checked})
                dict['choices'] = choices_list
            else:
                try:
                    dict['submitted_val'] = request_dict[val.label][0]
                except:
                    dict['submitted_val'] = ''

            dict['required'] = 'required' if val.required else ''

            if form.errors:
                try:
                    dict['errors'] = form.errors.as_data()[val.label][0]
                except:
                    pass

            custom_form.append(dict)

        context = self.get_context(request)
        context['form'] = form
        context['custom_form'] = custom_form # custom

        return render(
            request,
            self.get_template(request),
            context
       ) 
