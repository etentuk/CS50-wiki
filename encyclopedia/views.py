import re
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title.capitalize(),
        "entry": util.get_entry(title)
    })
