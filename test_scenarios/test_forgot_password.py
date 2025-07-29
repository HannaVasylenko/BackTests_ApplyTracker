import logging
import pytest


@pytest.mark.parametrize("test_input", [
    " tester@gmail.com",
    "tester@gmail.com ",
    " tester@gmail.com "
])
def test_forgot_password_with_spaces_in_email(api_forgot_password, config_data: dict, test_input):
    data = {
        "email": test_input
    }

    response = api_forgot_password[0].post("api/auth/forgot-password", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data['error_message_with_spaces_in_email_auth'] in response_body['message'], f"Expected error message {config_data['error_message_with_spaces_in_email_auth']} in response, but got: {response_body['message']}"


def test_forgot_password_with_unregistered_email(api_forgot_password, config_data: dict):
    data = {
        "email": config_data['invalid_email']
    }

    response = api_forgot_password[0].post("api/auth/forgot-password", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404"
    assert response_body['message'] == config_data["error_message_forgot_password_with_invalid_email_auth"], f"Expected error message {config_data["error_message_forgot_password_with_invalid_email_auth"]} in response, but got: {response_body['message']}"
