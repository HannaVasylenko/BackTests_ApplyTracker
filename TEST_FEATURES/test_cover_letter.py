import logging
import pytest


@pytest.fixture(scope="session")
def get_elements_url_and_request_body(config_data: dict):
    data = {
        "name": f"{config_data['cover_letter_name']}",
        "text": f"{config_data['cover_letter_text']}"
    }
    return ['api/cover-letter', data]

def test_add_cover_letter_unauthorized(api_create_object, config_data: dict):
    data = {
        "name": config_data['cover_letter_name'],
        "text": config_data['cover_letter_text']
    }

    response = api_create_object[0].post("api/cover-letter", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_add_cover_letter_with_empty_name(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": "",
        "text": config_data['cover_letter_text']
    }

    response = api_create_object[0].post("api/cover-letter", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_with_empty_name_cover_letter'] in response_body['message'], f"Expected error message {config_data['error_message_with_empty_name_cover_letter']} in response, but got: {response_body['message']}"


def test_add_cover_letter_with_empty_text(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['cover_letter_name'],
        "text": ""
    }

    response = api_create_object[0].post("api/cover-letter", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_with_empty_text_cover_letter'] in response_body['message'], f"Expected error message {config_data['error_message_with_empty_text_cover_letter']} in response, but got: {response_body['message']}"


def test_add_cover_letter_without_name(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "text": config_data['cover_letter_text']
    }

    response = api_create_object[0].post("api/cover-letter", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_without_name_cover_letter'] in response_body['message'], f"Expected error message {config_data['error_message_without_name_cover_letter']} in response, but got: {response_body['message']}"


def test_add_cover_letter_without_text(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['cover_letter_name']
    }

    response = api_create_object[0].post("api/cover-letter", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_without_text_cover_letter'] in response_body['message'], f"Expected error message {config_data['error_message_without_text_cover_letter']} in response, but got: {response_body['message']}"


def test_get_list_cover_letters_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].get("api/cover-letter")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_get_list_cover_letters_valid(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get("api/cover-letter", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"


def test_get_cover_letter_by_id_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].get(f"api/cover-letter/{api_create_object[2]}")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_get_cover_letter_by_id_valid(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get(f"api/cover-letter/{api_create_object[2]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    assert response_body['name'] == config_data["cover_letter_name"]


def test_get_cover_letter_by_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get("api/cover-letter?id=555555", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_get_cover_letter_by_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get(f"api/cover-letter/{config_data['invalid_cover_letter_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_update_cover_letter_unauthorized(api_create_object, config_data: dict):
    data = {
        "name": config_data['cover_letter_name'],
        "text": config_data['cover_letter_text']
    }

    response = api_create_object[0].patch(f"api/cover-letter/{api_create_object[2]}", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    "name",
    "text"
])
def test_update_cover_letter_valid(api_create_object, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        test_input: config_data["upd_cover_letter_value"]
    }

    response = api_create_object[0].patch(f"api/cover-letter/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    assert response_body[test_input] == config_data["upd_cover_letter_value"]


def test_update_cover_letter_with_empty_name(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": ""
    }

    response = api_create_object[0].patch(f"api/cover-letter/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data["error_message_update_with_empty_name_or_text"] in response_body['message'], f"{config_data["error_message_update_with_empty_name_or_text"]} in response, but got: {response_body['message']}"


def test_update_cover_letter_with_empty_text(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "text": ""
    }

    response = api_create_object[0].patch(f"api/cover-letter/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data["error_message_update_with_empty_name_or_text"] in response_body['message'], f"Expected error message {config_data["error_message_update_with_empty_name_or_text"]} in response, but got: {response_body['message']}"


def test_update_cover_letter_with_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['cover_letter_name'],
        "text": config_data['cover_letter_text']
    }

    response = api_create_object[0].patch("api/cover-letter?id=555555", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_update_cover_letter_with_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['cover_letter_name'],
        "text": config_data['cover_letter_text']
    }

    response = api_create_object[0].patch(f"api/cover-letter/{config_data['invalid_cover_letter_id']}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_update_cover_letter_without_cover_letter_id(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['cover_letter_name'],
        "text": config_data['cover_letter_text']
    }

    response = api_create_object[0].patch(f"api/cover-letter", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_update_without_cover_letter_id_cover_letter'], f"Expected error message {config_data['error_message_update_without_cover_letter_id_cover_letter']} in response, but got: {response_body['message']}"


def test_delete_cover_letter_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].delete(f"api/cover-letter/{api_create_object[2]}")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_delete_cover_letter_with_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete("api/cover-letter?id=555555", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_delete_cover_letter_with_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete(f"api/cover-letter/{config_data['invalid_cover_letter_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected message config_data['error_message_by_invalid_id_as_url'] in response, but got: {response_body['message']}"


def test_delete_cover_letter_without_cover_letter_id(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete("api/cover-letter", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_delete_without_cover_letter_id_cover_letter'], f"Expected message {config_data['error_message_delete_without_cover_letter_id_cover_letter']} in response, but got: {response_body['message']}"
