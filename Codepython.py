from pyomo.environ import *

model = ConcreteModel()

# Sets
model.j = Set(initialize=['v1', 'v2', 'v3', 'v4', 'v5', 'v6'])
model.i = Set(initialize=['1', '2', '3'])
model.jp = model.j

# Parameters
model.a = Param(model.j, initialize={'v1': 0, 'v2': 0, 'v3': 0, 'v4': 0, 'v5': 0, 'v6': 0})
model.w = Param(model.j, initialize={'v1': 4, 'v2': 1, 'v3': 4, 'v4': 4, 'v5': 8, 'v6': 2})
model.p = Param(model.j, initialize={'v1': 6, 'v2': 9, 'v3': 7, 'v4': 6, 'v5': 8, 'v6': 13})
model.M = Param(initialize=9999)
model.H = Param(model.j, initialize={'v1': 1, 'v2': 2, 'v3': 2, 'v4': 3, 'v5': 2, 'v6': 1})
model.L = Param(model.j, initialize={'v1': 1, 'v2': 3, 'v3': 3, 'v4': 3, 'v5': 3, 'v6': 1})
model.T = Param(initialize=12)

# Variables
model.z = Var()
model.x = Var(model.i, model.j, within=Binary)
model.II = Var(model.i, model.j, model.jp, within=Binary)
model.s = Var(model.j, within=NonNegativeReals)

# Objective function
def obj_rule(model):
    return sum(model.w[j] * (model.s[j] + model.p[j] - model.a[j]) for j in model.j)
model.obj = Objective(rule=obj_rule)

# Constraints
def eq1_rule(model, j):
    return sum(model.x[i,j] for i in model.i) == 1
model.eq1 = Constraint(model.j, rule=eq1_rule)

def eq2_rule(model, j):
    return model.s[j] == model.a[j]
model.eq2 = Constraint(model.j, rule=eq2_rule)

def eq3_rule(model, i, j, jp):
    if j != jp:
        return model.s[jp] == model.s[j] + model.p[j] - model.M * (1 - model.II[i,j,jp])
    return Constraint.Skip
model.eq3 = Constraint(model.i, model.j, model.jp, rule=eq3_rule)

# Add the rest of the constraints here

# Solve the model
solver = SolverFactory('cplex')
results = solver.solve(model)

# Display the results
print("Objective value:", value(model.z))
for i in model.i:
    for j in model.j:
        print(f"x[{i},{j}] =", value(model.x[i,j]))
for i in model.i:
    for j in model.j:
        for jp in model.jp:
            print(f"II[{i},{j},{jp}] =", value(model.II[i,j,jp]))
for j in model.j:
    print(f"s[{j}] =", value(model.s[j]))
