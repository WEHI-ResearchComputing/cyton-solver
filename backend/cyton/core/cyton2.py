"""
Last Edit: 11-Feb-2024

Cyton2 Algorithm Model
"""
import numpy as np
from scipy.stats import lognorm, norm
from cyton.core import types

DTYPE = np.float64

class Cyton2Model:
  t0: float
  tf: float
  dt: float
  times: types.ExtrapolationTimes
  nt: int
  n0: int
  ht: types.HarvestTimes
  nreps: types.NReps
  exp_max_div: types.MaxGeneration
  max_div: types.MaxGeneration
  logn: bool

  def __init__(self, ht: types.HarvestTimes, n0: int, max_div: types.MaxGeneration, dt: float, nreps: types.NReps = [], logn: bool = True):

    self.t0 = 0.0
    self.tf = max(ht) + dt
    self.dt = dt  									  # Time increment

    # Declare time array
    self.times = np.arange(self.t0, self.tf, dt, dtype=DTYPE)
    self.nt = self.times.size

    self.n0 = n0  										# experiment initial cell number
    self.ht = ht  										# experiment harvested times
    self.nreps = nreps  							# experiment number of replicates

    self.exp_max_div = max_div  			# observed maximum division number
    self.max_div = 10  							  # theoretical maximum division number
    self.logn = logn

  def compute_pdf(self, times: types.ExtrapolationTimes, mu: float, sig: float):
    if self.logn:
      return lognorm.pdf(times, sig, scale=mu)
    else:
      return norm.pdf(times, mu, sig)

  def compute_cdf(self, times: types.ExtrapolationTimes, mu: float, sig: float):
    if self.logn:
      return lognorm.cdf(times, sig, scale=mu)
    else:
      return norm.cdf(times, mu, sig)

  def compute_sf(self, times: types.ExtrapolationTimes, mu: float, sig: float):
    if self.logn:
      return lognorm.sf(times, sig, scale=mu)
    else:
      return norm.sf(times, mu, sig)

  def _storage(self):
    pdfDD = np.zeros(shape=self.nt, dtype=DTYPE)

    sfUns = np.zeros(shape=self.nt, dtype=DTYPE)
    sfDiv = np.zeros(shape=self.nt, dtype=DTYPE)
    sfDie = np.zeros(shape=self.nt, dtype=DTYPE)
    sfDD = np.zeros(shape=self.nt, dtype=DTYPE)

    # Declare 3 arrays for unstimulated cells, divided cells & destiny cells
    nUNS = np.zeros(shape=self.nt, dtype=DTYPE)
    nDIV = np.zeros(shape=(self.max_div+1, self.nt), dtype=DTYPE)
    nDES = np.zeros(shape=(self.max_div+1, self.nt), dtype=DTYPE)

    # Store number of live cells at all time per generations
    cells_gen = np.zeros(shape=(self.exp_max_div+1, self.nt), dtype=DTYPE)

    return pdfDD, sfUns, sfDiv, sfDie, sfDD, nUNS, nDIV, nDES, cells_gen

  # Return sum of dividing and destiny cells in each generation
  def evaluate(self, params: types.Parameters):         # subsequent division time, activation probability
    times = self.times

    # Create empty arrays
    pdfDD, sfUns, sfDiv, sfDie, sfDD, nUNS, nDIV, nDES, cells_gen = self._storage()

    # Compute probability distribution
    pdfDD = self.compute_pdf(times, params["mDD"], params["sDD"])

    # Compute survival functions (i.e. 1 - cdf)
    sfUns = self.compute_sf(times, params["mUns"], params["sUns"])
    sfDiv = self.compute_sf(times, params["mDiv0"], params["sDiv0"])
    sfDie = self.compute_sf(times, params["mDie"], params["sDie"])
    sfDD = self.compute_sf(times, params["mDD"], params["sDD"])

    # Calculate gen = 0 cells
    nUNS = self.n0 * (1. - params["p"]) * sfUns
    nDIV[0,:] = self.n0 * params["p"] * sfDie * sfDiv * sfDD
    nDES[0,:] = self.n0 * params["p"] * sfDie * np.cumsum([x * y for x, y in zip(pdfDD, sfDiv)]) * self.dt
    cells_gen[0,:] = nUNS + nDIV[0,:] + nDES[0,:]  # cells in generation 0

    # Calculate gen > 0 cells
    for igen in range(1, self.max_div+1):
      core = (2.**igen * self.n0 * params["p"])
      upp_cdfDiv = self.compute_cdf(times - ((igen - 1.)*params["b"]), params["mDiv0"], params["sDiv0"])
      low_cdfDiv = self.compute_cdf(times - (igen*params["b"]), params["mDiv0"], params["sDiv0"])
      difference = upp_cdfDiv - low_cdfDiv

      nDIV[igen,:] = core * sfDie * sfDD * difference
      nDES[igen,:] = core * sfDie * np.cumsum([x * y for x, y in zip(pdfDD, difference)]) * self.dt

      if igen < self.exp_max_div:
        cells_gen[igen,:] = nDIV[igen,:] + nDES[igen,:]
      else:
        cells_gen[self.exp_max_div,:] += nDIV[igen,:] + nDES[igen,:]

    # Extract number of live cells at harvested time points from 'cells_gen' array
    model = []
    for itpt, ht in enumerate(self.ht):
      t_idx = np.where(times == ht)[0][0]
      for _irep in range(self.nreps[itpt]):
        for igen in range(self.exp_max_div+1):
          cell = cells_gen[igen, t_idx]
          model.append(cell)

    return np.asfarray(model)

  def extrapolate(self, model_times: types.ExtrapolationTimes, params: types.Parameters) -> types.ExtrapolationResults:
    # Unstimulated death parameters
    mUns = params['mUns']
    sUns = params['sUns']

    # Stimulated cells parameters
    mDiv0 = params['mDiv0']
    sDiv0 = params['sDiv0']
    mDD = params['mDD']
    sDD = params['sDD']
    mDie = params['mDie']
    sDie = params['sDie']

    # Subsequent division time & cell fraction parameters
    b = params['b']
    p = params['p']

    n = model_times.size

    # Compute pdf
    pdfDD = self.compute_pdf(model_times, mDD, sDD)

    # Compute 1 - cdf
    sfUns = self.compute_sf(model_times, mUns, sUns)
    sfDiv = self.compute_sf(model_times, mDiv0, sDiv0)
    sfDie = self.compute_sf(model_times, mDie, sDie)
    sfDD = self.compute_sf(model_times, mDD, sDD)

    # Declare 2 arrays for unstimulated cells, divided cells & destiny cells
    nDIV = np.zeros(shape=(self.max_div+1, n), dtype=DTYPE)
    nDES = np.zeros(shape=(self.max_div+1, n), dtype=DTYPE)

    # Store number of cells at all time per generation
    cells_gen = np.zeros(shape=(self.exp_max_div+1, n), dtype=DTYPE)

    # Store total live cells
    total_live_cells = np.zeros(shape=n, dtype=DTYPE)

    # Calculate gen = 0 cells
    nUNS = self.n0 * (1. - p) * sfUns
    nDIV[0,:] = self.n0 * p * sfDie * sfDiv * sfDD
    nDES[0,:] = self.n0 * p * sfDie * np.cumsum([x * y for x, y in zip(pdfDD, sfDiv)]) * self.dt
    cells_gen[0,:] = nUNS + nDIV[0,:] + nDES[0,:]  # cells in generation 0

    # Calculate gen > 0 cells
    for igen in range(1, self.max_div+1):
      core = (2.**igen * self.n0 * p)

      upp_cdfDiv = self.compute_cdf(model_times - ((igen - 1.)*b), mDiv0, sDiv0)
      low_cdfDiv = self.compute_cdf(model_times - (igen*b), mDiv0, sDiv0)
      difference = upp_cdfDiv - low_cdfDiv

      nDIV[igen,:] = core * sfDie * sfDD * difference
      nDES[igen,:] = core * sfDie * np.cumsum([x * y for x, y in zip(pdfDD, difference)]) * self.dt

      if igen < self.exp_max_div:
        cells_gen[igen,:] = nDIV[igen,:] + nDES[igen,:]
      else:
        cells_gen[self.exp_max_div,:] += nDIV[igen,:] + nDES[igen,:]
    total_live_cells = np.sum(cells_gen, axis=0)  # sum over all generations per time point

    cells_gen_at_ht = [[] for _ in range(len(self.ht))]
    total_live_cells_at_ht = np.zeros(shape=(len(self.ht)), dtype=DTYPE)
    
    for itpt, ht in enumerate(self.ht):
      t_idx = np.where(model_times == ht)[0][0]
      for igen in range(self.exp_max_div+1):
        cells_gen_at_ht[itpt].append(cells_gen[igen, t_idx])
      total_live_cells_at_ht[itpt] = total_live_cells[t_idx]

    return {
      'ext': {  # Extrapolated cell numbers
        'total_live_cells': total_live_cells,
        'cells_gen': cells_gen,
        'nUNS': nUNS,
        'nDIV': nDIV,
        'nDES': nDES
      },
      'hts': {  # Collect cell numbers at harvested time points
        'total_live_cells': total_live_cells_at_ht,
        'cells_gen': cells_gen_at_ht
      }
    }
