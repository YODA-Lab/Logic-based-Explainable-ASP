
from random import randint
from pysat.formula import WCNF, IDPool
from pysat.solvers import Solver
from pysat.examples.rc2 import RC2
from pysat.examples.optux import OptUx
from pysat.examples.lbx import LBX
from pysat.card import *
from collections import defaultdict




def create_ESAP(a, r, t, k, n):

	""" 
Create an instance of the Employee Scheduling and Assignment Problem as a Weighted MaxSAT problem. (The constraints are hard-coded.)

:param a: number of agents
:param r: number of resources
:param d: number of time slots
:param k: number of shifts per agent
:param n: number of agents per shift

:return: a WCNF object representing the instance of the problem with all constraints (KB), 
		 a dictionary of the agent consraints (C_A)
		 a pool of variable ids (vpool) 
	"""

	A = range(1, a + 1)
	R = range(1, r + 1)
	T = range(1, t + 1)

	# Create decision variable:
	# initializing the pool of variable ids
	vpool = IDPool(start_from=1)
	x = lambda i, r, t: vpool.id('x{0}_{1}_{2}'.format(i, r, t))

	KB = WCNF()

	'''Domain Constraints'''

	# 1) An agent can't be assigned a morning shift if they were assigned an evening shift the previous day:
	for i in A:
		KB.extend([[-x(i,3,1), -x(i,1,2)], [-x(i,3,2), -x(i,1,3)], [-x(i,3,3), -x(i,1,4)], [-x(i,3,4), -x(i,1,5)] ])

	# 2) All agents must be assigned a shift k times:
	constraint2_lists = dict()
	for i in A:
		constraint2_lists[str(i)] = []

	for i in A:
		for r in R:
			for t in T:
				constraint2_lists[str(i)].append(x(i,r,t))

	for c in constraint2_lists:
		KB.extend(CardEnc.equals(lits=constraint2_lists[c], bound=k, vpool=vpool).clauses)

	# 3) At most one shift per agent on a single day

	for i in A:
		for t in T:
			KB.extend(CardEnc.atmost(lits=[x(i, 1, t), x(i, 2, t), x(i, 3, t)], bound=1, encoding=EncType.pairwise, vpool=vpool).clauses)


	# 4) A shift can only be assigned to at most n agents
	for r in R:
		for t in T:
			c = [x(i, r, t) for i in A]
			KB.extend(CardEnc.atmost(lits=c, bound=n, encoding=EncType.seqcounter, vpool=vpool).clauses)


	'''Agent Constraints'''

	C_A = defaultdict(list)

	# 1) 1/5 of the agents want to take only shift 1 on any day:
	for i in A[0:len(A)//5]:
		a = [x(i, 1, t) for t in T]
		c = CardEnc.atleast(a, bound=1,  vpool=vpool).clauses
		w = randint(10, 100)  # Pick a random number between 1 and 100 for the weight
		KB.extend(c, weights=[w for e in range(len(c))])
		C_A[str(i)].append(c)


	# 2) 1/5 of the agents want to take only shift 2 on any day:
	for i in A[(len(A)//5):2*len(A)//5]:

		a = [x(i, 2, t) for t in T]
		c = CardEnc.atleast(a, bound=1, vpool=vpool).clauses
		w = randint(10, 100)  # Pick a random number between 1 and 100 for the weight
		KB.extend(c, weights=[w for l in range(len(c))])
		C_A[str(i)].append(c)


	# 3) 1/5 of the agents want to take only shift 3 on any day:
	for i in A[(2*len(A)//5):3*len(A)//5]:
		a = [x(i, 3, t) for t in T]
		c = CardEnc.atleast(a, bound=1, vpool=vpool).clauses
		w = randint(10, 100)  # Pick a random number between 1 and 100 for the weight
		KB.extend(c, weights=[w for e in range(len(c))])
		C_A[str(i)].append(c)

	# 4) 1/5 of the agents want to take shift 3 on days 2 and 5:
	for i in A[(3*len(A)//5):4*len(A)//5]:

		c = [[x(i, 3, 2)], [x(i, 3, 5)]]
		w = randint(10, 100)  # Pick a random number between 1 and 100 for the weight
		KB.extend(c, weights=[w for e in range(len(c))])
		C_A[str(i)].append(c)

	# 5) 1/5 of the agents want to take shift 3 on days 1 and 5 and not shift 1 and 2 on day 5:
	for i in A[(4 * len(A) // 5):len(A)]:
		c = [[x(i, 3, 1)], [x(i, 3, 5)], [-x(i, 1, 5)], [-x(i, 2, 5)]]
		w = randint(10, 100)  # Pick a random number between 1 and 100 for the weight
		KB.extend(c, weights=[w for e in range(len(c))])
		C_A[str(i)].append(c)


	return KB, C_A, vpool



'''Generate Schedule'''

def generate_schedule(KB, vpool):
	schedule = []
	schedule_false = []
	m = RC2(KB)
	# total_weight = sum(m.wght.values())
	model = m.compute()
	# cost = total_weight - m.cost
	# print("---------------")
	# print("---------------")
	if model:
		for i in model:
			if i>0 and vpool.obj(i):
				schedule.append(vpool.obj(i))
				schedule_false.append(i)
	return schedule, schedule_false, model






def main():
	KB, C_A, vpool = create_ESAP(4, 3, 3, 2, 1)
	schedule, schedule_false, model = generate_schedule(KB, vpool)
	print(schedule)


if __name__ == '__main__':
	main()
