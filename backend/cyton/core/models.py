from __future__ import annotations
from cyton.core.settings import DT
from cyton.core.utils import flatten
from cyton.core.extrapolate import get_times
from cyton.core.model_fitting import fit
from cyton.core.types import *
from cyton.core.model import Cyton2Model
from pydantic import BaseModel
import lmfit as lmf

class ExperimentSettings(BaseModel):
    """
    Settings that define how the model will be fitted
    """
    parameters: Parameters
    "Initial parameter estimates"
    bounds: Bounds
    vary: FittableParams

    def get_lmf_parameters(self) -> tuple[lmf.Parameters, ExcludedParameters]:
        """
        Generate the data structures needed by the lmfit library
        """
        params = lmf.Parameters()
        for par in self.parameters:
            params.add(par, value=self.parameters[par], min=self.bounds['lb'][par], max=self.bounds['ub'][par], vary=self.vary[par])
        paramExcl = [p for p in params if not params[p].vary]  # List of locked parameters

        return params, paramExcl

class SingleConditionData(BaseModel):
    """
    Experiment data for a single condition
    """
    exp_ht: PerTime[HarvestTime]
    exp_ht_reps: Reps[HarvestTime]
    max_div: MaxGeneration
    exp_num_tp: int

    total_cells: PerTime[CellTotal]
    total_cells_reps: Reps[CellTotal]
    total_cells_sem: PerTime[CellTotalSem]

    cell_gens: PerTime[PerGen[CellAverage]]
    cell_gens_reps: PerTime[PerRep[PerGen[CellCount]]]
    cell_gens_sem: PerTime[PerGen[CellTotalSem]]

    def get_times(self) -> ExtrapolationTimes:
        """
        Gets the times over which the model will be extrapolated
        """
        return get_times(self.exp_ht)

    def calc_nreps(self) -> NReps:
        """
        Calculate the number of replicates per timepoint
        """
        return [len(l) for l in self.cell_gens_reps]

    def calc_n0(self) -> float:
        """
        Calculates N0, the initial average number of cells.
        This is taken to be the average cell numbers at 0th time point.
        """
        return np.mean([sum(flatten(rep)) for rep in self.cell_gens_reps[0]]).item(0)

    def get_model(self) -> Cyton2Model:
        return Cyton2Model(
            ht=self.exp_ht,
            n0 = self.calc_n0(),
            max_div = self.max_div,
            dt = DT,
            nreps=self.calc_nreps()
        )

    def fit_model(self, model: Cyton2Model, settings: ExperimentSettings) -> Parameters:
        """
        Fits the model given some settings, and returns the fitted results
        """
        params, paramExcl = settings.get_lmf_parameters()
        return fit(self.exp_ht, self.cell_gens_reps, params, paramExcl, model)

    def extrapolate_model(self, model: Cyton2Model, params: Parameters) -> ExtrapolationResults:
        """
        Predicts cell counts for harvest times saved in exp_ht
        """
        times = self.get_times()
        return model.extrapolate(times, params)


class ExperimentData(BaseModel):
    """
    Experiment data for all conditions
    """
    exp_ht: PerCond[PerTime[HarvestTime]]
    exp_ht_reps: PerCond[Reps[HarvestTime]]
    max_div_per_conditions: PerCond[MaxGeneration]
    conditions: Conditions
    # exp_num_tp: NumTimePoints
    # We can't use NumTimePoints do due to a bug in Pydantic: https://github.com/pydantic/pydantic/issues/8984
    exp_num_tp: PerCond[int]
    "Number of time points, indexed by condition"

    total_cells: PerCond[PerTime[CellTotal]]
    total_cells_reps: PerCond[Reps[CellTotal]]
    total_cells_sem: PerCond[PerTime[CellTotalSem]]

    cell_gens: PerCond[PerTime[PerGen[CellAverage]]]
    cell_gens_reps: PerCond[PerTime[PerRep[PerGen[CellCount]]]]
    cell_gens_sem: PerCond[PerTime[PerGen[CellTotalSem]]]

    def slice_condition_idx(self, condition_index: int) -> SingleConditionData:
        """
        Get all the data for a single condition index.
        This is needed since the model is fit separately for each condition.
        Params:
            condition: A condition index
        """
        return SingleConditionData(
            exp_ht=self.exp_ht[condition_index],
            exp_ht_reps=self.exp_ht_reps[condition_index],
            max_div=self.max_div_per_conditions[condition_index],
            exp_num_tp=self.exp_num_tp[condition_index],

            total_cells=self.total_cells[condition_index],
            total_cells_reps=self.total_cells_reps[condition_index],
            total_cells_sem=self.total_cells_sem[condition_index],

            cell_gens=self.cell_gens[condition_index],
            cell_gens_reps=self.cell_gens_reps[condition_index],
            cell_gens_sem=self.cell_gens_sem[condition_index]
        )

    def slice_condition(self, condition: str) -> SingleConditionData:
        """
        Get all the data for a single condition
        Params:
            condition: A condition name
        """
        try:
            condition_index = self.conditions.index(condition)
        except ValueError:
            raise Exception(f"Unknown condition {condition}. Known conditions are: {self.conditions}")

        return self.slice_condition_idx(condition_index)
