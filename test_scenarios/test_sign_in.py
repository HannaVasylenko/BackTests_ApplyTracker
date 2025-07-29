import logging
import pytest


@pytest.mark.parametrize("test_input", [
    " tester@gmail.com",
    "tester@gmail.com ",
    " tester@gmail.com "
])
def test_sign_in_user_with_spaces_in_email(api_sign_in, config_data: dict, test_input):
    data = {
        "email": test_input,
        "password": config_data["password"]
    }

    response = api_sign_in[0].post("api/auth/register", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data['error_message_with_spaces_in_email_auth'] in response_body['message'], f"Expected error message {config_data['error_message_with_spaces_in_email_auth']} in response, but got: {response_body['message']}"


def test_sign_in_user_with_empty_email(api_sign_in, config_data: dict):
    data = {
        "email": "",
        "password": config_data["password"]
    }

    response = api_sign_in[0].post("api/auth/register", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data["error_message_empty_email_field_auth"] in response_body['message'], f"Expected error message {config_data["error_message_empty_email_field_auth"]} in response, but got: {response_body['message']}"


def test_sign_in_user_with_empty_password(api_sign_in, config_data: dict):
    data = {
        "email": config_data["email"],
        "password": ""
    }

    response = api_sign_in[0].post("api/auth/register", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data["error_message_empty_password_field_auth"] in response_body['message'], f"Expected error message {config_data["error_message_empty_password_field_auth"]} in response, but got: {response_body['message']}"


def test_sign_in_user_without_email(api_sign_in, config_data: dict):
    data = {
        "password": config_data["password"]
    }

    response = api_sign_in[0].post("api/auth/register", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data["error_message_without_email_field_auth"] in response_body['message'], f"Expected error message {config_data["error_message_without_email_field_auth"]} in response, but got: {response_body['message']}"


def test_sign_in_user_without_password(api_sign_in, config_data: dict):
    data = {
        "email": config_data["email"]
    }

    response = api_sign_in[0].post("api/auth/register", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data["error_message_without_password_field_auth"] in response_body['message'], f"Expected error message {config_data["error_message_without_password_field_auth"]} in response, but got: {response_body['message']}"


def test_sign_in_user_with_invalid_password(api_sign_in, config_data: dict):
    data = {
        "email": config_data["email"],
        "password": config_data['invalid_password']
    }

    response = api_sign_in[0].post("api/auth/register", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data["error_message_with_invalid_password_auth"] in response_body['message'], f"Expected error message {config_data["error_message_with_invalid_password_auth"]} in response, but got: {response_body['message']}"


def test_sign_in_user_with_already_registered_email(api_sign_in, config_data: dict):
    data = {
        "email": config_data["email"],
        "password": config_data["password"]
    }

    response = api_sign_in[0].post("api/auth/register", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 409, f"Expected status 409"
    assert response_body['message'] == config_data["error_message_already_registered_email_auth"], f"Expected error message {config_data["error_message_already_registered_email_auth"]} in response, but got: {response_body['message']}"
