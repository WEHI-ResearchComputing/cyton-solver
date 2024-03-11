from typing import TypedDict, Sequence
from numpy.typing import NDArray
import numpy as np

class Parameters(TypedDict):
    # These are floats
    mUns: float
    "Median unstimulated death time"
    sUns: float 
    "Log variance of unstimulated death time"
    mDiv0: float
    "Median time to first division"
    sDiv0: float
    "Log variance of time to first division"
    mDD: float
    "Median time to division destiny"
    sDD: float
    "Time to division destiny"
    mDie: float
    "Median time to death"
    sDie: float
    "Log variance of the time to death"
    b: float
    "Subsequent division time"
    p: float
    "Proportion of activated cells"

class Bounds(TypedDict):
    lb: Parameters
    "Lower bound"
    ub: Parameters
    "Upper bound"

class FittableParams(TypedDict):
    "True if a parameter is fittable. See Parameters class for details."
    mUns: bool
    sUns: bool
    mDiv0: bool
    sDiv0: bool
    mDD: bool
    sDD: bool
    mDie: bool
    sDie: bool
    b: bool
    p: bool


class LegacyExperimentMetadata(TypedDict):
    "Old metadata format"
    stimulus: str
    date: str
    cell_type: str
    comment: str

class ExperimentInfo(TypedDict):
    "Modern metadata format"
    num_tp: int
    "Number of timepoints"
    last_gen: int
    "Maximum generation number. Generally less than 10."
    num_condition: int
    "Number of conditions"
    num_replicate: int
    "Targeted/desired number of replicates"
    num_beads: float
    "Number of beads"
    prop_bead_gated: float
    "Proportion of beads that are gated"

# Index order is always: condition, timepoint, repetition then generation
type PerCond[T] = Sequence[T]
"Something that is indexed by condition"
type PerGen[T] = Sequence[T]
"Something that is indexed by generation"
type PerTime[T] = Sequence[T]
"Something that is indexed by time point"
type PerRep[T] = Sequence[T]
"Something that is indexed by replicate"
type Reps[T] = Sequence[T]
"Something that is indexed by time point, but also with each value repeated per replicate"

type HarvestTime = float
"Time of sample collection in hours"
type MaxGeneration = int
"Maximum number of generations, for a single condition"
type CellCount = float
"Number of cells. This can be a float because the assay may not return discretized counts."
type NumTimePoints = PerCond[int]
"Number of time points, indexed by condition"
type Conditions = Sequence[str]
"Condition names, in the order of the dataset"
type NReps = PerTime[int]
"Number of replicates, indexed by time point."
type CellTotal = float
"Total number of cells, summed over all generations."
type CellAverage = float
"Average number of cells over all replicates"
type CellTotalSem = float
"Standard error of the mean"

class ExtrapolatedData(TypedDict):
    ext_total_live_cells: NDArray[np.float64]
    "Extrapolated number of total live cells. Indexed by extrapolated timepoint."
    ext_cells_per_gen: NDArray[np.float64]
    "Extrapolated number of total live cells. Indexed by generation then extrapolated timepoint."
    hts_total_live_cells: NDArray[np.float64]
    "Extrapolated number of total live cells at the experimental timepoint. Indexed by experimental timepoint."
    hts_cells_per_gen: PerGen[PerTime[float]]
    "Extrapolated number of total live cells. Indexed by generation then experimental timepoint."

# Extrapolation
type ExtrapolationParams = tuple[PerCond[HarvestTime], PerCond[PerTime[PerRep[PerGen[CellCount]]]], PerCond[MaxGeneration]]
type ExtrapolationTimes = NDArray[np.float_]
class ExtrapolatedTimeResults(TypedDict):
    total_live_cells: NDArray[np.float64]
    "Cell numbers per timepoint, summed over all generations. 1d array."
    cells_gen: NDArray[np.float64]
    "2D array of cell numbers indexed by generation (first axis) and timepoint (second axis)."
    nUNS: NDArray[np.float64]
    "Unused 1D array. Predicted number of unstimulated cells that don't divide, indexed by timepoint."
    nDIV: NDArray[np.float64]
    "2D array. Predicted number of dividing cells, indexed by generation (first axis) then timepoint (second axis)."
    nDES: NDArray[np.float64]
    "2D array. Predicted number of destiny cells, indexed by generation (first axis) then timepoint (second axis)."

class HarvestTimeResults(TypedDict):
    total_live_cells: NDArray[np.float64]
    "Cell numbers per timepoint, summed over all generations. 1d array."
    cells_gen: PerGen[PerTime[float]]
    "2D array of cell numbers indexed by generation (first axis) and timepoint (second axis)."

class ExtrapolationResults(TypedDict):
    ext: ExtrapolatedTimeResults
    "Predicted data for extrapolated timepoints"
    hts: HarvestTimeResults
    "Predicted data for experimental harvested timepoints"

# Fitting
type ExcludedParameters = list[str]
class LmFitKwargs(TypedDict):
    epsfcn: float
    "Epsilon function condition. If the change in a parameter causes the change in the residual result by less than this number, that parameter is excluded. "
