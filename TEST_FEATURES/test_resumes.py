import logging
import pytest


@pytest.fixture(scope="session")
def get_elements_url_and_request_body(config_data: dict):
    data = {
        "name": f"{config_data['name_resume']}",
        "link": f"{config_data['link_example']}"
    }
    return ['api/resumes', data]


def test_add_resume_unauthorized(api_create_object, config_data: dict):
    data = {
        "name": config_data['name_resume'],
        "link": config_data['link_example']
    }

    response = api_create_object[0].post("api/resumes", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    " https://demoqa.com/",
    "https://demoqa.com/ ",
    " https://demoqa.com/ "
])
def test_add_resume_with_spaces_in_link(api_create_object, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data["name_resume"],
        "link": test_input
    }

    response = api_create_object[0].post("api/resumes", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_and_update_with_space_in_link_resume'] in response_body['message'], f"Expected error message {config_data['error_message_add_and_update_with_space_in_link_resume']} in response, but got: {response_body['message']}"


def test_add_resume_with_empty_name(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": "",
        "link": config_data['link_example']
    }

    response = api_create_object[0].post("api/resumes", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_with_empty_name_resume'] in response_body['message'], f"Expected error message {config_data['error_message_add_with_empty_name_resume']} in response, but got: {response_body['message']}"


def test_add_resume_with_empty_link(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['name_resume'],
        "link": ""
    }

    response = api_create_object[0].post("api/resumes", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_with_empty_link_resume'] in response_body['message'], f"Expected error message {config_data['error_message_add_with_empty_link_resume']} in response, but got: {response_body['message']}"


def test_add_resume_without_name(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "link": config_data['link_example']
    }

    response = api_create_object[0].post("api/resumes", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_without_name_resume'] in response_body['message'], f"Expected error message {config_data['error_message_add_without_name_resume']} in response, but got: {response_body['message']}"


def test_add_resume_without_link(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['name_resume']
    }

    response = api_create_object[0].post("api/resumes", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_without_link_resume'] in response_body['message'], f"Expected error message {config_data['error_message_add_without_link_resume']} in response, but got: {response_body['message']}"


def test_add_resume_without_https_in_link(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data["name_resume"],
        "link": config_data['link_without_http']
    }

    response = api_create_object[0].post("api/resumes", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_without_https_in_link_resume'] in response_body['message'], f"Expected error message {config_data['error_message_add_without_https_in_link_resume']} in response, but got: {response_body['message']}"


def test_get_list_resumes_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].get("api/resumes")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_get_list_resumes_valid(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get("api/resumes", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"


def test_get_resume_by_id_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].get(f"api/resumes/{api_create_object[2]}")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_get_resume_by_id_valid(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get(f"api/resumes/{api_create_object[2]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    assert response_body['name'] == config_data["name_resume"], f"The actual name of the resume does not match the expected one, expected resume name: {response_body['name']}"


def test_get_resume_by_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get("api/resumes?id=12345", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_get_resume_by_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].get(f"api/resumes/{config_data['invalid_resume_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_update_resume_unauthorized(api_create_object, config_data: dict):
    data = {
        "name": config_data['name_resume'],
        "link": config_data['link_example']
    }

    response = api_create_object[0].patch(f"api/resumes/{api_create_object[2]}", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    "name",
    "link"
])
def test_update_resume_valid(api_create_object, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        test_input: config_data["upd_cv_value"]
    }

    response = api_create_object[0].patch(f"api/resumes/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    assert response_body[test_input] == config_data["upd_cv_value"], f"The actual updated name of the resume does not match the expected one, expected updated resume name: {response_body['name']}"


def test_update_resume_with_empty_name(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": ""
    }

    response = api_create_object[0].patch(f"api/resumes/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_update_with_empty_name_or_link_resume'] in response_body['message'], f"Expected error message {config_data['error_message_update_with_empty_name_or_link_resume']} in response, but got: {response_body['message']}"


def test_update_resume_with_empty_link(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "link": ""
    }

    response = api_create_object[0].patch(f"api/resumes/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_update_with_empty_name_or_link_resume'] in response_body['message'], f"Expected error message {config_data['error_message_update_with_empty_name_or_link_resume']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    " https://demoqa.com/",
    "https://demoqa.com/ ",
    " https://demoqa.com/ "
])
def test_update_resume_with_spaces_in_link(api_create_object, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "link": test_input
    }

    response = api_create_object[0].patch(f"api/resumes/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_and_update_with_space_in_link_resume'] in response_body['message'], f"Expected error message {config_data['error_message_add_and_update_with_space_in_link_resume']} in response, but got: {response_body['message']}"


def test_update_resume_without_https_in_link(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "link": config_data['link_without_http']
    }

    response = api_create_object[0].patch(f"api/resumes/{api_create_object[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}" #200
    assert config_data['error_message_update_without_https_in_link_resume'] in response_body['message'], f"Expected error message {config_data['error_message_update_without_https_in_link_resume']} in response, but got: {response_body['message']}"


def test_update_resume_with_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['name_resume'],
        "link": config_data['link_example']
    }

    response = api_create_object[0].patch("api/resumes?id=12345", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_update_resume_with_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['name_resume'],
        "link": config_data['link_example']
    }

    response = api_create_object[0].patch(f"api/resumes/{config_data['invalid_resume_id']}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_update_resume_without_resume_id(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    data = {
        "name": config_data['name_resume'],
        "link": config_data['link_example']
    }

    response = api_create_object[0].patch(f"api/resumes", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_update_without_id_resume'], f"Expected error message {config_data['error_message_update_without_id_resume']} in response, but got: {response_body['message']}"


def test_delete_resume_unauthorized(api_create_object, config_data: dict):
    response = api_create_object[0].delete(f"api/resumes/{api_create_object[2]}")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_delete_resume_with_invalid_id_as_parameter(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete("api/resumes?id=12345", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_delete_resume_with_invalid_id_as_url(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete(f"api/resumes/{config_data['invalid_resume_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_delete_resume_without_resume_id(api_create_object, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_object[1]}"
    }

    response = api_create_object[0].delete(f"api/resumes", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_delete_without_id_resume'], f"Expected error message {config_data['error_message_delete_without_id_resume']} in response, but got: {response_body['message']}"
