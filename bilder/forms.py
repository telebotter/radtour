#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms

class FilterForm(forms.Form):
    tag_lukas = forms.CheckboxSelectMultiple()
    tag_renas = forms.CheckboxSelectMultiple()
    tag_hendrik = forms.CheckboxSelectMultiple()