#from bootstrap_datepicker.widgets import DatePicker
from django import forms
from django.forms import ModelForm
from logbuch.models import Logbucheintrag
from main.forms import CustomDatePickerInput, IconTextInput
from bootstrap_datepicker_plus import DatePickerInput #TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput


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
        widget=IconTextInput(attrs={"class": "form-control"}, icon='clock-o', placeholder="Fahrzeit h"),
        required=False)
    strecke = forms.FloatField(
        widget=IconTextInput(attrs={"class": "form-control"}, icon='road', placeholder="Strecke km"),
        required=False)
