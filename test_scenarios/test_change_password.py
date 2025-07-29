import logging


def test_change_password_profile_unauthorized(api_change_password, config_data: dict):
    data = {
        "previous_password": config_data["password"],
        "new_password": config_data["new_password"]
    }

    response = api_change_password[0].post("api/user/change-password", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401"
    assert response_body['message'] == config_data["error_message_unauthorized"], f"Expected error message {config_data["error_message_unauthorized"]} in response, but got: {response_body['message']}"


def test_change_password_profile_with_invalid_previous_password(api_change_password, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_change_password[1]}"
    }

    data = {
        "previous_password": config_data['previous_password'],
        "new_password": config_data["new_password"]
    }

    response = api_change_password[0].post("api/user/change-password", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401"
    assert response_body['message'] == config_data["error_message_change_password_with_invalid_previous_password_auth"], f"Expected error message {config_data["error_message_change_password_with_invalid_previous_password_auth"]} in response, but got: {response_body['message']}"


def test_change_password_profile_valid(api_change_password, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_change_password[1]}"
    }

    data = {
        "previous_password": config_data["password"],
        "new_password": config_data["new_password"]
    }

    response = api_change_password[0].post("api/user/change-password", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200"
    assert response_body['message'] == config_data["success_message_change_password_auth"], f"Expected error message {config_data["success_message_change_password_auth"]} in response, but got: {response_body['message']}"
