"""
Last Edit: 11-Feb-2024

Cyton2 Algorithm Model
"""
import numpy as np
from scipy.stats import lognorm, norm

DTYPE = np.float64

class Cyton2Model:
  def __init__(self, ht, n0, max_div, dt, nreps, logn=True):

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

  def compute_pdf(self, times, mu, sig):
    if self.logn:
      return lognorm.pdf(times, sig, scale=mu)
    else:
      return norm.pdf(times, mu, sig)

  def compute_cdf(self, times, mu, sig):
    if self.logn:
      return lognorm.cdf(times, sig, scale=mu)
    else:
      return norm.cdf(times, mu, sig)

  def compute_sf(self, times, mu, sig):
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
  def evaluate(self,
               mUns, sUns,    # unstimulated death
               mDiv0, sDiv0,  # time to first division
               mDD, sDD,      # division destiny
               mDie, sDie,    # stimulated death
               b, p):         # subsequent division time, activation probability
    times = self.times

    # Create empty arrays
    pdfDD, sfUns, sfDiv, sfDie, sfDD, nUNS, nDIV, nDES, cells_gen = self._storage()

    # Compute probability distribution
    pdfDD = self.compute_pdf(times, mDD, sDD)

    # Compute survival functions (i.e. 1 - cdf)
    sfUns = self.compute_sf(times, mUns, sUns)
    sfDiv = self.compute_sf(times, mDiv0, sDiv0)
    sfDie = self.compute_sf(times, mDie, sDie)
    sfDD = self.compute_sf(times, mDD, sDD)

    # Calculate gen = 0 cells
    nUNS = self.n0 * (1. - p) * sfUns
    nDIV[0,:] = self.n0 * p * sfDie * sfDiv * sfDD
    nDES[0,:] = self.n0 * p * sfDie * np.cumsum([x * y for x, y in zip(pdfDD, sfDiv)]) * self.dt
    cells_gen[0,:] = nUNS + nDIV[0,:] + nDES[0,:]  # cells in generation 0

    # Calculate gen > 0 cells
    for igen in range(1, self.max_div+1):
      core = (2.**igen * self.n0 * p)
      upp_cdfDiv = self.compute_cdf(times - ((igen - 1.)*b), mDiv0, sDiv0)
      low_cdfDiv = self.compute_cdf(times - (igen*b), mDiv0, sDiv0)
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
      for irep in range(self.nreps[itpt]):
        for igen in range(self.exp_max_div+1):
          cell = cells_gen[igen, t_idx]
          model.append(cell)

    return np.asfarray(model)

  def extrapolate(self, model_times, params):
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

    res = {
      'ext': {  # Extrapolated cell numbers
        'total_live_cells': total_live_cells,
        'cells_gen': cells_gen,
        'nUNS': nUNS, 'nDIV': nDIV, 'nDES': nDES
      },
      'hts': {  # Collect cell numbers at harvested time points
        'total_live_cells': total_live_cells_at_ht,
        'cells_gen': cells_gen_at_ht
      }
    }

    return res