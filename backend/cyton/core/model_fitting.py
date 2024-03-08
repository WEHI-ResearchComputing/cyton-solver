"""
Last Edit: 11-Feb-2024

Model Fitting
"""
from typing import cast
import tqdm
import pandas as pd
import numpy as np
import lmfit as lmf
from cyton.core.cyton2 import Cyton2Model
from cyton.core.settings import MAX_NFEV, LM_FIT_KWS, ITER_SEARCH
from cyton.core.types import *
from numpy.typing import NDArray
from cyton.core.utils import flatten

# Model: Residual
def residual(pars: lmf.Parameters, x: NDArray, data: NDArray, model: Cyton2Model) -> NDArray[np.float_]:
	vals: Parameters = cast(Parameters, pars.valuesdict())
	pred = model.evaluate(vals)
	return data - pred

# Fitting Process
def fit(exp_ht: PerTime[HarvestTime], cell_gens_reps: PerTime[PerRep[PerGen[CellCount]]], params: lmf.Parameters, paramExcl: ExcludedParameters, model: Cyton2Model) -> Parameters:

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
