import logging
import pytest


@pytest.fixture(scope="session")
def get_elements_url_and_request_body(config_data: dict):
    data = {
        "name": f"{config_data['project_name']}",
        "link": f"{config_data['githubLink_valid']}",
        "technologies": "string",
        "description": "string"
    }
    return ['api/projects', data]


def test_add_project_unauthorized(api_create_object, config_data: dict):
    data = {
        "name": config_data['project_name'],
        "link": config_data['githubLink_valid'],
        "technologies": "string",
        "description": "string"
    }

    response = api_create_object[0].post("api/projects", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    " https://github.com/microsoft/playwright-python.git",
    "https://github.com/microsoft/playwright-python.git ",
    " https://github.com/microsoft/playwright-python.git "
])
def test_add_project_with_space_in_link(api_create_object, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['project_name'],
        "link": test_input,
        "technologies": "string",
        "description": "string"
    }

    response = api_create_object[0].post("api/projects", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_and_update_with_space_in_project_link'] in response_body['message'], f"Expected error message {config_data['error_message_add_and_update_with_space_in_project_link']} in response, but got: {response_body['message']}"


def test_add_project_without_https_in_link(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['project_name'],
        "link": config_data['link_without_http'],
        "technologies": "string",
        "description": "string"
    }

    response = api_create_object[0].post("api/projects", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_and_update_without_http_in_link'] in response_body['message'], f"Expected error message {config_data['error_message_add_and_update_without_http_in_link']} in response, but got: {response_body['message']}"


def test_add_project_without_github_com_in_link(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['project_name'],
        "link": config_data['invalid_github_link'],
        "technologies": "string",
        "description": "string"
    }

    response = api_create_object[0].post("api/projects", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_without_github_com_in_link'] in response_body['message'], f"Expected error message {config_data['error_message_without_github_com_in_link']} in response, but got: {response_body['message']}"


def test_add_project_without_name(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "link": config_data['githubLink_valid'],
        "technologies": "string",
        "description": "string"
    }

    response = api_create_object[0].post("api/projects", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_without_name_project'] in response_body['message'], f"Expected error message {config_data['error_message_add_without_name_project']} in response, but got: {response_body['message']}"


def test_add_project_without_link(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['project_name'],
        "technologies": "string",
        "description": "string"
    }

    response = api_create_object[0].post("api/projects", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_without_link_project'] in response_body['message'], f"Expected error message {config_data['error_message_add_without_link_project']} in response, but got: {response_body['message']}"


def test_add_project_with_empty_name(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": "",
        "link": config_data['githubLink_valid'],
        "technologies": "string",
        "description": "string"
    }

    response = api_create_object[0].post("api/projects", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_with_empty_name_project'] in response_body['message'], f"Expected error message {config_data['error_message_add_with_empty_name_project']} in response, but got: {response_body['message']}"


def test_add_project_with_empty_link(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['project_name'],
        "link": "",
        "technologies": "string",
        "description": "string"
    }

    response = api_create_object[0].post("api/projects", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_with_empty_link_project'] in response_body['message'], f"Expected error message {config_data['error_message_add_with_empty_link_project']} in response, but got: {response_body['message']}"


def test_get_list_projects_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].get("api/projects")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_get_list_projects_valid(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get("api/projects", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"


def test_get_project_by_id_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].get(f"api/projects/{config_data['project_id']}")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_get_project_by_id_valid(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get(f"api/projects/{api_create_object[2]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    assert response_body['name'] == config_data["project_name"], f"The actual name of the project does not match the expected one, expected project name: {response_body['name']}"


def test_get_project_by_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get("api/projects?id=11111", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_get_project_by_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get(f"api/projects/{config_data['invalid_project_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_update_project_unauthorized(api_create_object, config_data: dict):
    data = {
        "name": config_data['project_name']
    }

    response = api_create_object[0].patch(f"api/projects/{api_create_object[2]}", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    "name",
    "link",
    "technologies",
    "description"
])
def test_update_project_valid(api_create_object, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        test_input: config_data["upd_project_value"]
    }

    response = api_create_object[0].patch(f"api/projects/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    updated_name = response_body['result'][test_input]
    assert updated_name == config_data["upd_project_value"], f"Expected updated note name: {config_data['upd_note_name']}, but got: {updated_name}. Response: {response_body}"


def test_update_project_with_empty_name(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": ""
    }

    response = api_create_object[0].patch(f"api/projects/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_update_with_empty_name_githublink_liveprojectlink_project'] in response_body['message'], f"Expected error message {config_data['error_message_update_with_empty_name_githublink_liveprojectlink_project']} in response, but got: {response_body['message']}"


def test_update_project_with_empty_link(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "link": ""
    }

    response = api_create_object[0].patch(f"api/projects/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_update_with_empty_name_githublink_liveprojectlink_project'] in response_body['message'], f"Expected error message {config_data['error_message_update_with_empty_name_githublink_liveprojectlink_project']} in response, but got: {response_body['message']}"


def test_update_project_with_empty_technologies(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "technologies": ""
    }

    response = api_create_object[0].patch(f"api/projects/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_with_empty_technologies'] in response_body['message'], f"Expected error message {config_data['error_message_add_with_empty_technologies']} in response, but got: {response_body['message']}"


def test_update_project_with_empty_description(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "description": ""
    }

    response = api_create_object[0].patch(f"api/projects/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_with_empty_description'] in response_body['message'], f"Expected error message {config_data['error_message_add_with_empty_description']} in response, but got: {response_body['message']}"


def test_update_project_without_https_in_link(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "link": config_data['link_without_http']
    }

    response = api_create_object[0].patch(f"api/projects/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_and_update_without_http_in_link'] in response_body['message'], f"Expected error message {config_data['error_message_add_and_update_without_http_in_link']} in response, but got: {response_body['message']}"


def test_update_project_without_github_com_in_link(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "link": config_data['invalid_github_link']
    }

    response = api_create_object[0].patch(f"api/projects/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_without_github_com_in_link'] in response_body['message'], f"Expected error message {config_data['error_message_without_github_com_in_link']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    " https://github.com/microsoft/playwright-python.git",
    "https://github.com/microsoft/playwright-python.git ",
    " https://github.com/microsoft/playwright-python.git "
])
def test_update_project_with_spaces_in_link(api_create_object, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "link": test_input
    }

    response = api_create_object[0].patch(f"api/projects/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_and_update_with_space_in_project_link'] in response_body['message'], f"Expected error message {config_data['error_message_add_and_update_with_space_in_project_link']} in response, but got: {response_body['message']}"



def test_update_project_with_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['project_name']
    }

    response = api_create_object[0].patch("api/projects?id=11111", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_update_project_with_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['project_name']
    }

    response = api_create_object[0].patch(f"api/projects/{config_data['invalid_project_id']}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_update_project_without_project_id(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['project_name']
    }

    response = api_create_object[0].patch(f"api/projects", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_update_without_id_project'], f"Expected error message {config_data['error_message_update_without_id_project']} in response, but got: {response_body['message']}"


def test_delete_project_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].delete(f"api/projects/{api_create_object[2]}")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_delete_project_with_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete("api/projects?id=11111", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_delete_project_with_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete(f"api/projects/{config_data['invalid_project_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_delete_project_without_project_id(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete(f"api/projects", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_delete_without_id_project'], f"Expected error message {config_data['error_message_delete_without_id_project']} in response, but got: {response_body['message']}"
