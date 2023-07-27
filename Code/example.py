import copy
from utils import *
from pysat.formula import CNF
from generate_ASP import create_ESAP





'''Generate knowledge bases'''

a = 4 # agents	
r = 3 # resources
t = 3 # time (days)
k = 2 # shifts per agent
n = 1 # agents per shift


KB, C_A, vpool = create_ESAP(a, r, t, k, n)


'''Define which agent is the explainee and which are the other agents'''
explainee = str(3)
other_agents = copy.deepcopy(C_A)
other_agents.pop(explainee)
public_agents = []
public_agents.append(explainee)

'''Define query'''
reason_seeking_query = CNF(from_clauses=C_A[explainee][0])

'''Access rights percentage and publc/private clauses'''
access_rights_perc = 0.4
public_clauses = []
private_clauses = []
public_clauses.extend(KB.hard)
public_clauses.extend(C_A[explainee][0])



while len(public_agents) < round(access_rights_perc*len(C_A)):
	o = other_agents.popitem()[0]
	if o not in public_agents:
		public_agents.append(o)

for c in C_A:
	if c in public_agents:
		public_clauses.extend(C_A[c][0])
	else:
		private_clauses.extend(C_A[c][0])


'''Generate explanation for reason seeking query'''
reason_seeking_explanation = get_MUS(public_clauses, private_clauses, reason_seeking_query, vpool)
print(reason_seeking_explanation)






