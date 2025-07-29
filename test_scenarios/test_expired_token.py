import logging


def test_register_logout_login_with_expired_token(api_expired_token_when_register_logout_login, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_expired_token_when_register_logout_login[1]}"
    }
    response = api_expired_token_when_register_logout_login[0].get("api/user/profile", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401"
    assert response_body['message'] == config_data["error_message_when_logout_auth"], f"Expected error message {config_data["error_message_when_logout_auth"]} in response, but got: {response_body['message']}"


def test_login_logout_login_with_expired_token(api_expired_token_when_login_logout_login, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_expired_token_when_login_logout_login[1]}"
    }
    response = api_expired_token_when_login_logout_login[0].get("api/user/profile", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401"
    assert response_body['message'] == config_data["error_message_when_logout_auth"], f"Expected error message {config_data["error_message_when_logout_auth"]} in response, but got: {response_body['message']}"


def test_refresh_token(api_expired_token_when_refresh, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_expired_token_when_refresh[1]}"
    }
    response = api_expired_token_when_refresh[0].get("api/user/profile", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401"
    assert response_body['message'] == config_data["error_message_unauthorized"], f"Expected error message {config_data["error_message_unauthorized"]} in response, but got: {response_body['message']}"
