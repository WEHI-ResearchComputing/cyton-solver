from typing import Literal, TypedDict, Sequence
from numpy.typing import NDArray
import numpy as np

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
    ub: Parameters

class FittableParams(TypedDict):
    "True if a parameter is fittable"
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

class ExperimentSettings(TypedDict):
    parameters: Parameters
    bounds: Bounds
    vary: FittableParams

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

type MetaInformation = LegacyExperimentMetadata | ExperimentInfo

type CellPerGensReps = Sequence[Sequence[Sequence[float]]]
"Cell counts for a single condition, indexed by indexed by timepoint, repetition then generation."
type HarvestTimes = Sequence[float]
"Time of sample collection for a single condition in hours, indexed by timepoints"
type MaxGeneration = int
"Maximum number of generations, for a single condition"
type MaxGenerationPerCond = Sequence[MaxGeneration]
"Maximum number of generations, indexed per condition"
type HarvestTimesPerCondition = Sequence[HarvestTimes]
"Time of sample collection in hours, indexed by conditions then timepoints"
type HarvestedTimesReps = Sequence[Sequence[Number]]
"Time of sample collection in hours, indexed by conditions, then timepoints. The inner list of timepoints is repeated for each replicate."
type NumTimePoints = Sequence[int]
"Number of time points, indexed by condition"
type Conditions = Sequence[str]
"Condition names, in the order of the dataset"
# It is correct that these are floats and not integers!
type CellPerGensRepsCond = Sequence[CellPerGensReps]
"Number of cells, indexed by condition, timepoint, repetition then generation."
type NReps = Sequence[int]
"Number of replicates, indexed by time point."

type TotalCells = Sequence[Sequence[float]]
"Total number of cells, indexed by condition, then timepoint."
type TotalCellsReps = Sequence[Sequence[float]]
"Total number of cells, indexed by condition, then timepoint. The inner list of timepoints is repeated for each replicate."
type TotalCellsSem = Sequence[Sequence[float]]
"Standard error of the mean. Indexed by condition, then timepoint."

type AvgCellPerGen = Sequence[Sequence[Sequence[float]]]
"Average number of cells. Indexed by condition, then timepoint, then generation."
type CellsPerGenSem = Sequence[Sequence[float]]
"Standard error of the mean. Indexed by condition, then timepoint."

C15Check = Sequence[Sequence[Sequence[Literal[1]]]]

class ExperimentData(TypedDict):
    exp_ht: HarvestTimesPerCondition
    exp_ht_reps: HarvestedTimesReps
    max_div_per_conditions: MaxGenerationPerCond
    conditions: Conditions
    exp_num_tp: NumTimePoints

    total_cells: TotalCells
    total_cells_reps: TotalCellsReps
    total_cells_sem: TotalCellsSem

    cell_gens: AvgCellPerGen
    cell_gens_reps: CellPerGensRepsCond
    cell_gens_sem: CellsPerGenSem

    c15_check: C15Check

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
type ExtrapolationParams = tuple[HarvestTimesPerCondition, CellPerGensRepsCond, MaxGenerationPerCond]
type ExtrapolationTimes = NDArray[np.float_]
class ExtrapolatedTimeResults(TypedDict):
    total_live_cells: NDArray[np.float64]
    "1D array"
    cells_gen: NDArray[np.float64]
    "2d array"
    nUNS: NDArray[np.float64]
    nDIV: NDArray[np.float64]
    nDES: NDArray[np.float64]

class HarvestTimeResults(TypedDict):
    total_live_cells: NDArray[np.float64]
    cells_gen: Sequence[Sequence[float]]

class ExtrapolationResults(TypedDict):
    ext: ExtrapolatedTimeResults
    "Predicted data for extrapolated timepoints"
    hts: HarvestTimeResults
    "Predicted data for experimental harvested timepoints"

# Fitting
type ExcludedParameters = list[str]
class LmFitKwargs(TypedDict):
    epsfcn: float
