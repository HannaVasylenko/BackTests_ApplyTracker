import logging


def test_update_user_when_logout(api_for_auth_when_logout, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_for_auth_when_logout[1]}"
    }

    data = {
        "phone": config_data["valid_phone"],
        "socials": [
            {
                "name": config_data["linkedin_social_link"],
                "link": config_data["ln_link_valid"]
            }
        ]
    }

    response = api_for_auth_when_logout[0].patch(f"api/user/update", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_get_profile_data_when_logout(api_for_auth_when_logout, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_for_auth_when_logout[1]}"
    }
    response = api_for_auth_when_logout[0].get("api/user/profile", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_delete_user_when_logout(api_for_auth_when_logout, config_data: dict): # response 1
    headers = {
        "Authorization": f"Bearer {api_for_auth_when_logout[1]}"
    }

    response = api_for_auth_when_logout[0].delete(f"api/user/", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"
