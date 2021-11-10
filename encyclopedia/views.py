import re
from django.shortcuts import render, redirect
from django import forms
from django.urls.base import resolve
from . import util
from django.http.response import HttpResponseRedirect
# from django.urls import reverse


class SearchForm(forms.Form):
    q = forms.CharField()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title.capitalize(),
        "entry": util.get_entry(title),
    })


def search_results(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        entries = util.list_entries()
        if form.is_valid():
            query = form.cleaned_data["q"]
            matching_entries = []
            for entry in entries:
                if entry.lower() == query.lower():
                    return entry_page(request, query)
                elif query.lower() in entry.lower():
                    matching_entries += [entry]
        return render(request, "encyclopedia/search.html", {
            "matching_entries": matching_entries
        })
