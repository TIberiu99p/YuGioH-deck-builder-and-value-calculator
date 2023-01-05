import json
import tkinter as tk
from tkinter import messagebox


def search(term):
    with open('cardinfo.json') as f:
        data = json.load(f)

    results = []
    for card in data['data']:
        if term in card['name']:
            results.append(card)

    return results

def search_cards():
    global results
    term = entry.get()
    results = search(term)

    listbox.delete(0, tk.END)
    for result in results:
        listbox.insert(tk.END, result['name'])

def show_card_info(event):
    global results
    index = listbox.curselection()[0]
    card = results[index]

    info_text.delete('1.0', tk.END)
    info_text.insert(tk.END, f"Name: {card['name']}\n")
    info_text.insert(tk.END, f"Type: {card['type']}\n")
    info_text.insert(tk.END, f"Description: {card['desc']}\n")
    info_text.insert(tk.END, f"Race: {card['race']}\n")
    info_text.insert(tk.END, f"Archetype: {card['archetype']}\n")
    info_text.insert(tk.END, f"Cardmarket price: {card['card_prices'][0]['cardmarket_price']}\n")
    info_text.insert(tk.END, f"TCGPlayer price: {card['card_prices'][0]['tcgplayer_price']}\n")
    info_text.insert(tk.END, f"eBay price: {card['card_prices'][0]['ebay_price']}\n")
    info_text.insert(tk.END, f"Amazon price: {card['card_prices'][0]['amazon_price']}\n")
    info_text.insert(tk.END, f"Coolstuffinc price: {card['card_prices'][0]['coolstuffinc_price']}\n")   

def add_to_deck():
    # Make sure an item is selected in the listbox
    if not listbox.curselection():
        return

    # Get the selected card
    index = listbox.curselection()[0]
    card = results[index]

    # Check if the card is already in the deck
    found = False
    for c in deck:
        if c['name'] == card['name']:
            found = True
            # If the card is already in the deck, check if the limit has been reached
            if c['count'] < 3:
                c['count'] += 1
                # Update the deck listbox to show the updated count for the card
                update_deck_listbox()
                return
            else:
                # If the limit has been reached, display an error message
                messagebox.showerror("Error", "You cannot add more than 3 copies of a single card to the deck.")
                return

    # If the card is not already in the deck, add it to the deck with a count of 1
    card['count'] = 1
    deck.append(card)
    # Update the deck listbox to show the added card
    update_deck_listbox()
    if not len(deck) <= 60:
        deck.remove(card)
        messagebox.showerror("Error", "The deck must be between 40 and 60 cards.")

def calculate_total_price(card):
  return card['card_prices'][0]['Cardmarket_price'] * card['count']

total_price = 0

def update_deck_listbox():
    # Clear the deck listbox
    deck_listbox.delete(0, tk.END)

    # Initialize variables to store the total price for each field
    cardmarket_total = 0
    tcgplayer_total = 0
    ebay_total = 0
    amazon_total = 0
    coolstuffinc_total = 0

    # Add each card in the deck to the listbox, along with its count
    for card in deck:
        deck_listbox.insert(tk.END, f"{card['name']} ({card['count']})")
        # Calculate the total price for each field and add it to the appropriate variable
        cardmarket_total += float(card['card_prices'][0]['cardmarket_price']) * card['count']
        tcgplayer_total += float(card['card_prices'][0]['tcgplayer_price']) * card['count']
        ebay_total += float(card['card_prices'][0]['ebay_price']) * card['count']
        amazon_total += float(card['card_prices'][0]['amazon_price']) * card['count']
        coolstuffinc_total += float(card['card_prices'][0]['coolstuffinc_price']) * card['count']

    

    # Add the total price for each field to the listbox
    deck_listbox.insert(tk.END, f"Cardmarket total: {cardmarket_total}")
    deck_listbox.insert(tk.END, f"TCGPlayer total: {tcgplayer_total}")
    deck_listbox.insert(tk.END, f"eBay total: {ebay_total}")
    deck_listbox.insert(tk.END, f"Amazon total: {amazon_total}")
    deck_listbox.insert(tk.END, f"Coolstuffinc total: {coolstuffinc_total}")

# Initialize an empty deck list
deck = []

root = tk.Tk()
root.title("Card Search")

label = tk.Label(root, text="Enter search term:")
entry = tk.Entry(root)
button = tk.Button(root, text="Search", command=search_cards)
listbox = tk.Listbox(root)
info_text = tk.Text(root)
add_button = tk.Button(root, text="Add to Deck", command=add_to_deck)
deck_label = tk.Label(root, text="Deck:")
deck_listbox = tk.Listbox(root)


label.pack(side="top", fill="x")
entry.pack(side="top", fill="x")
button.pack(side="top", fill="x")
listbox.pack(side="left", fill="both", expand=True)
info_text.pack(side="right", fill="both", expand=True)
add_button.pack(side="right", fill="x")
deck_label.pack(side="top", fill="x")
deck_listbox.pack(side="right", fill="both", expand=True)

listbox.bind('<<ListboxSelect>>', show_card_info)

root.mainloop()
