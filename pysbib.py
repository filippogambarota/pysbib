import tkinter as tk
from tkinter import Listbox, Entry
from fuzzywuzzy import fuzz
from pybtex.database import parse_file
import pyperclip

bib_file = 'references.bib'
bib_data = parse_file(bib_file)

titles = []
authors = []
keys = []
i = 0

for key in bib_data.entries:
    pps = bib_data.entries[key].persons['Author']
    keys.append(key)
    titles.append(bib_data.entries[key].fields["title"])
    auts = []
    for i in range(len(pps)):
        auts.append(pps[i].last())
    auts = [x[0] for x in auts]
    if len(auts) > 3:
        idx = set([1,2,3])
        auts = [el for i, el in enumerate(auts) if i in idx]
    authors.append(", ".join(auts))

bibdict = []

for i in range(len(keys)):
    dd = {}
    dd["key"] = keys[i]
    dd["title"] = titles[i]
    dd["authors"] = authors[i]
    bibdict.append(dd)

tdisp = []

for i in range(len(bibdict)):
    tdisp.append('{}\n\n@{} | {}'.format(bibdict[i]["title"], bibdict[i]["key"], bibdict[i]["authors"]))


def create_display_list(query):
    display_items = []
    for item in bibdict:
        for field in item:
            if query.lower() in str(item[field]).lower() or fuzz.ratio(query.lower(), str(item[field]).lower()) > 80:
                display_items.append(item)
                break
    return display_items

def update_results(event=None):
    query = entry.get()
    display_items = create_display_list(query)
    results.delete(0, tk.END)  # Clear previous results
    for item in display_items:
        # You can customize how the item is displayed here
        display_text = '{}\n\n@{} | {}'.format(item["title"],item["key"], item["authors"])
        results.insert(tk.END, display_text)

def on_enter(event):
    selected_item = results.get(results.curselection())
    if selected_item:
        #messagebox.showinfo("Selected Item", f"You selected: {selected_item}")
        idx = tdisp.index(selected_item)
        pyperclip.copy('@{}'.format(keys[idx]))
        pyperclip.paste()

root = tk.Tk()
root.title("Fuzzy Search")

entry = Entry(root, width=70)
entry.pack()
entry.bind("<KeyRelease>", update_results)

results = Listbox(root, width=70)
results.pack()

# Bind the Enter key to a function that displays the selected item
root.bind("<Return>", on_enter)

root.mainloop()
