import pytest
import uuid
from aoa.api.dataset_template_api import DatasetTemplateApi


def _skip_generated_fields(dataset_template):
    keys_to_remove = ('id', 'ownerId', 'createdAt', '_links', 'projectId')
    for k in keys_to_remove:
        dataset_template.pop(k, None)
    return dataset_template


def test_dataset_template(setup):
    dataset_template_api = DatasetTemplateApi(pytest.aoa_client)
    try:
        before_count = len(dataset_template_api.find_all()['_embedded']['datasetTemplates'])
    except Exception as ex:
        # demo container is initialized without any dataset template
        before_count = 0

    dataset_template_definition = {
        "name": "aoa python client dataset template",
        "description": "adding sample dataset template",
        "templateBody": {
            "basic": {
                "hostname": "mydatabase.com"
            },
            "train": {
                "query": "SELECT * FROM {{table}}",
                "metrics_table": "MY_METRICS_TABLE"
            },
            "evaluate": {
                "query": "SELECT * FROM {{table}}",
                "predictions_table": "MY_PREDICTIONS_TABLE"
            }
        },
        "parameters": {
            "table": "DEFAULT_TABLE"
        }
    }

    dataset_template_rtn = dataset_template_api.save(dataset_template_definition)

    after_count = len(dataset_template_api.find_all()['_embedded']['datasetTemplates'])
    assert ( before_count + 1 == after_count), "save dataset template...failed"

    dataset_template_rtn_by_id = dataset_template_api.find_by_id(dataset_template_id=dataset_template_rtn['id'])
    assert (_skip_generated_fields(dataset_template_rtn_by_id) == dataset_template_definition), "validate find dataset template by id...failed"

    dataset_template_by_name = dataset_template_api.find_by_name(dataset_template_name=dataset_template_definition["name"])
    assert (_skip_generated_fields(dataset_template_by_name) == dataset_template_definition), "validate find dataset template by name...failed"

    dataset_template_rtn_by_id = dataset_template_api.find_by_id(dataset_template_id=str(uuid.uuid4()))
    assert (dataset_template_rtn_by_id is None), "validate missing resouce... failed"

    template_request = {
        "datasetTemplateId": dataset_template_rtn['id'],
        "scope": "train",
        "parameterOverrides": {
            "table": "MY_TRAIN_TABLE"
        }
    }

    rendered_template = dataset_template_api.apply_template(template_request=template_request)
    assert (rendered_template['query'] == "SELECT * FROM MY_TRAIN_TABLE"), "validate apply template with scope -- field: 'query'...failed"
    assert (rendered_template['metrics_table'] == "MY_METRICS_TABLE"), "validate apply template with scope -- field: 'metrics_table'...failed"
    assert (('predictions_table' in rendered_template) == False), "validate apply template with scope -- field: 'predictions_table'...failed"