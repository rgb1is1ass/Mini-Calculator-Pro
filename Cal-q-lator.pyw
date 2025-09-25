import tkinter as tk
from tkinter import ttk
import math

# --- Global Variables for Calculator Logic ---
current_input = "0"
first_operand = None
operator = None
waiting_for_second_operand = False
memory_value = 0
history_list = [] # List to store calculation history

# --- Calculator Logic Functions ---

def update_display():
    """Updates the display entry with the current_input string."""
    display_var.set(current_input)

def button_click(char):
    """Handles clicks for number and decimal point buttons."""
    global current_input, waiting_for_second_operand

    if waiting_for_second_operand:
        current_input = char
        waiting_for_second_operand = False
    
    else:
        if current_input == "0" and char != ".":
            current_input = char
        elif char == "." and "." in current_input:
            pass
        else:
            current_input += char
    update_display()

def operator_click(op):
    """Handles clicks for operator buttons (+, -, *, /, ^)."""
    global first_operand, operator, current_input, waiting_for_second_operand

    if first_operand is not None and waiting_for_second_operand:
        operator = op
        return

    if first_operand is not None and operator is not None and not waiting_for_second_operand:
        calculate_result()
        if current_input == "Error": # If previous calculation resulted in an error, don't set first_operand
            return
        first_operand = float(current_input)
        operator = op
        waiting_for_second_operand = True
        return

    first_operand = float(current_input)
    operator = op
 
    waiting_for_second_operand = True
    update_display()

def calculate_result():
    """Performs the calculation when '=' is pressed and adds to history."""
    global current_input, first_operand, operator, waiting_for_second_operand, history_list

    if first_operand is None or operator is None:
        return

    # Store string representation of operands for history
    first_operand_str = str(first_operand)
    second_operand_str = current_input

    try:
        second_operand_float = float(current_input)
        result = 0

        if operator == "+":
            result = first_operand + second_operand_float
        elif operator == "-":
            result = first_operand - second_operand_float
        elif operator == "*":
            result = first_operand * second_operand_float
        elif operator == "/":
            if second_operand_float == 0:
                current_input = "Error"
                return
            result = first_operand / second_operand_float
        elif operator == "%":
            if second_operand_float != 0:
                result = (first_operand / 100) * second_operand_float
            else:
                result = first_operand / 100
        elif operator == "^": # Power operator (x^y)
            result = first_operand ** second_operand_float

    except Exception as e:
        current_input = "Error"
    else:
        rounded_result = round(result, 12)

        if rounded_result == int(rounded_result):
            current_input = str(int(rounded_result))
        else:
            current_input = str(rounded_result)

        # Add to history AFTER successful calculation and current_input is updated
        history_list.append(f"{first_operand_str} {operator} {second_operand_str} = {current_input}")

    finally:
        update_display()
        first_operand = None
        operator = None
        waiting_for_second_operand = True

# --- Clear Functions ---
def all_clear():
    """Clears the display and resets all calculation variables."""
    global current_input, first_operand, operator, waiting_for_second_operand
    current_input = "0"
    first_operand = None
    operator = None
    waiting_for_second_operand = False
    update_display()

def clear_entry():
    """Clears only the current input on the display, without affecting stored operations."""
    global current_input, waiting_for_second_operand
    current_input = "0"
    waiting_for_second_operand = False
    update_display()

def backspace():
    """Removes the last character from the display."""
    global current_input
    if current_input == "Error":
        all_clear()
        return

    if len(current_input) > 1 and current_input != "0":
        current_input = current_input[:-1]
    else:
        current_input = "0"
    update_display()

# --- Scientific Functions (Single Operand or Constant) ---
def negate_number():
    """Changes the sign of the current number on the display."""
    global current_input
    if current_input != "0" and current_input != "Error":
        if current_input.startswith('-'):
            current_input = current_input[1:]
        else:
            current_input = '-' + current_input
    update_display()

def square_root():
    """Calculates the square root of the current number."""
    global current_input, first_operand, operator, waiting_for_second_operand
    try:
        num = float(current_input)
        if num < 0:
            current_input = "Error"
        else:
            result = math.sqrt(num)
            rounded_result = round(result, 12)
            if rounded_result == int(rounded_result):
                current_input = str(int(rounded_result))
            else:
                current_input = str(rounded_result)
    except ValueError:
        current_input = "Error"
    finally:
        update_display()
        first_operand = None
        operator = None
        waiting_for_second_operand = True

def power_of_two():
    """Calculates the square of the current number (x^2)."""
    global current_input, first_operand, operator, waiting_for_second_operand
    try:
        num = float(current_input)
        result = num ** 2
        rounded_result = round(result, 12)
        if rounded_result == int(rounded_result):
            current_input = str(int(rounded_result))
        else:
            current_input = str(rounded_result)
    except ValueError:
        current_input = "Error"
    finally:
        update_display()
        first_operand = None
        operator = None
        waiting_for_second_operand = True

def reciprocal():
    """Calculates the reciprocal (1/x) of the current number."""
    global current_input, first_operand, operator, waiting_for_second_operand
    try:
        num = float(current_input)
        if num == 0:
            current_input = "Error"
        else:
            result = 1 / num
            rounded_result = round(result, 12)
            if rounded_result == int(rounded_result):
                current_input = str(int(rounded_result))
            else:
                current_input = str(rounded_result)
    except ValueError:
        current_input = "Error"
    finally:
        update_display()
        first_operand = None
        operator = None
        waiting_for_second_operand = True

def factorial_func():
    """Calculates the factorial of the current number (x!)."""
    global current_input, first_operand, operator, waiting_for_second_operand
    try:
        num = int(float(current_input)) # Factorial requires a non-negative integer
        if num < 0:
            current_input = "Error" # Factorial of negative number
        else:
            result = math.factorial(num)
            current_input = str(result)
    except (ValueError, TypeError): # Catch if not convertible to int or float
        current_input = "Error"
    finally:
        update_display()
        first_operand = None
        operator = None
        waiting_for_second_operand = True

def insert_pi():
    """Inserts the value of Pi into the display."""
    global current_input, waiting_for_second_operand
    current_input = str(round(math.pi, 12)) # Insert pi, rounded for display
    waiting_for_second_operand = False # Treat as a number input
    update_display()

# --- Trigonometric Functions (Assuming Degrees for input, converting to Radians for math module) ---
def sin_func():
    """Calculates the sine of the current number (in degrees)."""
    global current_input, first_operand, operator, waiting_for_second_operand
    try:
        num_degrees = float(current_input)
        result = math.sin(math.radians(num_degrees))
        rounded_result = round(result, 12)
        if rounded_result == int(rounded_result):
            current_input = str(int(rounded_result))
        else:
            current_input = str(rounded_result)
    except ValueError:
        current_input = "Error"
    finally:
        update_display()
        first_operand = None
        operator = None
        waiting_for_second_operand = True

def cos_func():
    """Calculates the cosine of the current number (in degrees)."""
    global current_input, first_operand, operator, waiting_for_second_operand
    try:
        num_degrees = float(current_input)
        result = math.cos(math.radians(num_degrees))
        rounded_result = round(result, 12)
        if rounded_result == int(rounded_result):
            current_input = str(int(rounded_result))
        else:
            current_input = str(rounded_result)
    except ValueError:
        current_input = "Error"
    finally:
        update_display()
        first_operand = None
        operator = None
        waiting_for_second_operand = True

def tan_func():
    """Calculates the tangent of the current number (in degrees)."""
    global current_input, first_operand, operator, waiting_for_second_operand
    try:
        num_degrees = float(current_input)
        if abs(math.cos(math.radians(num_degrees))) < 1e-9: # Check for near zero cosine
            current_input = "Error" # Undefined
        else:
            result = math.tan(math.radians(num_degrees))
            rounded_result = round(result, 12)
            if rounded_result == int(rounded_result):
                current_input = str(int(rounded_result))
            else:
                current_input = str(rounded_result)
    except ValueError:
        current_input = "Error"
    finally:
        update_display()
        first_operand = None
        operator = None
        waiting_for_second_operand = True

# --- Logarithm Functions ---
def log_func(): # Base 10 logarithm
    """Calculates the base 10 logarithm of the current number."""
    global current_input, first_operand, operator, waiting_for_second_operand
    try:
        num = float(current_input)
        if num <= 0:
            current_input = "Error" # Logarithm of non-positive number
        else:
            result = math.log10(num)
            rounded_result = round(result, 12)
            if rounded_result == int(rounded_result):
                current_input = str(int(rounded_result))
            else:
                current_input = str(rounded_result)
    except ValueError:
        current_input = "Error"
    finally:
        update_display()
        first_operand = None
        operator = None
        waiting_for_second_operand = True

def ln_func(): # Natural logarithm (base e)
    """Calculates the natural logarithm (base e) of the current number."""
    global current_input, first_operand, operator, waiting_for_second_operand
    try:
        num = float(current_input)
        if num <= 0:
            current_input = "Error" # Natural logarithm of non-positive number
        else:
            result = math.log(num) # math.log() is natural logarithm
            rounded_result = round(result, 12)
            if rounded_result == int(rounded_result):
                current_input = str(int(rounded_result))
            else:
                current_input = str(rounded_result)
    except ValueError:
        current_input = "Error"
    finally:
        update_display()
        first_operand = None
        operator = None
        waiting_for_second_operand = True

# --- Memory Functions ---
def mc_func():
    """Clears the value stored in memory."""
    global memory_value, waiting_for_second_operand
    memory_value = 0
    waiting_for_second_operand = True
    update_display()

def mr_func():
    """Recalls the value stored in memory to the display."""
    global current_input, waiting_for_second_operand
    current_input = str(round(memory_value, 12)) # Recall and display, rounded
    waiting_for_second_operand = False
    update_display()

def m_plus_func():
    """Adds the current display value to the memory."""
    global memory_value, current_input, waiting_for_second_operand
    try:
        num = float(current_input)
        memory_value += num
        waiting_for_second_operand = True
    except ValueError:
        current_input = "Error"
    finally:
        update_display()

def m_minus_func():
    """Subtracts the current display value from the memory."""
    global memory_value, current_input, waiting_for_second_operand
    try:
        num = float(current_input)
        memory_value -= num
        waiting_for_second_operand = True
    except ValueError:
        current_input = "Error"
    finally:
        update_display()

def ms_func():
    """Stores the current display value into memory."""
    global memory_value, current_input, waiting_for_second_operand
    try:
        memory_value = float(current_input)
        waiting_for_second_operand = True
    except ValueError:
        current_input = "Error"
    finally:
        update_display()

# --- History Functions ---
def show_history_window():
    """Opens a new window to display the calculation history."""
    history_window = tk.Toplevel(root)
    history_window.title("Calculation History")
    history_window.geometry("300x400")
    history_window.transient(root) # Make it appear on top of the main window
    history_window.grab_set() # Make it modal (user must interact with it)
    history_window.protocol("WM_DELETE_WINDOW", history_window.destroy) # Allow closing with X button

    # Add this line to set the minimum size for the history window
    history_window.minsize(300, 200)

    # Frame for the text widget and scrollbar
    frame = ttk.Frame(history_window, padding="10")
    frame.pack(expand=True, fill="both")

    # Text widget for history display
    history_text = tk.Text(frame, wrap="word", font=("Arial", 10), bg="#ffffff", fg="#333333", state="disabled")
    history_text.pack(side="left", expand=True, fill="both")

    # Scrollbar for the text widget
    scrollbar = ttk.Scrollbar(frame, command=history_text.yview)
    scrollbar.pack(side="right", fill="y")
    history_text.config(yscrollcommand=scrollbar.set)

    # Populate history text
    history_text.config(state="normal") # Enable editing to insert text
    history_text.delete(1.0, tk.END) # Clear existing content
    for item in history_list:
        history_text.insert(tk.END, item + "\n")
    history_text.config(state="disabled") # Disable editing again

    # Clear History button
    clear_history_button = ttk.Button(history_window, text="Clear History", command=clear_history_and_update_window, style="Equals.TButton")
    clear_history_button.pack(pady=5)

    history_window.history_text_widget = history_text # Store reference to update it later

    root.wait_window(history_window) # Wait until history window is closed

def clear_history_and_update_window():
    """Clears the history list and updates the history window display."""
    
    global history_list
    history_list.clear()
    # If the history window is open, clear its text widget
    if hasattr(root.winfo_toplevel(), 'history_text_widget') and root.winfo_toplevel().history_text_widget.winfo_exists():
        root.winfo_toplevel().history_text_widget.config(state="normal")
        root.winfo_toplevel().history_text_widget.delete(1.0, tk.END)
        root.winfo_toplevel().history_text_widget.config(state="disabled")

# --- Main Tkinter Setup ---

root = tk.Tk()
root.title("Simple Calculator")
root.geometry("350x600") # Increased height for more rows
root.resizable(True, True)
root.minsize(300, 550) # Adjusted minsize
root.configure(bg="#f0f0f0") # Light gray background for the window itself

# --- Clean & Modern Light Theme Styling with Pusab Font ---
style = ttk.Style()
style.theme_use('clam') # 'clam' theme works well for custom colors and flat designs

# Configure the default style for all ttk.Button widgets (numbers, clear, +/- etc.)
style.configure('TButton',
                font=('Pusab', 16), # You might need to adjust 'Pusab' to 'Pusab Regular' or similar
                background='#ffffff', # White background for buttons
                foreground='#333333', # Dark gray text
                borderwidth=1,       # Slight border for definition
                bordercolor='#cccccc', # Light gray border
                focusthickness=0,
                relief="flat"        # Flat relief
               )

# Define how default buttons look when hovered or pressed
style.map('TButton',
          background=[('pressed', '#e0e0e0'), ('active', '#f5f5f5')], # Slightly darker when pressed, very light gray when hovered
          foreground=[('pressed', '#333333'), ('active', '#333333')]
         )

# Define a specific style for Operator buttons
style.configure('Operator.TButton',
                background='#ADD8E6', # Light Blue for operators
                foreground='#333333' # Dark gray text/icon
               )
style.map('Operator.TButton',
          background=[('pressed', '#87CEEB'), ('active', '#B0E0E6')], # Darker blue when pressed, lighter blue when hovered
          foreground=[('pressed', '#333333'), ('active', '#333333')]
         )

# Define a specific style for Scientific/Memory Function buttons
style.configure('Scientific.TButton',
                font=('Pusab', 14), # Even smaller font for scientific/memory labels
                background='#E6E6FA', # Lavender background
                foreground='#333333'
               )
style.map('Scientific.TButton',
          background=[('pressed', '#D8BFD8'), ('active', '#E0BBE4')], # Darker when pressed, slightly changed when hovered
          foreground=[('pressed', '#333333'), ('active', '#333333')]
         )

# Define a specific style for the Equals button
style.configure('Equals.TButton',
                background='#90EE90', # Light Green for equals
                foreground='#333333' # Dark gray text/icon
               )
style.map('Equals.TButton',
          background=[('pressed', '#66CDAA'), ('active', '#A2F2A2')], # Darker green when pressed, lighter green when hovered
          foreground=[('pressed', '#333333'), ('active', '#333333')]
         )

# --- Display Setup ---
display_var = tk.StringVar()
display_var.set(current_input)

display_entry = ttk.Entry(
    root,
    textvariable=display_var,
    font=("Pusab", 24), # You might need to adjust 'Pusab' here too
    justify="right",
    state="readonly",
    style="Display.TEntry"
)
# Configure the custom display entry style
style.configure("Display.TEntry",
                fieldbackground="#ffffff", # White background for display
                foreground="#333333",      # Dark gray text
                insertbackground="#333333", # Dark gray cursor
                borderwidth=1,
                bordercolor='#cccccc',
                relief="flat"
               )

display_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# --- Button Definitions and Layout ---
# New layout to accommodate History button in its own row
buttons = [
    # Row 1 (History button, spans 4 columns)
    ("History", show_history_window),
 
    # Row 2 (Memory functions)
    ("MC", mc_func), ("MR", mr_func), ("M+", m_plus_func), ("M-", m_minus_func),
    # Row 3 (More Scientific functions & MS)
    ("MS", ms_func), ("sin", sin_func), ("cos", cos_func), ("tan", tan_func),
    # Row 4 (More Scientific functions)
    ("log", log_func), ("ln", ln_func), ("π", insert_pi), ("!", factorial_func),
    # Row 5 (Power & Basic Scientific functions)
    ("x^y", lambda: operator_click("^")), ("1/x", reciprocal), ("x²", power_of_two), ("√", square_root),
    # Row 6 (Clear/Utility & Divide)
    ("%", lambda: operator_click("%")), ("AC", all_clear), ("->", backspace), ("÷", lambda: operator_click("/")),
    # Row 7 (Numbers & Multiply)
    ("7", lambda: button_click("7")), ("8", lambda: button_click("8")), ("9", lambda: button_click("9")), ("*", lambda: operator_click("*")),
    # Row 8 (Numbers & Subtract)
    ("4", lambda: button_click("4")), ("5", lambda: button_click("5")), ("6", lambda: button_click("6")), ("-", lambda: operator_click("-")),
    # Row 9 (Numbers & Add)
    ("1", lambda: button_click("1")), ("2", lambda: button_click("2")), ("3", lambda: button_click("3")), ("+", lambda: operator_click("+")),
    # Row 10 (Numbers & Equals)
    ("+/-", negate_number), ("0", lambda: button_click("0")), (".", lambda: button_click(".")), ("=", calculate_result)
]

# Configure row and column weights for responsive layout
for i in range(11): # 11 rows total (display row 0 + 10 button rows 1-10)
    root.grid_rowconfigure(i, weight=1)
for i in range(4): # 4 columns
    root.grid_columnconfigure(i, weight=1)

# Create and place the buttons using a loop, applying custom styles
row_num = 1
col_num = 0
for button_text, command_func in buttons:
    button_style = 'TButton'

    if button_text in ["/", "*", "-", "+", "%", "x^y", "÷"]:
        button_style = 'Operator.TButton'
    elif button_text in ["sin", "cos", "tan", "log", "ln", "π", "!", "1/x", "x²", "√", "MC", "MR", "M+", "M-", "MS", "History"]: # Scientific & Memory
        button_style = 'Scientific.TButton'
    elif button_text == "=":
        button_style = 'Equals.TButton'

    button_options = {
        'text': button_text,
        'command': command_func,
        'style': button_style
    }

    button = ttk.Button(root, **button_options)

    # Special handling for 'History' and '=' buttons to span columns
    if button_text == "History":
        button.grid(row=row_num, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        col_num = 4 # Force next button to new row
    elif button_text == "=":
        button.grid(row=row_num, column=col_num, columnspan=2, sticky="nsew", padx=5, pady=5)
        col_num += 2
    else:
        button.grid(row=row_num, column=col_num, sticky="nsew", padx=5, pady=5)
        col_num += 1

    if col_num >= 4:
        col_num = 0
        row_num += 1

# --- Keyboard Bindings ---
for i in range(10):
    root.bind(str(i), lambda event, num=str(i): button_click(num))
    root.bind(f"<KP_{i}>", lambda event, num=str(i): button_click(num))

root.bind(".", lambda event: button_click("."))
root.bind("<KP_Decimal>", lambda event: button_click("."))

root.bind("+", lambda event: operator_click("+"))
root.bind("-", lambda event: operator_click("-"))
root.bind("*", lambda event: operator_click("*"))
root.bind("/", lambda event: operator_click("/"))
root.bind("^", lambda event: operator_click("^"))
root.bind("<KP_Add>", lambda event: operator_click("+"))
root.bind("<KP_Subtract>", lambda event: operator_click("-"))
root.bind("<KP_Multiply>", lambda event: operator_click("*"))
root.bind("<KP_Divide>", lambda event: operator_click("/"))

root.bind("<Return>", lambda event: calculate_result())
root.bind("<KP_Enter>", lambda event: calculate_result())

root.bind("<BackSpace>", lambda event: backspace())
root.bind("c", lambda event: all_clear()) # 'c' for clear all
root.bind("C", lambda event: all_clear())
root.bind("<Escape>", lambda event: all_clear())
root.bind("<Delete>", lambda event: clear_entry()) # 'Del' for clear entry

# Initial display update
update_display()

# Start the Tkinter event loop
root.mainloop()
