from django.shortcuts import render, redirect
from . import util
import markdown
from django import forms

# model for getting the input when adding a new entry to the wiki 
class NewEntryForm(forms.Form):
    title = forms.CharField(label="title")
    md = forms.CharField(label="md")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def loadPage(request, filename):
    entry = util.get_entry(filename) # get the md file using get_entry method 
    if(entry == None): # if an exception is thrown "None": no result found
        response = render(request, "encyclopedia/wiki_not_found.html", {
            "title": filename
        })
        response.status_code = 404
        return response
    converted_result = markdown.markdown(entry)
    return render(request, "encyclopedia/show_page.html", {
        "title": filename, 
        "html": converted_result
    })

def createEntry(request):
    if request.method == "POST": 
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["title"]
            entry_md = form.cleaned_data["md"]
            if util.get_entry(entry_title) == None:
                util.save_entry(entry_title, entry_md)
            else:
                return render(request, "encyclopedia/create_entry.html", {
                    "textarea": entry_md,
                    "titleField": entry_title, 
                    "duplicate_title_found": True
                })
        return redirect('loadpage', filename=entry_title)
    return render(request, "encyclopedia/create_entry.html", {
        "textarea": "",
        "titleField": "", 
        "duplicate_title_found": False
    })

def editEntry(request, filename):
    current_title = filename
    requested_entry = util.get_entry(filename)
    if requested_entry == None: 
        response = render(request, "encyclopedia/wiki_not_found.html", {
            "title": filename
        })
        response.status_code = 404
        return response
    if request.method == "POST": 
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["title"]
            entry_md = form.cleaned_data["md"]
            if util.get_entry(entry_title) == None and entry_title != current_title:
                util.save_entry(entry_title, entry_md)
                util.remove_entry(current_title)
            else:
                return render(request, "encyclopedia/edit_entry.html", {
                    "textarea": entry_md,
                    "titleField": entry_title, 
                    "duplicate_title_found": True
                })
        return redirect('loadpage', filename=entry_title)
    return render(request, "encyclopedia/edit_entry.html", {
        "textarea": requested_entry,
        "titleField": filename, 
        "duplicate_title_found": False
    })