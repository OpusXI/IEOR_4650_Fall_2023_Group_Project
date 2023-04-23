import tkinter as tk
from tkinter import ttk
import pandas as pd

from clustering_analysis import positions_clustering
from clustering_analysis import curr_players
from clustering_analysis import zipSalaryData

from Optimization import team_builder

def format_dataframe(df):
    positions = ['Forward', 'Midfielder', 'Defender', 'Goalkeeper']
    output_str = ""
    total_cost = 0

    for position in positions:
        output_str += f"{position.upper()}S\n"
        output_str += "--------------------------------\n"

        position_df = df[df['position'] == position]

        for index, row in position_df.iterrows():
            name = row['full_name']
            salary = row['salary']
            output_str += f"{name} ({salary})\n"
            total_cost += salary

        output_str += "--------------------------------\n"

    output_str += f"TOTAL COST: {total_cost}"
    return output_str


def calculate():
    ### GET INPUT WEIGHTS FROM GUI ###
    weights = []
    numClusters = 6
    
    for i in range(4):
        tab_weights = [float(manual_entry_vars[i][j].get()) for j in range(len(manual_entry_vars[i]))]
        weights.append(tab_weights)
    
    weightsGK = weights[0]
    weightsDef = weights[1]
    weightsMid = weights[2]
    weightsFwd = weights[3]
    
    ### GET BUDGET CONSTRAINT ###
    budget = int(budget_var.get())
    salaryDataframe = pd.read_csv("./data/salaries/scrapedSalariesFINAL.csv")
    
    ### GET POSITION CONSTRAINTS ###
    num_players = [var.get() for var in dropdown_vars]
    numGK = num_players[0]
    numDef = num_players[1]
    numMid = num_players[2]
    numFwd = num_players[3]
    
    ### SET FEATURES AND CLUSTER-RANK ###
    outfield_selected_features = ['full_name', 'position','shot_conversion_rate_overall',
                      'shots_on_target_total_overall', 
                      'passes_completed_total_overall', 'shots_total_overall',
                      'duels_total_overall', 'min_per_card_overall',
                      'assists_away']
    
    goalkeeper_selected_features = ['full_name', 'position',"saves_per_game_overall",
                                "passes_completed_total_overall", 
                                "save_percentage_overall"]
    
    forwardRankingFrame = positions_clustering(curr_players, 'Forward', weightsFwd, numClusters, outfield_selected_features,output=False)
    forwardRankingFrameInput = zipSalaryData(forwardRankingFrame, salaryDataframe)
    
    midfielderRankingFrame = positions_clustering(curr_players, 'Midfielder', weightsMid, numClusters, outfield_selected_features, output=False)
    midfielderRankingFrameInput = zipSalaryData(midfielderRankingFrame, salaryDataframe)
    
    defenderRankingFrame = positions_clustering(curr_players, 'Defender', weightsDef, numClusters, outfield_selected_features, output=False)
    defenderRankingFrameInput = zipSalaryData(defenderRankingFrame, salaryDataframe)
    
    goalkeeperRankingFrame = positions_clustering(curr_players, 'Goalkeeper', weightsGK, numClusters, goalkeeper_selected_features, output=False)
    goalkeeperRankingFrameInput = zipSalaryData(goalkeeperRankingFrame, salaryDataframe)
    
    totalFrame = pd.concat([forwardRankingFrameInput, midfielderRankingFrameInput, defenderRankingFrameInput, goalkeeperRankingFrameInput])
    
    ### TEAM BUILDING FUNCTION CALL HERE###
    teamDataframe = team_builder(totalFrame, budget, numGK, numDef, numMid, numFwd)
    print(teamDataframe)

    ### OUTPUT TO GUI ###
    if type(teamDataframe) == str:
        outString = teamDataframe
    else:
        outString = format_dataframe(teamDataframe)
    
    output_text = f"{outString}"
    output_box.config(state="normal")
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, output_text)
    output_box.config(state="disabled")


def update_total_players(*args):
    total_players = sum([var.get() for var in dropdown_vars])
    total_players_label.config(text=f"Total players: {total_players}")
    if total_players < 11:
        total_players_label.config(fg="red")
    else:
        total_players_label.config(fg="green")

def manual_entry_update(i, j):
    def inner_function(*args):
        try:
            value = float(manual_entry_vars[i][j].get())
            manual_entry_vars[i][j].set("{:.2f}".format(value))
        except ValueError:
            manual_entry_vars[i][j].set("0.00")
        update_sum_label(i)
    return inner_function

def update_sum_label(i):
    current_sum = sum(float(manual_entry_vars[i][j].get()) for j in range(len(manual_entry_vars[i])))
    sum_labels[i].config(text=f"Sum: {current_sum:.2f}")

root = tk.Tk()
root.title("FutMoneybol")
root.geometry("730x500")
root.resizable(False, False)

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

container_frame = tk.Frame(root)
container_frame.pack(pady=20)

slider_notebook = ttk.Notebook(container_frame)
slider_notebook.pack(side=tk.LEFT, padx=10)

tab_labels = ['GK', 'DEF', 'MID', 'FWD']
slider_labels = [
    ["Saves/Game", "Passes Completed", "Save %"],
    ["Shot Conv. Rate", "Shots on Target", "Passes Completed", "Shot Total", "Duels Total", "Mins per Card", "Assists"],
    ["Shot Conv. Rate", "Shots on Target", "Passes Completed", "Shot Total", "Duels Total", "Mins per Card", "Assists"],
    ["Shot Conv. Rate", "Shots on Target", "Passes Completed", "Shot Total", "Duels Total", "Mins per Card", "Assists"]
]

manual_entry_vars = []
sum_labels = []

# Default values for each tab
default_values = [
    ["0.80", "0.10", "0.10"],
    ["0.30", "0.10", "0.20", "0.10", "0.10", "0.10", "0.10"],
    ["0.15", "0.15", "0.15", "0.15", "0.20", "0.10", "0.10"],
    ["0.40", "0.20", "0.20", "0.10", "0.05", "0.03", "0.02"]
]

for i in range(4):
    tab_frame = tk.Frame(slider_notebook)
    slider_notebook.add(tab_frame, text=tab_labels[i])

    tab_manual_entries = []
    for j in range(len(slider_labels[i])):
        slider_label = tk.Label(tab_frame, text=slider_labels[i][j])
        slider_label.grid(row=j, column=0, padx=10, pady=5)

        manual_entry_var = tk.StringVar()
        manual_entry_var.set(default_values[i][j])  # Set the default value
        manual_entry = tk.Entry(tab_frame, textvariable=manual_entry_var, width=6)
        manual_entry.grid(row=j, column=1, padx=10, pady=5)
        tab_manual_entries.append(manual_entry_var)

        enter_button = tk.Button(tab_frame, text="Enter", command=manual_entry_update(i, j))
        enter_button.grid(row=j, column=2, padx=10, pady=5)

    sum_label = tk.Label(tab_frame, text=f"Sum: {sum([float(val) for val in default_values[i]]):.2f}")
    sum_label.grid(row=8, column=0, columnspan=3, pady=10)
    sum_labels.append(sum_label)

    manual_entry_vars.append(tab_manual_entries)

# Create the output box to display the optimized team
output_title_label = tk.Label(container_frame, text="Optimized Team Output", font=("Helvetica", 14))
output_title_label.pack(side=tk.TOP, pady=(10, 5))

output_box = tk.Text(container_frame, wrap=tk.WORD, height=4*5, width=40, state="disabled")
output_box.pack(side=tk.LEFT, padx=10, pady=(0, 10))

budget_frame = tk.Frame(root)
budget_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)

budget_label = tk.Label(budget_frame, text="Budget (£):")
budget_label.pack(side=tk.LEFT, padx=10)

budget_var = tk.StringVar()
budget_var.set("100000000")
budget_entry = tk.Entry(budget_frame, textvariable=budget_var, width=10)
budget_entry.pack(side=tk.LEFT, padx=10)

calculate_button = tk.Button(budget_frame, text="Calculate", command=calculate)
calculate_button.pack(side=tk.LEFT, padx=10)

total_players_label = tk.Label(budget_frame, text="Total players: 0")
total_players_label.config(fg="red")
total_players_label.pack(side=tk.RIGHT, padx=10)

root.mainloop()
