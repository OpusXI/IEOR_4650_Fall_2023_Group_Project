import tkinter as tk
from tkinter import ttk

# Function to handle the "Calculate" button click
def calculate():
    # Implement the logic for calculating the optimized team
    # using the selected constraints
    output_text = "Optimized team will be shown here."
    output_box.config(state="normal")
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, output_text)
    output_box.config(state="disabled")

def simulate():
    # Implement the logic for simulating the team performance
    # using the selected option from the dropdown
    simulation_value = "Simulation value will be shown here."
    simulation_result.config(text=simulation_value)

def update_total_players(*args):
    total_players = sum([var.get() for var in dropdown_vars])
    total_players_label.config(text=f"Total players: {total_players}")
    if total_players > 11:
        total_players_label.config(fg="red")
    else:
        total_players_label.config(fg="black")

# Create the main application window
root = tk.Tk()
root.title("FutMoneybol")
root.geometry("730x450")

# Create the top row with 4 dropdown menus for selecting number of players
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

positions = ["Goalkeepers", "Defenders", "Midfielders", "Attackers"]
dropdown_vars = []

for position in positions:
    label = tk.Label(top_frame, text=position)
    label.pack(side=tk.LEFT, padx=10)
    
    var = tk.IntVar()
    var.trace("w", update_total_players)
    dropdown = ttk.Combobox(top_frame, textvariable=var, values=list(range(12)), width=5)
    dropdown.pack(side=tk.LEFT, padx=10)
    dropdown_vars.append(var)

# Create the budget input field and the "Calculate" button
budget_frame = tk.Frame(root)
budget_frame.pack(pady=10, fill=tk.X)

budget_label = tk.Label(budget_frame, text="Budget:")
budget_label.pack(side=tk.LEFT, padx=10)

budget_var = tk.StringVar()
budget_entry = tk.Entry(budget_frame, textvariable=budget_var, width=10)
budget_entry.pack(side=tk.LEFT, padx=10)

calculate_button = tk.Button(budget_frame, text="Calculate", command=calculate)
calculate_button.pack(side=tk.LEFT, padx=10)

total_players_label = tk.Label(budget_frame, text="Total players: 0")
total_players_label.pack(side=tk.RIGHT, padx=10)


# Create a container frame for the sliders and output box
container_frame = tk.Frame(root)
container_frame.pack(pady=20)

# Create the sliders for future constraints
slider_frame = tk.Frame(container_frame)
slider_frame.pack(side=tk.LEFT, padx=10)

sliders = []
for i in range(4):
    slider = tk.Scale(slider_frame, from_=0, to=100, orient=tk.HORIZONTAL)
    slider.pack(pady=5)
    sliders.append(slider)

# Create the output box to display the optimized team
output_box = tk.Text(container_frame, wrap=tk.WORD, height=4*5, width=40, state="disabled")
output_box.pack(side=tk.LEFT, padx=10)

# Create the simulation row with the "Simulate" button, a dropdown box, and a label to display the final simulation value
simulation_frame = tk.Frame(root)
simulation_frame.pack(side=tk.BOTTOM, pady=10)

simulate_button = tk.Button(simulation_frame, text="Simulate", command=simulate)
simulate_button.pack(side=tk.LEFT, padx=10)

simulation_options = ["Goals", "Season Points", "League Standing"]
simulation_var = tk.StringVar()
simulation_dropdown = ttk.Combobox(simulation_frame, textvariable=simulation_var, values=simulation_options, width=10)
simulation_dropdown.pack(side=tk.LEFT, padx=10)

simulation_result = tk.Label(simulation_frame, text="")
simulation_result.pack(side=tk.LEFT, padx=10)

root.mainloop()
