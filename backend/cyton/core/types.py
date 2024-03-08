from typing import TypedDict, Sequence, TYPE_CHECKING
from numpy.typing import NDArray
import numpy as np
from pydantic import BaseModel
from cyton.core.utils import flatten
from cyton.core.settings import DT

if TYPE_CHECKING:
    from cyton.core.cyton2 import Cyton2Model
else:
    from cyton.core.model import Cyton2Model

type Number = int | float

class Parameters(TypedDict):
    # These are floats
    mUns: float
    "Median unstimulated death time"
    sUns: Number 
    "Log variance of unstimulated death time"
    mDiv0: Number
    "Median time to first division"
    sDiv0: Number
    "Log variance of time to first division"
    mDD: Number
    "Median time to division destiny"
    sDD: Number
    "Time to division destiny"
    mDie: Number
    "Median time to death"
    sDie: Number
    "Log variance of the time to death"
    b: Number
    "Subsequent division time"
    p: Number
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
    "Unused metadata format"
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

# Harvest Times types
type HarvestTime = float
"Time of sample collection in hours"
# type HarvestTimes = Sequence[HarvestTime]
# "Time of sample collection for a single condition in hours, indexed by timepoints"
# type HarvestTimePerCond = Sequence[HarvestTimes]
# "Time of sample collection in hours, indexed by conditions then timepoints"
# type HarvestTimesReps = Sequence[HarvestTime]
# "Time of sample collection in hours, indexed by timepoints. The inner list of timepoints is repeated for each replicate."
# type HarvestTimesRepsPerCond = Sequence[HarvestTimesReps]
# "Time of sample collection in hours, indexed by conditions, then timepoints. The inner list of timepoints is repeated for each replicate."

# Generation types
type MaxGeneration = int
"Maximum number of generations, for a single condition"
# type MaxGenerationPerCond = Sequence[MaxGeneration]
# "Maximum number of generations, indexed per condition"

# Cell counts
type CellCount = float
"Number of cells. This can be a float because the assay may not return discretized counts."
# type CellPerGensReps = PerTime[PerRep[PerGen[CellCount]]]
# "Cell counts for a single condition, indexed by timepoint, repetition then generation."
# type CellPerGensRepsCond = Sequence[CellPerGensReps]
"Number of cells, indexed by condition, timepoint, repetition then generation."

# Miscellaneous types
type NumTimePoints = Sequence[int]
"Number of time points, indexed by condition"
type Conditions = Sequence[str]
"Condition names, in the order of the dataset"
# It is correct that these are floats and not integers!
type NReps = PerTime[int]
"Number of replicates, indexed by time point."

# Total cell counts, summed over all generations
type CellTotal = float
"Total number of cells, summed over all generations."
type CellAverage = float
"Average number of cells over all replicates"
type CellTotalSem = float
"Standard error of the mean"
# type TotalCells = Sequence[CellTotal]
# "Total number of cells, summed over all generations, indexed by timepoint."
# type TotalCellsPerCond = Sequence[TotalCells]
# "Total number of cells, summed over all generations, indexed by condition, then timepoint."
# type TotalCellsReps = Sequence[CellTotal]
# "Total number of cells, summed over all generations, indexed by timepoint. The inner list of timepoints is repeated for each replicate."
# type TotalCellsRepsPerCond = Sequence[TotalCellsReps]
# "Total number of cells, summed over all generations, indexed by condition, then timepoint. The inner list of timepoints is repeated for each replicate."
# type TotalCellsSem = Sequence[Sequence[float]]
# "Standard error of the mean. Indexed by condition, then timepoint."

# type AvgCellPerGen = Sequence[Sequence[Sequence[float]]]
# "Average number of cells. Indexed by condition, then timepoint, then generation."
# type CellsPerGenSem = Sequence[Sequence[float]]
# "Standard error of the mean. Indexed by condition, then timepoint."

class ExtrapolatedData(TypedDict):
    ext_total_live_cells: NDArray[np.float64]
    "Extrapolated number of total live cells. Indexed by extrapolated timepoint."
    ext_cells_per_gen: NDArray[np.float64]
    "Extrapolated number of total live cells. Indexed by generation then extrapolated timepoint."
    hts_total_live_cells: NDArray[np.float64]
    "Extrapolated number of total live cells at the experimental timepoint. Indexed by experimental timepoint."
    hts_cells_per_gen: Sequence[Sequence[float]]
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
    cells_gen: Sequence[Sequence[float]]
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
