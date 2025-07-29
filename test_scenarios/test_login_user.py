import logging
import pytest


@pytest.mark.parametrize("test_input", [
    " tester@gmail.com",
    "tester@gmail.com ",
    " tester@gmail.com "
])
def test_login_user_with_spaces_in_email(api_login, config_data: dict, test_input):
    data = {
        "email": test_input,
        "password": config_data["password"]
    }

    response = api_login[0].post("api/auth/login", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data['error_message_with_spaces_in_email_auth'] in response_body['message'], f"Expected error message {config_data['error_message_with_spaces_in_email_auth']} in response, but got: {response_body['message']}"


def test_login_user_with_empty_email(api_login, config_data: dict):
    data = {
        "email": "",
        "password": config_data["password"]
    }

    response = api_login[0].post("api/auth/login", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data["error_message_empty_email_field_auth"] in response_body['message'], f"Expected error message {config_data["error_message_empty_email_field_auth"]} in response, but got: {response_body['message']}"


def test_login_user_with_empty_password(api_login, config_data: dict):
    data = {
        "email": config_data["email"],
        "password": ""
    }

    response = api_login[0].post("api/auth/login", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data["error_message_empty_password_field_auth"] in response_body['message'], f"Expected error message {config_data["error_message_empty_password_field_auth"]} in response, but got: {response_body['message']}"


def test_login_user_without_email(api_login, config_data: dict):
    data = {
        "password": config_data["password"]
    }

    response = api_login[0].post("api/auth/login", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data["error_message_without_email_field_auth"] in response_body['message'], f"Expected error message {config_data["error_message_without_email_field_auth"]} in response, but got: {response_body['message']}"


def test_login_user_without_password(api_login, config_data: dict):
    data = {
        "email": config_data["email"]
    }

    response = api_login[0].post("api/auth/login", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data["error_message_without_password_field_auth"] in response_body['message'], f"Expected error message {config_data["error_message_without_password_field_auth"]} in response, but got: {response_body['message']}"


def test_login_user_with_invalid_password(api_login, config_data: dict):
    data = {
        "email": config_data["email"],
        "password": config_data['invalid_password']
    }

    response = api_login[0].post("api/auth/login", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data["error_message_with_invalid_password_auth"] in response_body['message'], f"Expected error message {config_data["error_message_with_invalid_password_auth"]} in response, but got: {response_body['message']}"


def test_get_profile_data_valid(api_login, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_login[1]}"
    }
    response = api_login[0].get("api/user/profile", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200"
    assert response_body['email'] == config_data["email"], f"The actual email does not match the expected one, expected email: {response_body['email']}"
