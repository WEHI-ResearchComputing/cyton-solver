
# =====================
# Extrapolation Default Settings
# ========
# =============

DEFAULT_EXP_HT = [0, 12, 24, 36, 48, 72, 96, 120, 144]

DEFAULT_CELL_GENS_REPS = 10

DEFAULT_MAX_DIV_PER_CONDITIONS = 10

# =====================
# Model Parameter Settings
# =====================


DEFAULT_PARS = {
		'mUns': 100_000, 'sUns': 1E-10,  # Unstimulated death time
		'mDiv0': 30, 'sDiv0': 0.2,     # Time to first division
		'mDD': 60, 'sDD': 0.3,         # Time to division destiny
		'mDie': 80, 'sDie': 0.2,       # Time to death
		'b': 10, 'p': 1                # Subsequent division time & Proportion of activated cells
	}

DEFAULT_BOUNDS = {
		'lb': {  # Lower bounds
			'mUns': 1E-2, 'sUns': 1E-2,
			'mDiv0': 1E-2, 'sDiv0': 1E-2,
			'mDD': 1E-2, 'sDD': 1E-2,
			'mDie': 1E-2, 'sDie': 1E-2,
			'b': 0, 'p': 0
		},
		'ub': {  # Upper bounds
			'mUns': 100_000, 'sUns': 2,
			'mDiv0': 500, 'sDiv0': 2,
			'mDD': 500, 'sDD': 2,
			'mDie': 500, 'sDie': 2,
			'b': 50, 'p': 1
		}
	}

DEFAULT_VARY = {  # True = Subject to change; False = Lock parameter
		'mUns': False, 'sUns': False,  # This is Cyton1.5 specific parameters. In Cyton2, this is not used!
		'mDiv0': True, 'sDiv0': True,
		'mDD': True, 'sDD': True,
		'mDie': True, 'sDie': True,
		'b': True, 'p': False
	}


# =====================
# Model Fitting Settings
# =====================

N0 = 10000			  # Initial number of cells
DT = 0.5              # [Cyton Model] Time step

ITER_SEARCH = 1		  # [Cyton Model] Number of initial search (100 is usually a good guess)

MAX_NFEV = None 	  # [LMFIT] Maximum number of function evaluation

LM_FIT_KWS = {        # [LMFIT/SciPy] Key-word arguements pass to LMFIT minimizer for Levenberg-Marquardt algorithm
    # 'ftol': 1E-10,  # Relative error desired in the sum of squares. DEFAULT: 1.49012E-8
    # 'xtol': 1E-10,  # Relative error desired in the approximate solution. DEFAULT: 1.49012E-8
    # 'gtol': 0.0,    # Orthogonality desired between the function vector and the columns of the Jacobian. DEFAULT: 0.0
    'epsfcn': 1E-4    # A variable used in determining a suitable step length for the forward-difference approximation of the Jacobian (for Dfun=None). Normally the actual step length will be sqrt(epsfcn)*x If epsfcn is less than the machine precision, it is assumed that the relative errors are of the order of the machine precision. Default value is around 2E-16. As it turns out, the optimisation routine starts by making a very small move (functinal evaluation) and calculating the finite-difference Jacobian matrix to determine the direction to move. The default value is too small to detect sensitivity of 'm' parameter.
}