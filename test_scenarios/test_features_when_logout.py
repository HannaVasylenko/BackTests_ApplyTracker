import logging


def test_add_social_link_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    data = {
        "name": config_data["name_example"],
        "link": config_data['link_example']
    }

    response = api_add_features_for_logout_verification[0].post("api/user/socials", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_update_social_link_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    data = {
        "name": config_data["linkedin_social_link"],
        "link": config_data['ln_link_valid']
    }

    response = api_add_features_for_logout_verification[0].patch(f"api/user/socials/{api_add_features_for_logout_verification[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_delete_social_link_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].delete(f"api/user/socials/{api_add_features_for_logout_verification[2]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_add_note_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    data = {
        "name": config_data["note_name"],
        "text": config_data['note_text']

    }

    response = api_add_features_for_logout_verification[0].post("api/notes", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_get_list_notes_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].get("api/notes", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_get_note_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].get(f"api/notes/{api_add_features_for_logout_verification[3]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_update_note_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    data = {
        "name": config_data["note_name"],
        "text": config_data['note_text']
    }

    response = api_add_features_for_logout_verification[0].patch(f"api/notes/{api_add_features_for_logout_verification[3]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_delete_note_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].delete(f"api/notes/{api_add_features_for_logout_verification[3]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_add_resume_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    data = {
        "name": config_data['name_resume'],
        "link": config_data['link_example']
    }

    response = api_add_features_for_logout_verification[0].post("api/resumes", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_get_list_resumes_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].get("api/resumes", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_get_resume_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].get(f"api/resumes/{api_add_features_for_logout_verification[4]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_update_resume_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    data = {
        "name": config_data['name_resume'],
        "link": config_data['link_example']
    }

    response = api_add_features_for_logout_verification[0].patch(f"api/resumes/{api_add_features_for_logout_verification[4]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_delete_resume_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].delete(f"api/resumes/{api_add_features_for_logout_verification[4]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_add_cover_letter_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    data = {
        "name": config_data['cover_letter_name'],
        "text": config_data['cover_letter_text']
    }

    response = api_add_features_for_logout_verification[0].post("api/cover-letter", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_get_list_cover_letters_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].get("api/cover-letter", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_get_cover_letter_by_id_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].get(f"api/cover-letter/{api_add_features_for_logout_verification[5]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_update_cover_letter_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    data = {
        "name": config_data['cover_letter_name'],
        "text": config_data['cover_letter_text']
    }

    response = api_add_features_for_logout_verification[0].patch(f"api/cover-letter/{api_add_features_for_logout_verification[5]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_delete_cover_letter_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].delete(f"api/cover-letter/{api_add_features_for_logout_verification[5]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_add_project_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    data = {
        "name": config_data['project_name'],
        "link": config_data['githubLink_valid'],
        "technologies": "string",
        "description": "string"
    }

    response = api_add_features_for_logout_verification[0].post("api/projects", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_get_list_projects_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].get("api/projects", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_get_project_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].get(f"api/projects/{api_add_features_for_logout_verification[6]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_update_project_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    data = {
        "name": config_data['project_name']
    }

    response = api_add_features_for_logout_verification[0].patch(f"api/projects/{api_add_features_for_logout_verification[6]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_delete_project_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].delete(f"api/projects/{api_add_features_for_logout_verification[6]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_add_event_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    data = {
        "name": config_data['event_name'],
        "date": config_data['event_date_valid'],
        "time": config_data['event_time_valid']
    }

    response = api_add_features_for_logout_verification[0].post("api/events", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_get_list_events_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].get("api/events", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_get_event_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].get(f"api/events/{api_add_features_for_logout_verification[7]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_update_event_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    data = {
        "name": config_data['event_name']
    }

    response = api_add_features_for_logout_verification[0].patch(f"api/events/{api_add_features_for_logout_verification[7]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_delete_event_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].delete(f"api/events/{api_add_features_for_logout_verification[7]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_add_vacancy_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    data = {
        "vacancy": config_data['vacancy'],
        "link": config_data['link_example'],
        "company": config_data['company'],
        "location": config_data['location'],
        "work_type": config_data['work_type_example'],
    }

    response = api_add_features_for_logout_verification[0].post("api/vacancies", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_get_list_vacancies_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].get("api/vacancies", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_get_vacancy_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].get(f"api/vacancies/{api_add_features_for_logout_verification[9]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_update_vacancy_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    data = {
        "vacancy": config_data['vacancy'],
        "link": config_data['link_example'],
        "company": config_data['company'],
        "location": config_data['location'],
        "work_type": config_data['work_type_example'],
    }

    response = api_add_features_for_logout_verification[0].patch(f"api/vacancies/{api_add_features_for_logout_verification[9]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_archive_vacancy_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].patch(f"api/vacancies/{api_add_features_for_logout_verification[9]}/archive", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_delete_vacancy_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].delete(f"api/vacancies/{api_add_features_for_logout_verification[9]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_add_prediction_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    data = {
        "textUk": config_data['textUk'],
        "textEn": config_data['textEn']
    }

    response = api_add_features_for_logout_verification[0].post("api/predictions", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_get_list_predictions_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].get("api/predictions", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_get_prediction_daily_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].get("api/predictions/daily", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_update_prediction_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    data = {
        "textUk": config_data['textUk'],
        "textEn": config_data['textEn']
    }

    response = api_add_features_for_logout_verification[0].patch(f"api/predictions/{api_add_features_for_logout_verification[8]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


def test_delete_prediction_when_logout(api_add_features_for_logout_verification, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
    }

    response = api_add_features_for_logout_verification[0].delete(f"api/predictions/{api_add_features_for_logout_verification[8]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"


# def test_seed_predictions_when_logout(api_add_features_for_logout_verification, config_data: dict):
#     headers = {
#         "Authorization": f"Bearer {api_add_features_for_logout_verification[1]}"
#     }
#
#     response = api_add_features_for_logout_verification[0].post("api/predictions/seed", headers=headers)
#     status = response.status
#     response_body = response.json()
#     logging.info(f"Response: {response_body}")
#     assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
#     assert response_body['message'] == config_data['error_message_when_logout_auth'], f"Expected error message {config_data['error_message_when_logout_auth']} in response, but got: {response_body['message']}"
