import re
from django.shortcuts import redirect, render
from django import forms
from . import util
from django.contrib import messages
import random
import markdown2


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
    if(util.get_entry(title)):
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(),
            "entry": markdown2.markdown(util.get_entry(title)),
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title.capitalize(),
        "entry": None
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
                    return redirect('encyclopedia:create_page')
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


def random_entry(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return redirect('encyclopedia:entry_page', entry)
