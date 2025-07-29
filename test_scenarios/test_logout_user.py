import logging


def test_logout_user_unauthorized(api_logout, config_data: dict):
    response = api_logout[0].post("api/auth/logout")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401"
    assert response_body['message'] == config_data["error_message_unauthorized"], f"Expected error message {config_data["error_message_unauthorized"]} in response, but got: {response_body['message']}"


def test_logout_user_valid(api_logout, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_logout[1]}"
    }

    response = api_logout[0].post("api/auth/logout", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200"
    assert response_body['message'] == config_data['success_message_logout_user_auth'], f"Expected error message {config_data['success_message_logout_user_auth']} in response, but got: {response_body['message']}"


def test_get_profile_data_when_logout(api_logout, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_logout[1]}"
    }
    response = api_logout[0].get("api/user/profile", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"
