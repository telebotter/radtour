#from bootstrap_datepicker.widgets import DatePicker
from django import forms
from django.forms import ModelForm
from logbuch.models import Logbucheintrag
from bootstrap_datepicker_plus import DatePickerInput #TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput


class CustomDatePickerInput(DatePickerInput):
    template_name = 'logbuch/datepicker.html'

""" from django.forms source
class Input(Widget):
    input_type = None  # Subclasses must define this.
    template_name = 'django/forms/widgets/input.html'

    def __init__(self, attrs=None):
        if attrs is not None:
            attrs = attrs.copy()
            self.input_type = attrs.pop('type', self.input_type)
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['type'] = self.input_type
        return context


class TextInput(Input):
    input_type = 'text'
    template_name = 'django/forms/widgets/text.html'
"""

class IconTextInput(forms.TextInput):
    template_name = 'logbuch/icontextinput.html'
    input_type = 'text'

    def __init__(self, attrs=None, icon='font', placeholder=None):
        super().__init__(attrs=attrs)
        self.icon = icon # this can be used in context
        self.placeholder = placeholder

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['icon'] = self.icon  # this can be used in template
        context['placeholder'] = self.placeholder
        return context


class LogForm(ModelForm):
    class Meta:
        model = Logbucheintrag
        fields = ['datum', 'strecke', 'uptime', 'hoehe', 'text']
        inlinefields = ['datum', 'strecke', 'uptime', 'hoehe']
    # datum = forms.DateField(widget=forms.SelectDateWidget(), required=True)
    datum = forms.DateField(
        widget=CustomDatePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "locale": "de",}),
        required=True)
    hoehe = forms.FloatField(
        widget=IconTextInput(attrs={"class": "form-control"}, icon='arrows-v', placeholder="Aufstieg m"),
        required=False)
    uptime = forms.FloatField(
        widget=IconTextInput(attrs={"class": "form-control", 'required':False}, icon='clock-o', placeholder="Fahrzeit h"),
        required=False)
    strecke = forms.FloatField(
        widget=IconTextInput(icon='road', placeholder="Strecke km"),
        required=False)
