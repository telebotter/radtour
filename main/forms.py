from django import forms
from django.forms import ModelForm
from main.models import Tour
from colorful.fields import RGBColorField
from bootstrap_datepicker_plus import DatePickerInput #TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput


class CustomDatePickerInput(DatePickerInput):
    template_name = 'main/datepicker.html'


class IconTextInput(forms.TextInput):
    template_name = 'main/icontextinput.html'
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


class CustomColorPickerInput(forms.TextInput):
    template_name = 'main/colorpicker.html'


class TourForm(ModelForm):
    class Meta:
        model = Tour
        fields = ['start_datum', 'color', 'bericht']
        # inlinefields = ['start_datum']
    # datum = forms.DateField(widget=forms.SelectDateWidget(), required=True)
    start_datum = forms.DateField(
        widget=CustomDatePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "locale": "de",}),
        required=False)
    # color = forms.Field(widget=CustomColorPickerInput)
