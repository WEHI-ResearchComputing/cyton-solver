from cyton.api.support.default_settings import get_default_settings
from cyton.api.support.upload import parse_file
from numpy.testing import assert_approx_equal
from pathlib import Path

def test_round_trip():
    data_location = Path(__file__).parent / "SH1.119.xlsx"
    experiment_data = parse_file(str(data_location))
    cond_data = experiment_data.slice_condition_idx(0)
    
    model = cond_data.get_model()
    params = cond_data.fit_model(model, get_default_settings())

    assert_approx_equal(params["mDiv0"], 39.81, significant=2)
    assert_approx_equal(params["sDiv0"], 0.28, significant=2)
    assert_approx_equal(params["mDD"], 71.82, significant=2)
    assert_approx_equal(params["sDD"], 0.11, significant=2)
    assert_approx_equal(params["mDie"], 115.88, significant=2)
    assert_approx_equal(params["sDie"], 0.84, significant=2)
    assert_approx_equal(params["b"], 9.20, significant=1)

    cond_data.extrapolate_model(model, params)
