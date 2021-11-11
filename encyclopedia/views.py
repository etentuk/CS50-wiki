import re
from django.shortcuts import redirect, render
from django import forms
from django.urls import reverse
from . import util
from django.http.response import HttpResponseRedirect
from django.contrib import messages


class SearchForm(forms.Form):
    q = forms.CharField()


class NewPageForm(forms.Form):
    title = forms.CharField()
    markdown_content = forms.CharField(widget=forms.Textarea)


class EditPageForm(forms.Form):
    markdown_content = forms.CharField(widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    print('You did not call sir')
    return render(request, "encyclopedia/entry.html", {
        "title": title.capitalize(),
        "entry": util.get_entry(title),
    })


def search_results(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        entries = util.list_entries()
        matching_entries = []
        if form.is_valid():
            query = form.cleaned_data["q"]
            for entry in entries:
                if entry.lower() == query.lower():
                    return entry_page(request, query)
                elif query.lower() in entry.lower():
                    matching_entries += [entry]
        return render(request, "encyclopedia/search.html", {
            "matching_entries": matching_entries
        })


def create_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        entries = util.list_entries()
        if form.is_valid():
            title = form.cleaned_data["title"]
            markdown_content = form.cleaned_data["markdown_content"]
            for entry in entries:
                if title.lower() == entry.lower():
                    messages.info(request, 'Page Already Exists')
                    return create_page(request)
            util.save_entry(title, markdown_content)
            return redirect('encyclopedia:entry_page', title)
    return render(request, "encyclopedia/create_page.html", {
        "form": NewPageForm()
    })


def edit_page(request, title):
    entry = util.get_entry(title)
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            edited_entry = form.cleaned_data["markdown_content"]
            util.save_entry(title, edited_entry)
            return redirect('encyclopedia:entry_page', title)
    return render(request, "encyclopedia/edit_page.html", {
        "form": EditPageForm({"markdown_content": entry}),
        "title": title
    })
