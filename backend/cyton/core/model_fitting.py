"""
Last Edit: 11-Feb-2024

Model Fitting
"""
from typing import cast
import tqdm
import pandas as pd
import numpy as np
import lmfit as lmf
from core.cyton2 import Cyton2Model
from core.settings import MAX_NFEV, LM_FIT_KWS, ITER_SEARCH, DT
from cyton.core import types
from numpy.typing import NDArray
from core.utils import flatten

# Model: Residual
def residual(pars: lmf.Parameters, x: NDArray, data: NDArray, model: Cyton2Model) -> NDArray[np.float_]:
	vals: types.Parameters = cast(types.Parameters, pars.valuesdict())
	pred = model.evaluate(vals)
	return data - pred

def get_parameters(pars: types.Parameters, bounds: types.Bounds, vary: types.FittableParams) -> tuple[lmf.Parameters, types.ExcludedParameters]:
	params = lmf.Parameters()
	for par in pars:
		params.add(par, value=pars[par], min=bounds['lb'][par], max=bounds['ub'][par], vary=vary[par])
	paramExcl = [p for p in params if not params[p].vary]  # List of locked parameters

	return params, paramExcl

def calc_n0(cell_gens_reps: types.CellPerGensReps) -> float:
    """
    Calculates N0, the initial number of cells.
    This is taken to be the average cell numbers at 0th time point.
    """
    return np.mean([sum(flatten(rep)) for rep in cell_gens_reps[0]])

def get_times(exp_ht: types.HarvestTimes) -> types.ExtrapolationTimes:
    t0 = 0
    tf = max(exp_ht) + 5
    return np.linspace(t0, tf, num=int(tf/DT)+1)

# Initial Model Extrapolation
def extrapolate(model: Cyton2Model, times: types.ExtrapolationTimes, pars: types.Parameters) -> types.ExtrapolatedData:
    ext = model.extrapolate(times, pars)  # model extrapolation

    return {
        "ext_total_live_cells": ext['ext']['total_live_cells'],  # total number of cells (sum over all genrations)
        "ext_cells_per_gen": ext['ext']['cells_gen'],        # number of cells in each generation as a function of time
        "hts_total_live_cells": ext['hts']['total_live_cells'],  # total number of cells at specified harvested time points
        "hts_cells_per_gen": ext['hts']['cells_gen']       # number of cells in each generation at each harvested time points
    }

# Fitting Process
def fit(exp_ht: types.HarvestTimes, cell_gens_reps: types.CellPerGensReps, params: lmf.Parameters, paramExcl: types.ExcludedParameters, model: Cyton2Model) -> types.Parameters:

    x_gens = np.array(exp_ht[0])
    y_cells = np.fromiter(flatten(cell_gens_reps[0]), dtype=float)

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
        except ValueError:
            pass

    fit_results = pd.DataFrame(candidates)
    fit_results.sort_values('residual', ascending=True, inplace=True)  # Find lowest RSS

    best_fit = fit_results.iloc[0]['result'].params.valuesdict()

    return best_fit
