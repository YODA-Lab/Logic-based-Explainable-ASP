from pysat.formula import WCNF, CNF
from pysat.examples.musx import MUSX
from pysat.examples.lbx import LBX
from collections import defaultdict


def map_explanation(explanation, vpool):
	mapped_explanation = []
	for e in explanation:
		sub_e = [vpool.obj(i) for i in e if i>0 and vpool.obj(i)]
		mapped_explanation.extend(sub_e)
	return mapped_explanation



def get_MUS(public, private, q, vpool):
	# Compute minimal unsatisfiable set
	wcnf2 = WCNF()
	if public:
		for c in public:
			wcnf2.append(c, weight=1)

	if private:
		for c in private:
			wcnf2.append(c, weight=100)


	wcnf2.extend((q.negate(topv=vpool.top).clauses))

	# wcnf2.extend(q)

	mmusx = MUSX(wcnf2, verbosity=0)
	mus = mmusx.compute()
	expl  = [list(wcnf2.soft[m - 1]) for m in mus]
	return map_explanation(expl, vpool)



def get_MCS(public, private, q, vpool):
	# Compute minimal hitting set
	wcnf = WCNF()
	if public:
		for c in public:
			wcnf.append(c, weight=1)

	if private:
		for c in private:
			wcnf.append(c, weight=100)

	# wcnf.extend(q.negate(topv=vpool.top).clauses)
	wcnf.extend(q)

	lbx = LBX(wcnf, use_cld=True, solver_name='g3')
	# Compute mcs and return the clauses indexes
	mcs = lbx.compute()
	return [list(wcnf.soft[m - 1]) for m in mcs]


