import logging
import pytest


@pytest.fixture(scope="session")
def get_elements_url_and_request_body(config_data: dict):
    data = {
        "name": f"{config_data['note_name']}",
        "text": f"{config_data['note_text']}"
    }
    return ['api/notes', data]

def test_add_note_unauthorized(api_create_object, config_data: dict):
    data = {
        "name": config_data["note_name"],
        "text": config_data['note_text']
    }

    response = api_create_object[0].post("api/notes", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_add_note_with_empty_name(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": ""
    }

    response = api_create_object[0].post("api/notes", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_with_empty_name_note'] in response_body['message'], f"Expected error message {config_data['error_message_add_with_empty_name_note']} in response, but got: {response_body['message']}"


def test_add_note_without_name(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "text": "note"
    }

    response = api_create_object[0].post("api/notes", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_without_name_note'] in response_body['message'], f"Expected error message {config_data['error_message_add_without_name_note']} in response, but got: {response_body['message']}"


def test_get_list_notes_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].get("api/notes")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_get_list_notes_valid(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get("api/notes", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"


def test_get_note_by_id_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].get(f"api/notes/{api_create_object[2]}")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_get_note_by_id_valid(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get(f"api/notes/{api_create_object[2]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    assert response_body['name'] == config_data["note_name"], f"The actual name of the note does not match the expected one, expected note name: {response_body['name']}"


def test_get_note_by_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get("api/notes?id=888888", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_get_note_by_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get(f"api/notes/{config_data['invalid_note_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_update_note_unauthorized(api_create_object, config_data: dict):
    data = {
        "name": config_data["note_name"],
        "text": config_data['note_text']
    }

    response = api_create_object[0].patch(f"api/notes/{api_create_object[2]}", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    "name",
    "text"
])
def test_update_note_valid(api_create_object, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        test_input: config_data["upd_note_name"]
    }

    response = api_create_object[0].patch(f"api/notes/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    updated_value = response_body['result'][test_input]
    assert updated_value == config_data["upd_note_name"], f"Expected updated note name: {config_data['upd_note_name']}, but got: {updated_value}. Response: {response_body}"


def test_update_note_with_empty_name(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": ""
    }

    response = api_create_object[0].patch(f"api/notes/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_update_with_empty_name_note'] in response_body['message'], f"Expected error message {config_data['error_message_update_with_empty_name_note']} in response, but got: {response_body['message']}"


def test_update_note_with_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data["note_name"],
        "text": config_data['note_text']
    }

    response = api_create_object[0].patch("api/notes?id=888888", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_update_note_with_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data["note_name"],
        "text": config_data['note_text']
    }

    response = api_create_object[0].patch(f"api/notes/{config_data['invalid_note_id']}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_update_note_without_note_id(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data["note_name"],
        "text": config_data['note_text']
    }

    response = api_create_object[0].patch("api/notes", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_update_without_id_note'], f"Expected error message {config_data['error_message_update_without_id_note']} in response, but got: {response_body['message']}"


def test_delete_note_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].delete(f"api/notes/{api_create_object[2]}")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_delete_note_with_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete("api/notes?id=888888", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_delete_note_with_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete(f"api/notes/{config_data['invalid_note_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_delete_note_without_note_id(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete("api/notes", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_delete_without_id_note'], f"Expected error message {config_data['error_message_delete_without_id_note']} in response, but got: {response_body['message']}"
