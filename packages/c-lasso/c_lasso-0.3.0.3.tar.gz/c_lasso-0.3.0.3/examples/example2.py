path = '/Users/lsimpson/Desktop/GitHub/c-lasso/joss-paper/figures/'
from classo import *
m,d,d_nonzero,k,sigma =100,100,5,1,0.5
(X,C,y),sol = random_data(m,d,d_nonzero,k,sigma,zerosum=True, seed = 4 )

problem  = classo_problem(X,y,C)


problem.formulation.huber  = True
problem.formulation.concomitant = False
problem.formulation.rho = 1.5

problem.model_selection.LAMfixed = True
problem.model_selection.LAMfixedparameters.numerical_method = 'DR'

problem.model_selection.StabSel = True
problem.model_selection.StabSelparameters.method = 'first'
problem.model_selection.StabSelparameters.q = 15


problem.model_selection.LAMfixedparameters.threshold = 0.1


problem.solve()

print(" \n Here is the problem instance plot : \n ")
print(problem)

problem.solution.StabSel.save1 = path+'StabSel'
problem.solution.StabSel.save2 = path+'StabSel-path'
problem.solution.StabSel.save3 = path+'StabSel-beta'
#problem.solution.CV.save = path+'CV-beta'
problem.solution.LAMfixed.save = path+'LAM-beta'
#problem.solution.PATH.save = path+'PATH'


print(" \n Here is the solution instance plot : \n ")
print(problem.solution)


#problem.solution.CV.graphic(mse_max = 1.,save=path+'CV-graph')