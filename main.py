from tkinter import Tk, Button, Canvas, PhotoImage
from pandas import read_csv

BACKGROUND_COLOR = "#B1DDC6"
current_card = ""

# IMPORT DATA #
try:
    flashcard_data = read_csv("data/to_learn.csv")
except FileNotFoundError:
    flashcard_data = read_csv("data/spanish_verbs.csv")


# CHANGE THE FLASHCARD #
def next_card():
    global current_card
    current_card = flashcard_data.sample()
    spanish_word = current_card["spanish"].iloc[0]

    canvas.itemconfig(word_text, text=spanish_word)
    canvas.itemconfig(title_text, text="Spanish")
    canvas.itemconfig(flashcard, image=front_flashcard_image)

    canvas.itemconfig(title_text, fill="black")
    canvas.itemconfig(word_text, fill="black")

    window.after(3000, func=flip_card)


# FLIP THE CARD #
def flip_card():
    global current_card
    english_word = current_card["english"].iloc[0]

    canvas.itemconfig(word_text, text=english_word)
    canvas.itemconfig(title_text, text="English")
    canvas.itemconfig(flashcard, image=back_flashcard_image)

    canvas.itemconfig(title_text, fill="white")
    canvas.itemconfig(word_text, fill="white")


# THE WORD IS ALREADY KNOWN, PREVENT REAPPEARING #
def pop_word():
    global current_card
    global flashcard_data
    flashcard_data = flashcard_data.drop(index=current_card.index)
    next_card()


# USER INTERFACE
window = Tk()
window.title("Flashcards: Verbs")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_flashcard_image = PhotoImage(file="images/card_front.png")
back_flashcard_image = PhotoImage(file="images/card_back.png")
flashcard = canvas.create_image(400, 263, image=front_flashcard_image)
canvas.grid(column=1, row=1, columnspan=2)

# Labels
title_text = canvas.create_text(400, 150, text="Spanish", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="Word", font=("Arial", 60, "bold"), width=700, anchor="center")

# Buttons
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightbackground=BACKGROUND_COLOR, command=pop_word)
right_button.grid(column=1, row=2)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightbackground=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(column=2, row=2)

next_card()

window.mainloop()

# EXPORT DATA
flashcard_data.to_csv("data/to_learn.csv")
