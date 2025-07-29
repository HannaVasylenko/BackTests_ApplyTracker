import logging
import pytest


@pytest.fixture(scope="session")
def get_elements_url_and_request_body(config_data: dict):
    data = {
        "name": f"{config_data['name_example']}",
        "link": f"{config_data['link_example']}"
    }
    return ['api/user/socials', data]


def test_add_social_link_unauthorized(api_create_social_link, config_data: dict):
    data = {
        "name": config_data["name_example"],
        "link": config_data['link_example']
    }

    response = api_create_social_link[0].post("api/user/socials", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


@pytest.mark.skip(reason="Do not check")
def test_add_social_link_with_invalid_link_valid(api_create_social_link, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_social_link[1]}"
    }

    data = {
        "name": config_data["name_example"],
        "link": config_data['link_without_http']
    }

    response = api_create_social_link[0].post("api/user/socials", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert response_body['message'] == config_data["error_message_when_add_invalid_link_in_profile"], f"Expected error message {config_data["error_message_when_add_invalid_link_in_profile"]} in response, but got: {response_body['message']}"


def test_update_social_link_unauthorized(api_create_social_link, config_data: dict):
    data = {
        "name": config_data["name_example"],
        "link": config_data['link_example_2']
    }

    response = api_create_social_link[0].patch(f"api/user/socials/{api_create_social_link[2]}", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_update_social_link_with_invalid_id_as_parameter(api_create_social_link, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_social_link[1]}"
    }

    data = {
        "name": config_data["linkedin_social_link"],
        "link": config_data['ln_link_valid']
    }

    response = api_create_social_link[0].patch(f"api/user/socials?id=8888888888", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_update_social_link_with_invalid_id_as_url(api_create_social_link, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_social_link[1]}"
    }

    data = {
        "name": config_data["linkedin_social_link"],
        "link": config_data['ln_link_valid']
    }

    response = api_create_social_link[0].patch(f"api/user/socials/{config_data['invalid_social_link_id']}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404"
    assert response_body['message'] == config_data['error_message_when_update_social_link_with_invalid_id_url'], f"Expected error message {config_data['error_message_when_update_social_link_with_invalid_id_url']} in response, but got: {response_body['message']}"


def test_update_social_link_without_id(api_create_social_link, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_social_link[1]}"
    }

    data = {
        "name": config_data["linkedin_social_link"],
        "link": config_data['ln_link_valid']
    }

    response = api_create_social_link[0].patch(f"api/user/socials", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404"
    assert response_body['message'] == config_data['error_message_when_update_social_link_without_id'], f"Expected error message {config_data['error_message_when_update_social_link_without_id']} in response, but got: {response_body['message']}"


def test_update_social_link_valid(api_create_social_link, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_social_link[1]}"
    }

    data = {
        "name": config_data["linkedin_social_link"],
        "link": config_data['ln_link_valid']
    }

    response = api_create_social_link[0].patch(f"api/user/socials/{api_create_social_link[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200"
    assert response_body['message'] == config_data["success_message_update_social_link"], f"Expected error message {config_data["success_message_update_social_link"]} in response, but got: {response_body['message']}"


def test_delete_social_link_unauthorized(api_create_social_link, config_data: dict):
    response = api_create_social_link[0].delete(f"api/user/socials/{api_create_social_link[2]}")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_delete_social_link_with_invalid_id_as_parameter(api_create_social_link, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_social_link[1]}"
    }

    response = api_create_social_link[0].delete(f"api/user/socials?id=8888888888", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_delete_social_link_with_invalid_id_as_url(api_create_social_link, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_social_link[1]}"
    }

    response = api_create_social_link[0].delete(f"api/user/socials/{config_data['invalid_social_link_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404"
    assert response_body['message'] == config_data['error_message_when_delete_social_link_with_invalid_id_url'], f"Expected error message {config_data['error_message_when_delete_social_link_with_invalid_id_url']} in response, but got: {response_body['message']}"


def test_delete_social_link_without_id(api_create_social_link, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_social_link[1]}"
    }

    response = api_create_social_link[0].delete(f"api/user/socials", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404"
    assert response_body['message'] == config_data['error_message_when_delete_social_link_without_id'], f"Expected error message {config_data['error_message_when_delete_social_link_without_id']} in response, but got: {response_body['message']}"
