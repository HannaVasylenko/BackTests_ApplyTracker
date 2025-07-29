import logging


def test_reset_password_with_invalid_token(api_reset_password, config_data: dict):
    data = {
        "password": config_data['password'],
        "token": config_data['invalid_token']
    }

    response = api_reset_password[0].post("api/auth/reset-password", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401"
    assert response_body['message'] == config_data["error_message_reset_password_with_invalid_token_auth"], f"Expected error message {config_data["error_message_reset_password_with_invalid_token_auth"]} in response, but got: {response_body['message']}"


def test_reset_password_with_invalid_password(api_reset_password, config_data: dict):
    data = {
        "password": config_data['invalid_password'],
        "token": api_reset_password[2]
    }

    response = api_reset_password[0].post("api/auth/reset-password", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data["error_message_with_invalid_password_auth"] in response_body['message'], f"Expected error message {config_data["error_message_with_invalid_password_auth"]} in response, but got: {response_body['message']}"


def test_reset_password_valid(api_reset_password, config_data: dict):
    data = {
        "password": config_data['new_password'],
        "token": api_reset_password[2]
    }

    response = api_reset_password[0].post("api/auth/reset-password", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 201, f"Expected status 201"
    assert response_body['message'] == config_data["success_message_reset_password_auth"], f"Expected error message {config_data["success_message_reset_password_auth"]} in response, but got: {response_body['message']}"
