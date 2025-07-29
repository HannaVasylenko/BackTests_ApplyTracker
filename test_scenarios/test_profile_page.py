import logging


def test_get_profile_data_unauthorized(api_login_for_profile_tests, config_data: dict):
    response = api_login_for_profile_tests[0].get("api/user/profile")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_get_profile_data_valid(api_login_for_profile_tests, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_login_for_profile_tests[1]}"
    }
    response = api_login_for_profile_tests[0].get("api/user/profile", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200"
    assert response_body['email'] == config_data["email"], f"The actual email does not match the expected one, expected email: {response_body['email']}"


def test_update_user_unauthorized(api_login_for_profile_tests, config_data: dict):
    data = {
        "phone": "+380000000000",
        "socials": [
            {
                "name": "LinkedIn",
                "link": "https://www.linkedin.com/company/baza-trainee-ukraine"
            }
        ]
    }

    response = api_login_for_profile_tests[0].patch(f"api/user/update", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_update_user_with_invalid_email(api_login_for_profile_tests, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_login_for_profile_tests[1]}"
    }

    data = {
        "email": config_data["email_username"]
    }

    response = api_login_for_profile_tests[0].patch(f"api/user/update", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data['error_message_when_update_profile_with_invalid_email'] in response_body['message'], f"Expected error message {config_data['error_message_when_update_profile_with_invalid_email']} in response, but got: {response_body['message']}"


def test_update_user_with_invalid_phone(api_login_for_profile_tests, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_login_for_profile_tests[1]}"
    }

    data = {
        "phone": config_data["invalid_phone"]
    }

    response = api_login_for_profile_tests[0].patch(f"api/user/update", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data['error_message_when_update_profile_with_invalid_phone'] in response_body['message'], f"Expected error message {config_data['error_message_when_update_profile_with_invalid_phone']} in response, but got: {response_body['message']}"


def test_update_user_with_invalid_social_link(api_login_for_profile_tests, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_login_for_profile_tests[1]}"
    }

    data = {
        "socials": [
            {
                "name": config_data["linkedin_social_link"],
                "link": config_data["invalid_linkedIn_social_link"]
            }
        ]
    }

    response = api_login_for_profile_tests[0].patch(f"api/user/update", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400"
    assert config_data['error_message_when_update_profile_with_invalid_ln_social_link'] in response_body['message'], f"Expected error message {config_data['error_message_when_update_profile_with_invalid_ln_social_link']} in response, but got: {response_body['message']}"


def test_update_user_valid(api_login_for_profile_tests, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_login_for_profile_tests[1]}"
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

    response = api_login_for_profile_tests[0].patch(f"api/user/update", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200"
    assert response_body['message'] == config_data["success_message_update_user"], f"Expected error message {config_data["success_message_update_user"]} in response, but got: {response_body['message']}"


def test_delete_user_unauthorized(api_login_for_profile_tests, config_data: dict):
    response = api_login_for_profile_tests[0].delete(f"api/user")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"
