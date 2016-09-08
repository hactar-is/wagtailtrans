from __future__ import absolute_import, unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy

from wagtail.wagtailadmin.views.generic import (
    CreateView, DeleteView, EditView, IndexView)
from wagtail.wagtailtrans.models import Language


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = (
            'code',
            'is_default',
            'order',
            'live',
        )


class Index(IndexView):
    model = Language
    context_object_name = 'languages'
    template_name = 'wagtailtrans/languages/index.html'
    add_url_name = 'wagtailtrans_languages:add'
    page_title = ugettext_lazy("Languages")
    add_item_label = ugettext_lazy("Add a language")
    header_icon = 'folder-open-1'


class Create(CreateView):
    form_class = LanguageForm
    page_title = ugettext_lazy("Add language")
    success_message = ugettext_lazy("Language '{0}' created.")
    add_url_name = 'wagtailtrans_languages:add'
    edit_url_name = 'wagtailtrans_languages:edit'
    index_url_name = 'wagtailtrans_languages:index'
    header_icon = 'folder-open-1'


class Edit(EditView):
    model = Language
    form_class = LanguageForm
    success_message = ugettext_lazy("Language '{0}' updated.")
    error_message = ugettext_lazy(
        "The language could not be saved due to errors.")
    delete_item_label = ugettext_lazy("Delete language")
    edit_url_name = 'wagtailtrans_languages:edit'
    index_url_name = 'wagtailtrans_languages:index'
    delete_url_name = 'wagtailtrans_languages:delete'
    context_object_name = 'languages'
    header_icon = 'folder-open-1'


class Delete(DeleteView):
    model = Language
    success_message = ugettext_lazy("Language '{0}' deleted.")
    index_url_name = 'wagtailtrans_languages:index'
    delete_url_name = 'wagtailtrans_languages:delete'
    page_title = ugettext_lazy("Delete language")
    confirmation_message = ugettext_lazy(
        "Are you sure you want to delete this language?")
    header_icon = 'folder-open-1'
