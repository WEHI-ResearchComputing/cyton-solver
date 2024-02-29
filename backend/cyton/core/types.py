from typing import Literal, TypedDict, Sequence

Number = int | float

class Parameters(TypedDict):
    mUns: Number
    sUns: Number  # Unstimulated death time
    mDiv0: Number
    sDiv0: Number     # Time to first division
    mDD: Number
    sDD: Number         # Time to division destiny
    mDie: Number
    sDie: Number       # Time to death
    b: Number
    p: Number                # Subsequent division time & Proportion of activated cells

class Bounds(TypedDict):
    lb: Parameters
    ub: Parameters

class Vary(TypedDict):
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

class DefaultSettings(TypedDict):
    parameters: Parameters
    bounds: Bounds
    vary: Vary

class LegacyExperimentMetadata(TypedDict):
    stimulus: str
    date: str
    cell_type: str
    comment: str

class ExperimentInfo(TypedDict):
    num_tp: int
    last_gen: int
    num_condition: int
    num_replicate: int
    num_beads: int
    prop_bead_gated: int

MetaInformation = LegacyExperimentMetadata | ExperimentInfo
GenerationPerCondition = Sequence[int]
HarvestedTimes = Sequence[Sequence[int]]
HarvestedTimesReps = Sequence[Sequence[int]]
NumTimePoints = Sequence[int]
Conditions = Sequence[str]
CellNumber = Sequence[Sequence[Sequence[int]]]
"Number of cells, indexed by condition, then generation"
CellNumber4D = Sequence[Sequence[Sequence[Sequence[int | None]]]]
"Number of cells, indexed by condition, timepoint, repetition then generation."
TotalCells = Sequence[Sequence[int]]
TotalCellsReps = Sequence[Sequence[int]]
TotalCellsSem = Sequence[Sequence[float]]
"Standard error of the mean. Indexed by condition, then timepoint"
AvgCellPerGen = Sequence[Sequence[float]]
"Average number of cells per generation. Indexed by condition, then generation"
C15Check = Sequence[Sequence[Sequence[Literal[1]]]]

class ExperimentData(TypedDict):
    exp_ht: HarvestedTimes
    exp_ht_reps: HarvestedTimesReps
    max_div_per_conditions: GenerationPerCondition
    conditions: Conditions
    exp_num_tp: NumTimePoints
    total_cells: TotalCells
    total_cells_reps: TotalCellsReps
    total_cells_sem: TotalCellsSem
    cell_gens: AvgCellPerGen
    cell_gens_reps: TotalCellsReps
    cell_gens_sem: TotalCellsSem
    c15_check: C15Check
