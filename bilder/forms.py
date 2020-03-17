#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render, get_object_or_404, get_list_or_404


class FileFieldForm(forms.Form):
    """ upload multiple images at once """
    file_field = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
