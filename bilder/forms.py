#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms

class FilterForm(forms.Form):
    OPTIONS = (
        ("AUT", "Austria"),
        ("DEU", "Germany"),
        ("NLD", "Neitherlands"),
    )
    Countries = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=OPTIONS)