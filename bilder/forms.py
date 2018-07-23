#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms

class FilterForm(forms.Form):
    tag_lukas = forms.CheckboxSelectMultiple(label='Lukas', default=False)
    tag_renas = forms.CheckboxSelectMultiple(label='Renas', default=False)
    tag_hendrik = forms.CheckboxSelectMultiple(label='Hendrik', default=False)