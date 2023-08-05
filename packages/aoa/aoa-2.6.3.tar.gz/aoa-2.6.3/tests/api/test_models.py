import pytest
from aoa.api.model_api import ModelApi


def test_model(setup):
    model_api = ModelApi(pytest.aoa_client)
    models_all_rtn = model_api.find_all()['_embedded']['models']

    if len(models_all_rtn) > 0:
        model_rtn = models_all_rtn[0]

    model_by_id_rtn = model_api.find_by_id(model_id=model_rtn['id'])

    assert (model_rtn == model_by_id_rtn), "validate models...failed"
