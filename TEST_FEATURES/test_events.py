import logging
import pytest


@pytest.fixture(scope="session")
def get_elements_url_and_request_body(config_data: dict):
    data = {
        "name": f"{config_data['event_name']}",
        "date": f"{config_data['event_date_valid']}",
        "time": f"{config_data['event_time_valid']}"
    }
    return ['api/events', data]


def test_add_event_unauthorized(api_create_object, config_data: dict):
    data = {
        "name": config_data['event_name'],
        "date": config_data['event_date_valid'],
        "time": config_data['event_time_valid']
    }

    response = api_create_object[0].post("api/events", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_add_event_with_empty_name(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": "",
        "date": config_data['event_date_valid'],
        "time": config_data['event_time_valid']
    }

    response = api_create_object[0].post("api/events", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_with_empty_name_event'] in response_body['message'], f"Expected error message {config_data['error_message_with_empty_name_event']} in response, but got: {response_body['message']}"


def test_add_event_with_empty_date(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data["event_name"],
        "date": "",
        "time": config_data['event_time_valid']
    }

    response = api_create_object[0].post("api/events", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_with_empty_date_event'] in response_body['message'], f"Expected error message {config_data['error_message_with_empty_date_event']} in response, but got: {response_body['message']}"


def test_add_event_with_empty_time(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data["event_name"],
        "date": config_data['event_date_valid'],
        "time": ""
    }

    response = api_create_object[0].post("api/events", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_with_empty_time_event'] in response_body['message'], f"Expected error message {config_data['error_message_with_empty_time_event']} in response, but got: {response_body['message']}"


def test_add_event_without_name(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "date": config_data['event_date_valid'],
        "time": config_data['event_time_valid']
    }

    response = api_create_object[0].post("api/events", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_without_name_event'] in response_body['message'], f"Expected error message {config_data['error_message_without_name_event']} in response, but got: {response_body['message']}"


def test_add_event_without_date(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data["event_name"],
        "time": config_data['event_time_valid']
    }

    response = api_create_object[0].post("api/events", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_without_date_event'] in response_body['message'], f"Expected error message {config_data['error_message_without_date_event']} in response, but got: {response_body['message']}"


def test_add_event_without_time(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data["event_name"],
        "date": config_data['event_date_valid']
    }

    response = api_create_object[0].post("api/events", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_without_time_event'] in response_body['message'], f"Expected error message {config_data['error_message_without_time_event']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    "18.12.2024",
    "18 12 2024",
    "18/12/2024",
    "18 december 2024 year",
    "20245-12-14",
    "2024-123-14",
    "2024-12-143",
    "18-12-2024"
])
def test_add_event_with_invalid_date(api_create_object, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data["event_name"],
        "date": test_input,
        "time": config_data['event_time_valid']
    }

    response = api_create_object[0].post("api/events", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_with_invalid_date_event'] in response_body['message'], f"Expected error message {config_data['error_message_with_invalid_date_event']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    "00-00",
    "0:0",
    "00/00",
    "000:000",
    "12h 30min",
    "00 00"
])
def test_add_event_with_invalid_time(api_create_object, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data["event_name"],
        "date": config_data['event_date_valid'],
        "time": test_input
    }

    response = api_create_object[0].post("api/events", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_with_invalid_time_event'] in response_body['message'], f"Expected error message {config_data['error_message_with_invalid_time_event']} in response, but got: {response_body['message']}"


def test_get_list_events_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].get("api/events")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_get_list_events_valid(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get("api/events", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"


def test_get_event_by_id_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].get(f"api/events/{api_create_object[2]}")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_get_event_by_id_valid(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get(f"api/events/{api_create_object[2]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    assert response_body['name'] == config_data["event_name"], f"The actual name of the event does not match the expected one, expected event name: {response_body['name']}"


def test_get_event_by_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get("api/events?id=33333333", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_get_event_by_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get(f"api/events/{config_data['invalid_event_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_update_event_unauthorized(api_create_object, config_data: dict):
    data = {
        "name": config_data['event_name'],
        "date": config_data['event_date_valid'],
        "time": config_data['event_time_valid']
    }

    response = api_create_object[0].patch(f"api/events/{api_create_object[2]}", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_update_event_name_valid(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data["upd_event_name"]
    }

    response = api_create_object[0].patch(f"api/events/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    updated_name = response_body['result']['name']
    assert updated_name == config_data["upd_event_name"], f"The actual name of the event does not match the expected updated one, expected updated event name: {response_body['name']}"


def test_update_event_date_valid(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "date": config_data["upd_event_date"]
    }

    response = api_create_object[0].patch(f"api/events/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    updated_date = response_body['result']['date']
    assert updated_date == config_data["upd_event_date"], f"The actual name of the event does not match the expected updated one, expected updated event name: {response_body['name']}"


def test_update_event_time_valid(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "time": config_data["upd_event_time"]
    }

    response = api_create_object[0].patch(f"api/events/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    updated_time = response_body['result']['time']
    assert updated_time == config_data["upd_event_time"], f"The actual name of the event does not match the expected updated one, expected updated event name: {response_body['name']}"


def test_update_event_with_empty_name(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": ""
    }

    response = api_create_object[0].patch(f"api/events/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_update_with_empty_date_name_time_event'] in response_body['message'], f"Expected error message {config_data['error_message_update_with_empty_date_name_time_event']} in response, but got: {response_body['message']}"


def test_update_event_with_empty_date(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "date": ""
    }

    response = api_create_object[0].patch(f"api/events/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_update_with_empty_date_name_time_event'] in response_body['message'], f"Expected error message {config_data['error_message_update_with_empty_date_name_time_event']} in response, but got: {response_body['message']}"


def test_update_event_with_empty_time(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "time": ""
    }

    response = api_create_object[0].patch(f"api/events/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_update_with_empty_date_name_time_event'] in response_body['message'], f"Expected error message {config_data['error_message_update_with_empty_date_name_time_event']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    "18.12.2024",
    "18 12 2024",
    "18/12/2024",
    "20245-12-14",
    "2024-123-14",
    "2024-12-143",
    "18 december 2024 year",
    "18-12-2024"
])
def test_update_event_with_invalid_date(api_create_object, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "date": test_input
    }

    response = api_create_object[0].patch(f"api/events/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_with_invalid_date_event'] in response_body['message'], f"Expected error message {config_data['error_message_with_invalid_date_event']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    "00-00",
    "0:0",
    "00/00",
    "000:000",
    "12h 30min",
    "00 00"
])
def test_update_event_with_invalid_time(api_create_object, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "time": test_input
    }

    response = api_create_object[0].patch(f"api/events/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_with_invalid_time_event'] in response_body['message'], f"Expected error message {config_data['error_message_with_invalid_time_event']} in response, but got: {response_body['message']}"


def test_update_event_with_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['event_name']
    }

    response = api_create_object[0].patch("api/events?id=33333333", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_update_event_with_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['event_name']
    }

    response = api_create_object[0].patch(f"api/events/{config_data['invalid_event_id']}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_update_event_without_event_id(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['event_name']
    }

    response = api_create_object[0].patch("api/events", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_update_without_id_event'], f"Expected error message {config_data['error_message_update_without_id_event']} in response, but got: {response_body['message']}"


def test_delete_event_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].delete(f"api/events/{api_create_object[2]}")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_delete_event_with_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete("api/events?id=33333333", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_delete_event_with_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete(f"api/events/{config_data['invalid_event_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_delete_event_without_event_id(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete("api/events", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_delete_without_id_event'], f"Expected error message {config_data['error_message_delete_without_id_event']} in response, but got: {response_body['message']}"
