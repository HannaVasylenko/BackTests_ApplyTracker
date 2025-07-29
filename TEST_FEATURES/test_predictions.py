import logging
import pytest


@pytest.fixture(scope="session")
def get_elements_url_and_request_body(config_data: dict):
    data = {
        "textUk": f"{config_data['textUk']}",
        "textEn": f"{config_data['textEn']}"
    }
    return ['api/predictions', data]


def test_add_prediction_unauthorized(api_create_object, config_data: dict):
    data = {
        "textUk": config_data['textUk'],
        "textEn": config_data['textEn']
    }

    response = api_create_object[0].post("api/predictions", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_add_prediction_with_empty_textuk(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "textUk": "",
        "textEn": config_data['textEn']
    }

    response = api_create_object[0].post("api/predictions", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data["error_message_add_with_empty_textuk_prediction"] in response_body['message'], f"Expected error message {config_data["error_message_add_with_empty_textuk_prediction"]} in response, but got: {response_body['message']}"


def test_add_prediction_with_empty_texten(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "textUk": config_data['textUk'],
        "textEn": ""
    }

    response = api_create_object[0].post("api/predictions", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data["error_message_add_with_empty_texten_prediction"] in response_body['message'], f"Expected error message {config_data["error_message_add_with_empty_texten_prediction"]} in response, but got: {response_body['message']}"


def test_add_prediction_without_textuk(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "textEn": config_data['textEn']
    }

    response = api_create_object[0].post("api/predictions", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data["error_message_add_without_textuk_prediction"] in response_body['message'], f"Expected error message {config_data["error_message_add_without_textuk_prediction"]} in response, but got: {response_body['message']}"


def test_add_prediction_without_texten(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "textUk": config_data['textUk']
    }

    response = api_create_object[0].post("api/predictions", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data["error_message_add_without_texten_prediction"] in response_body['message'], f"Expected error message {config_data["error_message_add_without_texten_prediction"]} in response, but got: {response_body['message']}"


def test_get_list_predictions_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].get("api/predictions")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_get_list_predictions_valid(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get("api/predictions", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"


def test_get_prediction_daily_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].get("api/predictions/daily")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_get_prediction_daily_valid(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get("api/predictions/daily", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"


@pytest.mark.skip(reason="Delete from swagger 01/08/25")
def test_get_prediction_by_id_unauthorized(api_create_object, config_data: dict): #404
    response = api_create_object[0].get(f"api/predictions/{config_data['precondition_id']}")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


@pytest.mark.skip(reason="Delete from swagger 01/08/25")
def test_get_prediction_by_id_valid(api_create_object, config_data: dict): #404
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get(f"api/predictions/{config_data['precondition_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    assert response_body['textUk'] == config_data["textUk"], f"The actual textUk of the prediction does not match the expected one, expected prediction textUk: {response_body['textUk']}"
    assert response_body['textEn'] == config_data["textEn"], f"The actual textEn of the prediction does not match the expected one, expected prediction textUk: {response_body['textEn']}"


@pytest.mark.skip(reason="Delete from swagger 01/08/25")
def test_get_prediction_by_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get("api/predictions?id=666666666", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


@pytest.mark.skip(reason="Delete from swagger 01/08/25")
def test_get_prediction_by_invalid_id_as_url(api_create_object, config_data: dict): #404
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get(f"api/predictions/{config_data['invalid_precondition_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_update_prediction_unauthorized(api_create_object, config_data: dict):
    data = {
        "textUk": config_data['textUk'],
        "textEn": config_data['textEn']
    }

    response = api_create_object[0].patch(f"api/predictions/{api_create_object[2]}", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    "textUk",
    "textEn"
])
def test_update_prediction_valid(api_create_object, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        test_input: config_data["upd_precondition_value"]
    }

    response = api_create_object[0].patch(f"api/predictions/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    assert response_body[test_input] == config_data["upd_precondition_value"], f"The actual test_input of the prediction does not match the expected one, expected prediction textUk: {response_body['test_input']}"


def test_update_prediction_with_empty_textuk(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "textUk": ""
    }

    response = api_create_object[0].patch(f"api/predictions/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data["error_message_update_with_empty_textuk_prediction"] in response_body['message'], f"Expected error message {config_data["error_message_update_with_empty_textuk_prediction"]} in response, but got: {response_body['message']}"


def test_update_prediction_with_empty_texten(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "textEn": ""
    }

    response = api_create_object[0].patch(f"api/predictions/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data["error_message_update_with_empty_texten_prediction"] in response_body['message'], f"Expected error message {config_data["error_message_update_with_empty_texten_prediction"]} in response, but got: {response_body['message']}"


def test_update_prediction_with_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "textUk": config_data['textUk'],
        "textEn": config_data['textEn']
    }

    response = api_create_object[0].patch("api/predictions?id=666666666", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_update_prediction_with_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "textUk": config_data['textUk'],
        "textEn": config_data['textEn']
    }

    response = api_create_object[0].patch(f"api/predictions/{config_data['invalid_precondition_id']}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_update_prediction_without_prediction_id(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "textUk": config_data['textUk'],
        "textEn": config_data['textEn']
    }

    response = api_create_object[0].patch("api/predictions", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_update_without_id_prediction'], f"Expected error message {config_data['error_message_update_without_id_prediction']} in response, but got: {response_body['message']}"


def test_delete_prediction_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].delete(f"api/predictions/{api_create_object[2]}")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_get_prediction_after_deleting(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get(f"api/predictions/{api_create_object[2]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == f"{config_data['error_message_get_after_deleting_prediction']}/{api_create_object[2]}", f"Expected error message {config_data['error_message_get_after_deleting_prediction']} in response, but got: {response_body['message']}"


def test_delete_prediction_with_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete("api/predictions?id=666666666", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_delete_prediction_with_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete(f"api/predictions/{config_data['invalid_precondition_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_delete_prediction_without_prediction_id(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete("api/predictions", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_delete_without_id_prediction'], f"Expected error message {config_data['error_message_delete_without_id_prediction']} in response, but got: {response_body['message']}"


def test_seed_prediction_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].post("api/predictions/seed")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


# @pytest.mark.skip(reason="Do not check")
# def test_seed_predictions_valid(api_create_object, config_data: dict):
#     headers = {
#         "Authorization": f"Bearer {api_create_object[1]}"
#     }
#
#     response = api_create_object[0].post("api/predictions/seed", headers=headers)
#     status = response.status
#     response_body = response.json()
#     logging.info(f"Response: {response_body}")
#     assert status == 201, f"Expected status 201, but got {status}. Response: {response_body}"
#     assert response_body['count'] == 40, f"Expected count of predictions is '40' in response, but got: {response_body['count']}"
