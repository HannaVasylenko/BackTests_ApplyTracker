import logging
import pytest


@pytest.fixture(scope="session")
def get_elements_url_and_request_body(config_data: dict):
    data = {
        "vacancy": f"{config_data['vacancy']}",
        "link": f"{config_data['link_example']}",
        "company": f"{config_data['company']}",
        "location": f"{config_data['location']}",
        "work_type": f"{config_data['work_type_example']}"
    }

    return ['api/vacancies', data]

@pytest.fixture(scope="session")
def get_status_data(config_data: dict):
    data = {
        "name": "hr"
    }
    return data


def test_add_vacancy_unauthorized(api_create_vacancy_with_status, config_data: dict):
    data = {
        "vacancy": config_data['vacancy'],
        "link": config_data['link_example'],
        "company": config_data['company'],
        "location": config_data['location'],
        "work_type": config_data['work_type_example']
    }

    response = api_create_vacancy_with_status[0].post("api/vacancies", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    " https://demoqa.com/",
    "https://demoqa.com/ ",
    " https://demoqa.com/ "
])
@pytest.mark.vacancies
def test_add_vacancy_with_spaces_in_link(api_create_vacancy_with_status, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "vacancy": config_data["vacancy"],
        "link": test_input,
        "company": config_data["company"],
        "location": config_data['location'],
        "work_type": config_data['work_type_example']
    }

    response = api_create_vacancy_with_status[0].post("api/vacancies", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_update_with_spaces_in_link_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_update_with_spaces_in_link_vacancy']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    "remote",
    "office",
    "hybrid"
])
def test_add_vacancy_with_work_type_variants(api_create_vacancy_with_status, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "vacancy": config_data["vacancy"],
        "link": config_data['link_example'],
        "company": config_data['company'],
        "location": config_data['location'],
        "work_type": test_input
    }

    response = api_create_vacancy_with_status[0].post("api/vacancies", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 201, f"Expected status 201, but got {status}. Response: {response_body}"
    assert response_body['work_type'] == test_input, f"The actual work_type does not match the expected one, expected work_type: {response_body['work_type']}"


def test_add_vacancy_with_empty_vacancy_name(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "vacancy": "",
        "link": config_data['link_example'],
        "company": config_data['company'],
        "location": config_data['location'],
        "work_type": config_data['work_type_example']
    }

    response = api_create_vacancy_with_status[0].post("api/vacancies", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_and_update_with_empty_name_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_and_update_with_empty_name_vacancy']} in response, but got: {response_body['message']}"


def test_add_vacancy_with_empty_link(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "vacancy": config_data['vacancy'],
        "link": "",
        "company": config_data['company'],
        "location": config_data['location'],
        "work_type": config_data['work_type_example']
    }

    response = api_create_vacancy_with_status[0].post("api/vacancies", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_with_empty_link_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_with_empty_link_vacancy']} in response, but got: {response_body['message']}"


def test_add_vacancy_without_https_in_link(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "vacancy": config_data['vacancy'],
        "link": config_data['link_without_http'],
        "company": config_data['company'],
        "location": config_data['location'],
        "work_type": config_data['work_type_example']
    }

    response = api_create_vacancy_with_status[0].post("api/vacancies", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_without_https_in_link_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_without_https_in_link_vacancy']} in response, but got: {response_body['message']}"


def test_add_vacancy_with_empty_company_name(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "vacancy": config_data['vacancy'],
        "link": config_data['link_example'],
        "company": "",
        "location": config_data['location'],
        "work_type": config_data['work_type_example'],
    }

    response = api_create_vacancy_with_status[0].post("api/vacancies", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_and_update_with_empty_company_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_and_update_with_empty_company_vacancy']} in response, but got: {response_body['message']}"


def test_add_vacancy_with_empty_location(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "vacancy": config_data['vacancy'],
        "link": config_data['link_example'],
        "company": config_data['company'],
        "location": "",
        "work_type": config_data['work_type_example'],
    }

    response = api_create_vacancy_with_status[0].post("api/vacancies", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_and_update_with_empty_location_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_and_update_with_empty_location_vacancy']} in response, but got: {response_body['message']}"


def test_add_vacancy_with_empty_work_type(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "vacancy": config_data['vacancy'],
        "link": config_data['link_example'],
        "company": config_data['company'],
        "location": config_data['location'],
        "work_type": "",
    }

    response = api_create_vacancy_with_status[0].post("api/vacancies", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_and_update_with_empty_work_type_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_and_update_with_empty_work_type_vacancy']} in response, but got: {response_body['message']}"


def test_add_vacancy_without_vacancy_name(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "link": config_data['link_example'],
        "company": config_data['company'],
        "location": config_data['location'],
        "work_type": config_data['work_type_example']
    }

    response = api_create_vacancy_with_status[0].post("api/vacancies", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_without_name_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_without_name_vacancy']} in response, but got: {response_body['message']}"


def test_add_vacancy_without_link(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": config_data['vacancy'],
        "company": config_data['company'],
        "location": config_data['location'],
        "work_type": config_data['work_type_example']
    }

    response = api_create_vacancy_with_status[0].post("api/vacancies", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_without_link_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_without_link_vacancy']} in response, but got: {response_body['message']}"


def test_add_vacancy_without_company_name(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": config_data['vacancy'],
        "link": config_data['link_example'],
        "location": config_data['location'],
        "work_type": config_data['work_type_example']
    }

    response = api_create_vacancy_with_status[0].post("api/vacancies", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_without_company_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_without_company_vacancy']} in response, but got: {response_body['message']}"


def test_add_vacancy_without_location(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": config_data['vacancy'],
        "link": config_data['link_example'],
        "company": config_data['company'],
        "work_type": config_data['work_type_example']
    }

    response = api_create_vacancy_with_status[0].post("api/vacancies", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_without_location_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_without_location_vacancy']} in response, but got: {response_body['message']}"


def test_add_vacancy_without_work_type(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": config_data['vacancy'],
        "link": config_data['link_example'],
        "company": config_data['company'],
        "location": config_data['location']
    }

    response = api_create_vacancy_with_status[0].post("api/vacancies", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_without_work_type_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_without_work_type_vacancy']} in response, but got: {response_body['message']}"


def test_get_list_vacancies_unauthorized(api_create_vacancy_with_status, config_data: dict):
    response = api_create_vacancy_with_status[0].get("api/vacancies")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_get_list_vacancies_valid(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].get("api/vacancies", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"


def test_get_vacancy_by_id_unauthorized(api_create_vacancy_with_status, config_data: dict):
    response = api_create_vacancy_with_status[0].get(f"api/vacancies/{api_create_vacancy_with_status[2]}")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_get_vacancy_by_id_valid(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].get(f"api/vacancies/{api_create_vacancy_with_status[2]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    assert response_body['vacancy'] == config_data["vacancy"], f"The actual vacancy name {config_data["vacancy"]} does not match the expected one, expected vacancy name: {response_body['vacancy']}"
    assert response_body['company'] == config_data["company"], f"The actual company name {config_data["company"]} does not match the expected one, expected company name: {response_body['company']}"


def test_get_vacancy_by_invalid_id_as_parameter(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].get(f"api/vacancies?id=44444", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_get_vacancy_by_invalid_id_as_url(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].get(f"api/vacancies/{config_data['invalid_vacancy_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_update_vacancy_unauthorized(api_create_vacancy_with_status, config_data: dict):
    data = {
        "vacancy": config_data['vacancy'],
        "link": config_data['link_example'],
        "company": config_data['company'],
        "location": config_data['location'],
        "work_type": config_data['work_type_example']
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_update_vacancy_valid(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "vacancy": config_data["upd_vacancy_name"]
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    assert response_body['vacancy'] == config_data["upd_vacancy_name"], f"The actual updated vacancy name {config_data["upd_vacancy_name"]} does not match the expected one, expected updated vacancy name: {response_body['vacancy']}"


@pytest.mark.parametrize("test_input", [
    "remote",
    "office",
    "hybrid"
])
def test_update_vacancy_work_type_variants(api_create_vacancy_with_status, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "work_type": test_input
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    assert response_body['work_type'] == test_input, f"The actual work_type {test_input } does not match the expected one, expected work_type: {response_body['work_type']}"


def test_update_vacancy_with_empty_vacancy_name(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "vacancy": ""
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_and_update_with_empty_name_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_and_update_with_empty_name_vacancy']} in response, but got: {response_body['message']}"


def test_update_vacancy_with_empty_link(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "link": ""
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_update_with_empty_only_link_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_update_with_empty_only_link_vacancy']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    " https://demoqa.com/",
    "https://demoqa.com/ ",
    " https://demoqa.com/ "
])
def test_update_vacancy_with_spaces_in_link(api_create_vacancy_with_status, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "link": test_input
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_update_with_spaces_in_link_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_update_with_spaces_in_link_vacancy']} in response, but got: {response_body['message']}"


def test_update_vacancy_without_https_in_link(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "link": config_data['link_without_http']
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_update_without_https_in_link_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_update_without_https_in_link_vacancy']} in response, but got: {response_body['message']}"


def test_update_vacancy_with_empty_company_name(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "company": ""
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_and_update_with_empty_company_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_and_update_with_empty_company_vacancy']} in response, but got: {response_body['message']}"


def test_update_vacancy_with_empty_location(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "location": ""
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_and_update_with_empty_location_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_and_update_with_empty_location_vacancy']} in response, but got: {response_body['message']}"


def test_update_vacancy_with_empty_work_type(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "work_type": ""
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_add_and_update_with_empty_work_type_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_add_and_update_with_empty_work_type_vacancy']} in response, but got: {response_body['message']}"


def test_update_vacancy_with_invalid_id_as_parameter(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "vacancy": config_data['vacancy'],
        "link": config_data['link_example'],
        "company": config_data['company'],
        "location": config_data['location']
    }

    response = api_create_vacancy_with_status[0].patch("api/vacancies?id=44444", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_update_vacancy_with_invalid_id_as_url(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "vacancy": config_data['vacancy'],
        "link": config_data['link_example'],
        "company": config_data['company'],
        "location": config_data['location']
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{config_data['invalid_vacancy_id']}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_by_invalid_id_as_url'] in response_body['message'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_update_vacancy_without_vacancy_id(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "vacancy": config_data['vacancy'],
        "link": config_data['link_example'],
        "company": config_data['company'],
        "location": config_data['location']
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert config_data['error_message_update_without_id_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_update_without_id_vacancy']} in response, but got: {response_body['message']}"


def test_delete_vacancy_unauthorized(api_create_vacancy_with_status, config_data: dict):
    response = api_create_vacancy_with_status[0].delete(f"api/vacancies/{api_create_vacancy_with_status[2]}")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_delete_vacancy_with_invalid_id_as_parameter(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].delete("api/vacancies?id=44444", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_delete_vacancy_with_invalid_id_as_url(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].delete(f"api/vacancies/{config_data['invalid_vacancy_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_delete_vacancy_without_vacancy_id(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].delete(f"api/vacancies", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_delete_without_id_vacancy'], f"Expected error message {config_data['error_message_delete_without_id_vacancy']} in response, but got: {response_body['message']}"


def test_add_vacancy_status_unauthorized(api_create_vacancy_with_status, config_data: dict):
    data = {
        "name": "hr"
    }

    response = api_create_vacancy_with_status[0].post(f"api/vacancies/{api_create_vacancy_with_status[2]}/status", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_add_vacancy_status_without_vacancy_id(api_create_vacancy_with_status, config_data: dict):
    data = {
        "name": "hr"
    }

    response = api_create_vacancy_with_status[0].post(f"api/vacancies/status", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_add_status_without_id_vacancy'], f"Expected error message {config_data['error_message_add_status_without_id_vacancy']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    "hr",
    "test",
    "tech",
    "offer",
    "saved"
])
def test_add_vacancy_statuses_valid(api_create_vacancy_with_status, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": test_input
    }

    response = api_create_vacancy_with_status[0].post(f"api/vacancies/{api_create_vacancy_with_status[2]}/status", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 201, f"Expected status 201, but got {status}. Response: {response_body}"
    assert any(status['name'] == test_input for status in response_body['statuses'])


@pytest.mark.parametrize("test_input", [
    "SOFT_SKILLS",
    "TECH_SKILLS",
    "ENGLISH",
    "EXPERIENCE",
    "STOPPED",
    "NO_ANSWER",
    "OTHER"
])
def test_add_reject_vacancy_status_valid(api_create_vacancy_with_status, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "reject",
        "rejectReason": test_input
    }

    response = api_create_vacancy_with_status[0].post(f"api/vacancies/{api_create_vacancy_with_status[2]}/status", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 201, f"Expected status 201, but got {status}. Response: {response_body}"


def test_add_reject_vacancy_status_without_rejectreason(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "reject"
    }

    response = api_create_vacancy_with_status[0].post(f"api/vacancies/{api_create_vacancy_with_status[2]}/status", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_add_status_without_rejectreason_vacancy'], f"Expected error message {config_data['error_message_add_status_without_rejectreason_vacancy']} in response, but got: {response_body['message']}"


def test_add_reject_vacancy_status_with_empty_rejectreason(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "reject",
        "rejectReason": ""

    }

    response = api_create_vacancy_with_status[0].post(f"api/vacancies/{api_create_vacancy_with_status[2]}/status", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_add_status_with_empty_rejectreason_vacancy'], f"Expected error message {config_data['error_message_add_status_with_empty_rejectreason_vacancy']} in response, but got: {response_body['message']}"


def test_add_resume_vacancy_status_valid(api_create_vacancy_with_status, config_data: dict):
    resume_id = api_create_vacancy_with_status[4]
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "resume",
        "resumeId": resume_id
    }

    response = api_create_vacancy_with_status[0].post(f"api/vacancies/{api_create_vacancy_with_status[2]}/status", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 201, f"Expected status 201, but got {status}. Response: {response_body}"
    assert any(status['name'] == 'resume' for status in response_body['statuses'])


def test_add_resume_vacancy_status_without_resumeid(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "resume"
    }

    response = api_create_vacancy_with_status[0].post(f"api/vacancies/{api_create_vacancy_with_status[2]}/status", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_add_status_without_resumeid_vacancy'], f"Expected error message {config_data['error_message_add_status_without_resumeid_vacancy']} in response, but got: {response_body['message']}"


def test_add_resume_vacancy_status_with_empty_resumeid(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "resume",
        "resumeId": ""

    }

    response = api_create_vacancy_with_status[0].post(f"api/vacancies/{api_create_vacancy_with_status[2]}/status", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_add_status_with_empty_resumeid_vacancy'], f"Expected error message {config_data['error_message_add_status_with_empty_resumeid_vacancy']} in response, but got: {response_body['message']}"


def test_add_vacancy_status_with_invalid_vacancy_id_as_parameter(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "hr"
    }

    response = api_create_vacancy_with_status[0].post(f"api/vacancies?vacancyId=111/status", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_add_vacancy_status_with_invalid_id_as_url(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "hr"
    }

    response = api_create_vacancy_with_status[0].post(f"api/vacancies/{config_data['invalid_vacancy_id']}/status", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_update_vacancy_status_unauthorized(api_create_vacancy_with_status, config_data: dict):
    data = {
        "name": "hr"
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}/status/{api_create_vacancy_with_status[3]}", data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    "hr",
    "test",
    "tech",
    "offer",
    "saved"
])
def test_update_vacancy_status_valid(api_create_vacancy_with_status, config_data: dict, test_input): # update saved status
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": test_input
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}/status/{api_create_vacancy_with_status[3]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"


def test_update_vacancy_status_to_resume_valid(api_create_vacancy_with_status, config_data: dict):
    resume_id = api_create_vacancy_with_status[4]
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "resume",
        "resumeId": resume_id
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}/status/{api_create_vacancy_with_status[3]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"


def test_update_vacancy_status_to_resume_with_empty_resumeid(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "resume",
        "resumeId": ""
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}/status/{api_create_vacancy_with_status[3]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_update_status_with_empty_resumeid_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_update_status_with_empty_resumeid_vacancy']} in response, but got: {response_body['message']}"


def test_update_vacancy_status_to_resume_without_resumeid(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "resume"
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}/status/{api_create_vacancy_with_status[3]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_update_status_without_resumeid_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_update_status_without_resumeid_vacancy']} in response, but got: {response_body['message']}"


@pytest.mark.parametrize("test_input", [
    "SOFT_SKILLS",
    "TECH_SKILLS",
    "ENGLISH",
    "EXPERIENCE",
    "STOPPED",
    "NO_ANSWER",
    "OTHER"
])
def test_update_vacancy_status_to_reject_valid(api_create_vacancy_with_status, config_data: dict, test_input):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "reject",
        "rejectReason": test_input
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}/status/{api_create_vacancy_with_status[3]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"


def test_update_vacancy_status_to_reject_with_empty_rejectreason(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "reject",
        "rejectReason": ""
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}/status/{api_create_vacancy_with_status[3]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_update_status_with_empty_rejectreason_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_update_status_with_empty_rejectreason_vacancy']} in response, but got: {response_body['message']}"


def test_update_vacancy_status_to_reject_without_rejectreason(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "reject"
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}/status/{api_create_vacancy_with_status[3]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert config_data['error_message_update_status_without_rejectreason_vacancy'] in response_body['message'], f"Expected error message {config_data['error_message_update_status_without_rejectreason_vacancy']} in response, but got: {response_body['message']}"


def test_update_vacancy_status_without_statusid(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "tech"
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}/status", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == f"{config_data['error_message_update_status_without_statusid_vacancy']}/{api_create_vacancy_with_status[2]}/status", f"Expected error message {config_data['error_message_update_status_without_statusid_vacancy']} in response, but got: {response_body['message']}"


def test_update_vacancy_status_with_invalid_status_id_as_parameter(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "hr"
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}/status?statusId=44444", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_update_vacancy_status_with_invalid_status_id_as_url(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "hr"
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}/status/{config_data['invalid_status_id']}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_update_vacancy_status_with_invalid_vacancy_id_as_parameter(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "hr"
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies?vacancyId=111/status/{api_create_vacancy_with_status[3]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_update_vacancy_status_with_invalid_vacancy_id_as_url(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    data = {
        "name": "hr"
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{config_data['invalid_vacancy_id']}/status/{api_create_vacancy_with_status[3]}", headers=headers, data=data)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_delete_vacancy_status_unauthorized(api_create_vacancy_with_status, config_data: dict):
    response = api_create_vacancy_with_status[0].delete(f"api/vacancies/{api_create_vacancy_with_status[2]}/status/{api_create_vacancy_with_status[3]}")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_delete_vacancy_status_with_invalid_vacancy_id_as_parameter(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].delete(f"api/vacancies?vacancyId=4444444/status/{api_create_vacancy_with_status[3]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_delete_vacancy_status_with_invalid_vacancy_id_as_url(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].delete(f"api/vacancies/{config_data['invalid_vacancy_id']}/status/{api_create_vacancy_with_status[3]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_delete_vacancy_status_without_vacancy_id(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].delete(f"api/vacancies/status/{api_create_vacancy_with_status[3]}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == f"{config_data['error_message_delete_status_without_id_vacancy']}/{api_create_vacancy_with_status[3]}", f"Expected error message {config_data['error_message_delete_status_without_id_vacancy']} in response, but got: {response_body['message']}"


def test_delete_vacancy_status_with_invalid_status_id_as_parameter(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].delete(f"api/vacancies/{api_create_vacancy_with_status[2]}/status?statusId=44444", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_delete_vacancy_status_with_invalid_status_id_as_url(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].delete(f"api/vacancies/{api_create_vacancy_with_status[2]}/status/{config_data['invalid_status_id']}", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_delete_vacancy_status_without_statusid(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].delete(f"api/vacancies/{api_create_vacancy_with_status[2]}/status", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 404, f"Expected status 404, but got {status}. Response: {response_body}"
    assert response_body['message'] == f"{config_data['error_message_delete_status_without_statusid_vacancy']}/{api_create_vacancy_with_status[2]}/status", f"Expected error message {config_data['error_message_delete_status_without_statusid_vacancy']} in response, but got: {response_body['message']}"


def test_archive_vacancy_unauthorized(api_create_vacancy_with_status, config_data: dict):
    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}/archive")
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 401, f"Expected status 401, but got {status}. Response: {response_body}" #404
    assert response_body['message'] == config_data['error_message_unauthorized'], f"Expected error message {config_data['error_message_unauthorized']} in response, but got: {response_body['message']}"


def test_archive_vacancy_valid(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{api_create_vacancy_with_status[2]}/archive", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 200, f"Expected status 200, but got {status}. Response: {response_body}"
    assert response_body['isArchived'] is True, f"Expected 'isArchived' to be True, but got {response_body['isArchived']}. Response: {response_body}"


def test_archive_vacancy_with_invalid_vacancy_id_as_parameter(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].patch("api/vacancies?id=123654/archive", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_parameter'], f"Expected error message {config_data['error_message_by_invalid_id_as_parameter']} in response, but got: {response_body['message']}"


def test_archive_vacancy_with_invalid_vacancy_id_as_url(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/{config_data['invalid_vacancy_id']}/archive", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"


def test_archive_vacancy_without_vacancy_id(api_create_vacancy_with_status, config_data: dict):
    headers = {
        "Authorization": f"Bearer {api_create_vacancy_with_status[1]}"
    }

    response = api_create_vacancy_with_status[0].patch(f"api/vacancies/archive", headers=headers)
    status = response.status
    response_body = response.json()
    logging.info(f"Response: {response_body}")
    assert status == 400, f"Expected status 400, but got {status}. Response: {response_body}"
    assert response_body['message'] == config_data['error_message_by_invalid_id_as_url'], f"Expected error message {config_data['error_message_by_invalid_id_as_url']} in response, but got: {response_body['message']}"
