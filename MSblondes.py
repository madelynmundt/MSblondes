from pyomo.common.enums import minimize
from pyomo.environ import *
model = AbstractModel()
# sets
model.J = Set(ordered=True)
#parameters
model.d = Param(model.J)
model.cinc = Param()
model.cdec = Param()
model.cinv = Param()
model.Imax = Param()
model.Iend = Param()
model.I0 = Param()
model.P0 = Param()
# dec variables
model.I = Var(model.J, domain = NonNegativeReals)
model.P = Var(model.J, domain = NonNegativeReals)
model.INC = Var(model.J, domain = NonNegativeReals)
model.DEC = Var(model.J, domain = NonNegativeReals)
#Objective function
def obj(model):
    return sum(model.cinc*model.INC[i] + model.cdec*model.DEC[i] + model.cinv*model.I[i] for i in model.J)


model.objfn = Objective(rule = obj, sense = minimize)   

#production change
def prodchange(model, j):

    if j == model.J.first():
        return model.P[j] == model.P0 + model.INC[j] - model.DEC[j]

    prev = model.J.prev(j)

    return model.P[j] == model.P[prev] + model.INC[j] - model.DEC[j]

model.prodchange = Constraint(model.J, rule=prodchange)

#inventory balance
def invbal(model, j):

    if j == model.J.first():
        return model.I[j] == model.I0 + model.P[j] - model.d[j]

    prev = model.J.prev(j)

    return model.I[j] == model.I[prev] + model.P[j] - model.d[j]

model.invbal = Constraint(model.J, rule=invbal)

# inventory capacity
def invcap(model, j):
    return model.I[j] <= model.Imax

model.invcap = Constraint(model.J, rule=invcap)


#final inventory
def finalinv(model):
    return model.I[model.J.last()] == model.Iend


model.finalinv = Constraint(rule=finalinv)


