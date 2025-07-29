import logging


def test_refresh_with_invalid_token(api_refresh_token, config_data: dict):
    data = {
        "refresh_token": config_data['invalid_token']
    }

    response = api_refresh_token[0].post("api/auth/refresh", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401" # 500
    assert response_body['message'] == config_data["error_message_refresh_with_invalid_token_auth"], f"Expected error message {config_data["error_message_refresh_with_invalid_token_auth"]} in response, but got: {response_body['message']}"


def test_get_profile_data_valid(api_refresh_token, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_refresh_token[1]}"
    }
    response = api_refresh_token[0].get("api/user/profile", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200"
    assert response_body['email'] == config_data["email"], f"The actual email does not match the expected one, expected email: {response_body['email']}"
