"""Lightweight Tk desktop interface."""
import tkinter as tk
from tkinter import ttk, messagebox
from .catalog import find_offers, open_offer

def run():
    root = tk.Tk()
    root.title("ePlus AI Portal")
    root.geometry("900x560")
    root.minsize(680, 460)
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="ePlus AI Portal", font=("TkDefaultFont", 22, "bold")).pack(anchor="w")
    ttk.Label(frame, text="Explore published Google AI offers • No emulator required").pack(anchor="w", pady=(4, 16))

    query = tk.StringVar()
    ttk.Label(frame, text="Search offers").pack(anchor="w")
    search = ttk.Entry(frame, textvariable=query)
    search.pack(fill="x", pady=(4, 12))
    columns = ("title", "provider", "region")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=5, selectmode="browse")
    for name, label, width in (("title", "Offer", 310), ("provider", "Provider", 120), ("region", "Region", 160)):
        tree.heading(name, text=label)
        tree.column(name, width=width, minwidth=90)
    tree.pack(fill="x")

    details = tk.Text(frame, height=8, wrap="word", relief="flat", padx=8, pady=8)
    details.pack(fill="both", expand=True, pady=12)
    details.configure(state="disabled")
    current = {}

    def selected():
        selection = tree.selection()
        return current.get(selection[0]) if selection else None

    def render(_event=None):
        offer = selected()
        details.configure(state="normal")
        details.delete("1.0", "end")
        if offer:
            details.insert("end", f"{offer.description}\n\nEligibility: {offer.eligibility}\n"
                           f"Region: {offer.region}\nSource reviewed: {offer.reviewed}\n"
                           f"Official page: {offer.url}")
        else:
            details.insert("end", "Select an offer to view details.")
        details.configure(state="disabled")
        button.configure(state="normal" if offer else "disabled")

    def launch():
        offer = selected()
        if offer:
            try:
                if not open_offer(offer):
                    messagebox.showerror("Browser unavailable", "Open the official URL manually.")
            except (ValueError, OSError) as exc:
                messagebox.showerror("Unable to open", str(exc))

    button = ttk.Button(frame, text="Open official offer page", command=launch)
    button.pack(anchor="e")
    ttk.Label(frame, text="Informational catalog only. Eligibility is determined by the provider.",
              wraplength=650).pack(anchor="w", pady=(10, 0))

    def refresh(*_args):
        for row in tree.get_children():
            tree.delete(row)
        current.clear()
        for offer in find_offers(query.get()):
            current[offer.id] = offer
            tree.insert("", "end", iid=offer.id, values=(offer.title, offer.provider, offer.region))
        rows = tree.get_children()
        if rows:
            tree.selection_set(rows[0])
        render()

    query.trace_add("write", refresh)
    tree.bind("<<TreeviewSelect>>", render)
    refresh()
    search.focus_set()
    root.mainloop()
