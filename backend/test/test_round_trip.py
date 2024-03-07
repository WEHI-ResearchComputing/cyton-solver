from api.support.default_settings import get_default_settings
from api.support.extrapolate import extrapolate_model
from api.support.start_fit import fit_model
from api.support.upload import parse_file
from numpy.testing import assert_approx_equal

def test_round_trip():
    experiment_data = parse_file("test/SH1.119.xlsx")
    cell_gens_reps = experiment_data["cell_gens_reps"]
    exp_ht = experiment_data["exp_ht"]
    max_div_per_conditions = experiment_data["max_div_per_conditions"]
    settings = get_default_settings()
    mUns, sUns, mDiv0, sDiv0, mDD, sDD, mDie, sDie, b, p = fit_model(
        exp_ht=exp_ht,
        cell_gens_reps=cell_gens_reps,
        max_div_per_conditions=max_div_per_conditions,
        settings=settings
    )
    assert_approx_equal(mDiv0, 39.81, significant=2)
    assert_approx_equal(sDiv0, 0.28, significant=2)
    assert_approx_equal(mDD, 71.82, significant=2)
    assert_approx_equal(sDD, 0.11, significant=2)
    assert_approx_equal(mDie, 115.88, significant=2)
    assert_approx_equal(sDie, 0.84, significant=2)
    assert_approx_equal(b, 9.20, significant=1)

    extrapolate_model(exp_ht, max_div_per_conditions, cell_gens_reps, dict(
        mUns = mUns,
        sUns = sUns,
        mDiv0 = mDiv0,
        sDiv0 = sDiv0,
        mDD = mDD,
        sDD = sDD,
        mDie = mDie,
        sDie = sDie,
        b = b,
        p = p
    ))
