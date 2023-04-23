#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def team_builder(df, budget, num_gk, num_def, num_mid, num_for):
    indices = players.full_name
    perf = dict(zip(indices,players.performance))
    salary = dict(zip(indices,players.performance))
    player_position = list(zip(players.full_name,players.position))

    # Create the model
    m = Model()

    # Create the decision variables
    x = m.addVars(players.full_name, vtype=GRB.BINARY, name="x")

    # Set the objective function
    m.setObjective(quicksum(perf[i]*x[i] for i in indices), GRB.MAXIMIZE)

    # Add the constraints
    m.addConstr(quicksum(salary[i]*x[i] for i in indices) <= budget, name='salary')

    m.addConstr(quicksum([x[i] for i, position in player_position if position=='Goalkeeper'])== num_gk)
    m.addConstr(quicksum([x[i] for i, position in player_position if position=='Goalkeeper'])<= 1)
    

    m.addConstr(quicksum([x[i] for i, position in player_position if position=='Defender'])== num_def)
    m.addConstr(quicksum([x[i] for i, position in player_position if position=='Defender'])<=5)

    m.addConstr(quicksum([x[i] for i, position in player_position if position=='Midfielder']) == num_mid)
    m.addConstr(quicksum([x[i] for i, position in player_position if position=='Midfielder'])<=5)

    m.addConstr(quicksum([x[i] for i, position in player_position if position=='Forward']) == num_for)
    m.addConstr(quicksum([x[i] for i, position in player_position if position=='Forward'])<=3)

    m.addConstr(quicksum(x[i] for i in indices)<=11)

    # Solve the model
    m.optimize()
    
    r = pd.DataFrame()

    for v in m.getVars():
        if v.x > 1e-6:
            r = r.append(players.iloc[v.index][['full_name','position', 'salary']])

    col = {'full_name':[],'position':[],'salary':[]} 
    team_stats = pd.DataFrame(col)

    for i in r['full_name']:
        x = players[players['full_name']==i]
        x = x[['full_name','position','salary']] #add cols
        team_stats= team_stats.append(x)
    return team_stats

