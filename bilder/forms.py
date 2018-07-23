#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render, get_object_or_404, get_list_or_404
from bilder.models import Label

class FilterForm(forms.Form):
    LABELS = get_list_or_404(Label, private=False)
    OPTIONS = []
    for lab in LABELS:
        OPTIONS.append(lab.name)
    Filter = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=OPTIONS)