"""
Last Edit: 11-Feb-2024

Model Fitting
"""
import tqdm
import pandas as pd
import numpy as np
import multiprocessing as mp
import lmfit as lmf
from core.cyton2 import Cyton2Model
from core.settings import MAX_NFEV, LM_FIT_KWS, ITER_SEARCH, DT

# Model: Residual
def residual(pars, x, data=None, model=None):
	vals = pars.valuesdict()
	mUns, sUns = vals['mUns'], vals['sUns']
	mDiv0, sDiv0 = vals['mDiv0'], vals['sDiv0']
	mDD, sDD = vals['mDD'], vals['sDD']
	mDie, sDie = vals['mDie'], vals['sDie']
	b, p = vals['b'], vals['p']
	pred = model.evaluate(mUns, sUns, mDiv0, sDiv0, mDD, sDD, mDie, sDie, b, p)

	return (data - pred)

def get_parameters(pars, bounds, vary):
	params = lmf.Parameters()
	for par in pars:
		params.add(par, value=pars[par], min=bounds['lb'][par], max=bounds['ub'][par], vary=vary[par])
	paramExcl = [p for p in params if not params[p].vary]  # List of locked parameters

	return params, paramExcl

def get_model(exp_ht, n0, max_div_per_conditions, dt, nreps):
    return Cyton2Model(exp_ht[0], n0, max_div_per_conditions[0], dt, nreps)

def get_times(exp_ht):
    t0 = 0
    tf = max(exp_ht[0]) + 5
    return np.linspace(t0, tf, num=int(tf/DT)+1)

# Initial Model Extrapolation
def extrapolate(model, times, pars):
	ext = model.extrapolate(times, pars)  # model extrapolation
	ext_total_live_cells = ext['ext']['total_live_cells']  # total number of cells (sum over all genrations)
	ext_cells_per_gen    = ext['ext']['cells_gen']        # number of cells in each generation as a function of time
	hts_total_live_cells = ext['hts']['total_live_cells']  # total number of cells at specified harvested time points
	hts_cells_per_gen    = ext['hts']['cells_gen']       # number of cells in each generation at each harvested time points

	return ext_total_live_cells, ext_cells_per_gen, hts_total_live_cells, hts_cells_per_gen

# Fitting Process
def fit(exp_ht, cell_gens_reps, params, paramExcl, model) :

    x_gens = np.array(exp_ht[0])
    y_cells = np.array(cell_gens_reps[0]).flatten()

    rng = np.random.RandomState(seed=894375982)
    candidates = {'result': [], 'residual': []}
    for _ in tqdm.trange(ITER_SEARCH, leave=False, position=2*0+1):
        # Random initial guesses
        for par in params:
            if par in paramExcl: pass  # Ignore locked parameters
            else:
                par_min, par_max = params[par].min, params[par].max
                params[par].set(value=rng.uniform(low=par_min, high=par_max))

        try:
            mini = lmf.Minimizer(residual, params, fcn_args=(x_gens, y_cells, model), **LM_FIT_KWS)
            res = mini.minimize(method='leastsq', max_nfev=MAX_NFEV)

            candidates['result'].append(res)
            candidates['residual'].append(res.chisqr)
        except ValueError as ve:
            pass

    fit_results = pd.DataFrame(candidates)
    fit_results.sort_values('residual', ascending=True, inplace=True)  # Find lowest RSS

    best_fit = fit_results.iloc[0]['result'].params.valuesdict()
    mUns, sUns = best_fit['mUns'], best_fit['sUns']
    mDiv0, sDiv0 = best_fit['mDiv0'], best_fit['sDiv0']
    mDD, sDD = best_fit['mDD'], best_fit['sDD']
    mDie, sDie = best_fit['mDie'], best_fit['sDie']
    b, p = best_fit['b'], best_fit['p']

    return mUns, sUns, mDiv0, sDiv0, mDD, sDD, mDie, sDie, b, p