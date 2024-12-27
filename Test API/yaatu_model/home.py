import tkinter as tk
from tkinter import ttk
from ticket_logic import submit_ticket_logic
from ticket_history import ticket_history_logic

""" Homepage Button Functions """
def submit_ticket():
    # Gets member ID and ticket notes from entry fields
    member_id = member_id_entry.get()
    ticket_notes = ticket_notes_entry.get("1.0", tk.END)

    if not member_id or len(ticket_notes) == 1:
        # Checks to see that member ID and ticket notes fields are non-empty
        error_label.config(text="Error: Please fill in all fields.", fg="red")
    elif not len(member_id) == 9:
        # Checks to see if the member ID is exactly 9 digits
        error_label.config(text="Error: Member ID should be 9 digits long.", fg="red")
    elif not member_id[0] in ('1', '2', '3'):
        error_label.config(text="Error: Invalid member ID entered. Must begin with 1, 2, or 3.", fg="red")
    else:
        # If fields are filled out correctly, it resets the page and runs the logic for submitting a ticket from ticket_logic.py file
        error_label.config(text="", fg="red")
        member_id_entry.delete(0, tk.END)
        ticket_notes_entry.delete("1.0", tk.END)
        ticket_frame.grid_remove()
        submitted_ticket_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)
        global frame
        frame = submitted_ticket_frame

        # Perform the logic for submitting a ticket
        category, assignee = submit_ticket_logic(member_id, ticket_notes)

        # Display the result
        ticket_type_solution.config(text=category)
        ticket_assignee_solution.config(text=assignee)


def switch_to_home(old_frame):
    # Logic for when the "Home" button is pressed
    # The nav bar (top_frame) is kept while resetting all frames below it and replacing them with the frame corresponding with the ticket page
    error_label.config(text="", fg="red")
    old_frame.grid_remove()
    ticket_frame.grid()
    if member_id_entry :
        member_id_entry.delete(0, tk.END)
    if ticket_notes_entry :
        ticket_notes_entry.delete('1.0', tk.END)
    member_id_entry.focus()
    global frame
    frame = ticket_frame

def switch_to_my_tickets(old_frame):
    # Logic for when the "My Tickets" button is pressed
    # The nav bar (top_frame) is kept while resetting all frames below it and replacing them with the frame corresponding with the ticket history page
    error_label.config(text="", fg="red")
    old_frame.grid_remove()
    ticket_history_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)
    global frame
    frame = ticket_history_frame


    # Call ticket_history_logic to get ticket history and display it
    history_content_label.config(text=ticket_history_logic())

    

def validate_member_id(char, entry_value):
    # Whenever a key is pressed while in the member ID field, it validates to check that the character is a numerical value and that the length of the entry field is never longer than 10 digits
    return char.isdigit() and len(entry_value) < 10

# Define hover effects
def on_enter(e):
    """Change button color on hover."""
    e.widget.config(background='#0A3891')

def on_leave(e):
    """Revert button color when not hovering."""
    e.widget.config(background='#1866FF')

""" Creating the main window (Homepage) """
root = tk.Tk()
root.title("eSMT Triage Assistant")
root.minsize(400,300)

# Configure styles
style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Arial', 10), background='#1866FF', foreground='white')
style.configure('TEntry', relief='solid', borderwidth=1)
style.configure('TLabel', font=('Arial', 10))
style.configure('TText', relief='solid', borderwidth=1)
style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
style.configure("Bold.TLabel", font=('Arial', 10, "bold"))

# Main frame setup
main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True)
global frame

# Navigation frame setup
top_frame = tk.Frame(main_frame, bg='#0A3891')
main_frame.columnconfigure(0, weight=1)
top_frame.grid(row=0, column=0, sticky='ew')

# Navigation buttons
home_button = tk.Button(top_frame, text="Home", bg='#1866FF', fg='white', command=lambda: switch_to_home(frame))
my_tickets_button = tk.Button(top_frame, text="My Tickets", bg='#1866FF', fg='white', command=lambda: switch_to_my_tickets(frame))
home_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
my_tickets_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Bind hover effects to navigation buttons
home_button.bind("<Enter>", on_enter)
home_button.bind("<Leave>", on_leave)
my_tickets_button.bind("<Enter>", on_enter)
my_tickets_button.bind("<Leave>", on_leave)

""" Ticket Entry Frame Setup """
ticket_frame = tk.Frame(main_frame, bg='white')
frame = ticket_frame
ticket_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)
main_frame.rowconfigure(1, weight=1)
ticket_frame.columnconfigure(1, weight=1)

# Ticket entry widgets
title_label = ttk.Label(ticket_frame, text="Ticket Entry Form", style='Header.TLabel', background='white')
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Member ID input
member_id_label = ttk.Label(ticket_frame, text="Enter member ID: ", style='TLabel', background='white')
member_id_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
member_id_entry = tk.Entry(ticket_frame, relief='solid', borderwidth=1, width=30, validate="key", validatecommand=(root.register(validate_member_id), "%S", "%P"))
member_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky=(tk.W+tk.E))

# Ticket notes input
ticket_notes_label = ttk.Label(ticket_frame, text="Enter ticket notes: ", style='TLabel', background='white')
ticket_notes_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
ticket_notes_entry = tk.Text(ticket_frame, height=5, width=30, relief='solid', borderwidth=1)
ticket_notes_entry.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky=(tk.W+tk.E))

# Submit button
submit_button = tk.Button(ticket_frame, text="Submit", bg='#1866FF', fg='white', command=submit_ticket)
submit_button.grid(row=4, column=0, columnspan=2, pady=10)

# Error Label
error_label = tk.Label(ticket_frame, text="", fg="red", background="white")
error_label.grid(row=5, column=0, columnspan=2, pady=10)

# Bind hover effects to submit button
submit_button.bind("<Enter>", on_enter)
submit_button.bind("<Leave>", on_leave)

""" Submit Ticket Page """
submitted_ticket_frame = tk.Frame(main_frame, bg="white")
submitted_ticket_frame.columnconfigure(0, weight=1)

# Creates title label
ticket_assignment_label = ttk.Label(submitted_ticket_frame, text="Ticket Assignment Details", style='Header.TLabel', background='white')
ticket_assignment_label.grid(row=0, column=0, columnspan=2, pady=10)

# Creates frame for assignment information
assignment_frame = tk.Frame(submitted_ticket_frame, relief="solid", bg='#F3F3F3', highlightbackground='#656667', highlightthickness=2)
assignment_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=20, sticky='ew')

# Placeholder for ticket's type
ticket_type_label = ttk.Label(assignment_frame, text="Ticket Type:", style="Bold.TLabel", background='#F3F3F3')
ticket_type_label.grid(row=1, column=0, padx=[10, 5], pady=5)

ticket_type_solution = ttk.Label(assignment_frame, text="", style='TLabel', background='#F3F3F3')
ticket_type_solution.grid(row=1, column=1, padx=[5, 10], pady=5, sticky=tk.W)

# Placeholder for ticket's assignee
ticket_assignee_label = ttk.Label(assignment_frame, text="Assignee:", style="Bold.TLabel", background='#F3F3F3')
ticket_assignee_label.grid(row=2, column=0, padx=[10, 5], pady=5)

ticket_assignee_solution = ttk.Label(assignment_frame, text="", style='TLabel', background='#F3F3F3')
ticket_assignee_solution.grid(row=2, column=1, padx=[5, 10], pady=5, sticky=tk.W)

""" Ticket History Page """
ticket_history_frame = tk.Frame(main_frame, bg='white')
ticket_history_frame.columnconfigure(1, weight=1)

# Creates title label
history_title_label = ttk.Label(ticket_history_frame, text="Ticket History", style='Header.TLabel', background='white')
history_title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Placeholder for user's ticket history
history_content_label = ttk.Label(ticket_history_frame, text="Ticket history goes here", style='TLabel', background='white')
history_content_label.grid(row=1, column=0, padx=10, pady=5)

""" Starts the Tkinter Event Loop to run application"""
root.mainloop()