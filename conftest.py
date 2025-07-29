import json
import logging
import os
import pytest
from playwright.sync_api import Playwright


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("report.txt", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)


def pytest_runtest_logreport(report):

    if report.when == "call":
        test_status = "PASSED" if report.passed else "FAILED" if report.failed else "SKIPPED"

        with open("report.txt", "a") as f:
            f.write(f"Test name: {report.nodeid} | Status: {test_status}\n")
            f.write("\n")


@pytest.fixture(scope="session")
def config_data() -> dict:
    config_path = os.path.join(os.path.dirname(__file__), "user_config.json")
    with open(config_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


@pytest.fixture(scope="session")
def read_id() -> dict:
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


@pytest.fixture(scope="session")
def get_elements_url_and_request_body():
    data = {"Key name": "Value"}
    return ['Url link', data]


@pytest.fixture(scope="session")
def get_status_data():
    data = {"Key name": "Value"}
    return data


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright, request):
    base_url = request.config.getini("base_url")
    request_context = playwright.request.new_context(base_url=base_url)
    yield request_context
    request_context.dispose()


@pytest.fixture(scope="session")
def api_login(api_request_context, config_data: dict):
    request_context = api_request_context

    # login
    data = {
        "email": config_data["email"],
        "password": config_data["password"]
    }
    response_login = request_context.post("api/auth/login", data=data)
    status = response_login.status
    assert status == 200, f"Expected status 200"
    response_body = response_login.json()
    access_token = response_body["access_token"]
    logging.info("The user has successfully logged in")

    yield [request_context, access_token]

    # logout
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response_logout = request_context.post("api/auth/logout", headers=headers)
    response_message = response_logout.json()
    status = response_logout.status
    assert status == 200, f"Expected status 200"
    logging.info(f"The user has successfully logged out. Response message: {response_message['message']}")


@pytest.fixture(scope="session")
def api_create_object(api_login, get_elements_url_and_request_body):
    request_context = api_login[0]
    access_token = api_login[1]
    url = get_elements_url_and_request_body[0]
    data = get_elements_url_and_request_body[1]

    # create element with id
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response_create_element = request_context.post(url, headers=headers, data=data)
    status = response_create_element.status
    assert status == 201, f"Expected status 201"
    response_body = response_create_element.json()
    logging.info(f"The object has been successfully created with id {response_body["id"]}")

    yield [request_context, access_token, response_body["id"], url]

    # delete element
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response_delete = request_context.delete(f"{url}/{response_body["id"]}", headers=headers)
    status = response_delete.status
    response_body = response_delete.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"Object successfully deleted: {response_body['message']}")


@pytest.fixture(scope="session")
def api_create_vacancy_with_status(api_create_object, get_status_data, config_data: dict):
    request_context = api_create_object[0]
    access_token = api_create_object[1]
    object_id = api_create_object[2]
    url = api_create_object[3]
    data = get_status_data

    # create vacancy status with status id
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response_create_vacancy_status = request_context.post(f"{url}/{object_id}/status", headers=headers, data=data)
    status = response_create_vacancy_status.status
    response_body = response_create_vacancy_status.json()
    assert status == 201, f"Expected status 201"

    vacancy_status_id = None
    for status_item in response_body.get("statuses", []):
        if status_item.get("name") == "hr":
            vacancy_status_id = status_item.get("id")
            break

    assert vacancy_status_id is not None, "Failed to find status ID for 'hr' in response."
    logging.info(f"Vacancy status successfully created with id: {vacancy_status_id}")

    # create resume
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    resume_data = {
        "name": config_data["name_resume"],
        "link": config_data['link_example']
    }

    response_create_resume = request_context.post("api/resumes", headers=headers, data=resume_data)
    status = response_create_resume.status
    assert status == 201, f"Expected status 201"
    response_body = response_create_resume.json()
    resume_id = response_body["id"]
    logging.info(f"The Resume has been successfully created with id {response_body["id"]}")

    yield [request_context, access_token, object_id, vacancy_status_id, resume_id]

    # delete vacancy status
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response_delete_vacancy_status = request_context.delete(f"{url}/{object_id}/status/{vacancy_status_id}", headers=headers)
    status = response_delete_vacancy_status.status
    response_body = response_delete_vacancy_status.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"Vacancy status successfully deleted: {response_body['message']}")

    # delete resume
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response_delete_resume = request_context.delete(f"api/resumes/{resume_id}", headers=headers)
    status = response_delete_resume.status
    response_body = response_delete_resume.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"Resume successfully deleted: {response_body['message']}")


@pytest.fixture(scope="session")
def api_create_social_link(api_login, get_elements_url_and_request_body):
    request_context = api_login[0]
    access_token = api_login[1]
    url = get_elements_url_and_request_body[0]
    data = get_elements_url_and_request_body[1]

    # create social link id
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response_create_element = request_context.post(url, headers=headers, data=data)
    status = response_create_element.status
    assert status == 201, f"Expected status 201"
    response_body = response_create_element.json()
    logging.info(f"The social link has been successfully created with id {response_body["data"]["id"]}")

    yield [request_context, access_token, response_body["data"]["id"], url]

    # delete social link
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response_delete = request_context.delete(f"{url}/{response_body["data"]["id"]}", headers=headers)
    status = response_delete.status
    response_body = response_delete.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"Social link successfully deleted: {response_body['message']}")


@pytest.fixture(scope="session")
def api_only_login(api_request_context, config_data: dict):
    request_context = api_request_context

    # login
    data = {
        "email": config_data["email"],
        "password": config_data["password"]
    }
    response_login = request_context.post("api/auth/login", data=data)
    status = response_login.status
    assert status == 200, f"Expected status 200"
    response_body = response_login.json()
    access_token = response_body["access_token"]
    logging.info("The user has successfully logged in")

    yield [access_token]


@pytest.fixture(scope="session")
def api_only_sign_in(api_request_context, config_data: dict):
    request_context = api_request_context

    # sign in
    data = {
        "email": config_data["email"],
        "password": config_data["password"]
    }
    response_sign_in = request_context.post("api/auth/register", data=data)
    status = response_sign_in.status
    assert status == 201, f"Expected status 200"
    response_body = response_sign_in.json()
    access_token = response_body["access_token"]
    logging.info("The user has successfully sign in")

    yield [access_token]


@pytest.fixture(scope="session")
def api_expired_token_when_register_logout_login(api_request_context, config_data: dict):
    request_context = api_request_context

    # sign in
    data = {
        "email": config_data["email"],
        "password": config_data["password"]
    }
    response_sign_in = request_context.post("api/auth/register", data=data)
    status = response_sign_in.status
    assert status == 201, f"Expected status 201"
    response_body_sign_in = response_sign_in.json()
    sign_in_access_token = response_body_sign_in["access_token"]
    logging.info("The user has successfully signed in")

    # logout
    headers = {
        "Authorization": f"Bearer {sign_in_access_token}"
    }
    response_logout = request_context.post("api/auth/logout", headers=headers)
    response_message = response_logout.json()
    status = response_logout.status
    assert status == 200, f"Expected status 200"
    logging.info(f"The user has successfully logged out. Response message: {response_message['message']}")

    # login
    response_login = request_context.post("api/auth/login", data=data)
    status = response_login.status
    assert status == 200, f"Expected status 200"
    response_body_login = response_login.json()
    login_access_token = response_body_login["access_token"]
    logging.info("The user has successfully logged in")

    yield [request_context, sign_in_access_token]

    # delete user
    headers_new = {
        "Authorization": f"Bearer {login_access_token}"
    }
    response_delete_user = request_context.delete(f"api/user", headers=headers_new)
    status = response_delete_user.status
    response_user = response_delete_user.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"User successfully deleted: {response_user['message']}")


@pytest.fixture(scope="session")
def api_expired_token_when_login_logout_login(api_request_context, config_data: dict):
    request_context = api_request_context

    data = {
        "email": config_data["email"],
        "password": config_data["password"]
    }

    # login
    response_login = request_context.post("api/auth/login", data=data)
    status = response_login.status
    assert status == 200, f"Expected status 200"
    response_body_login = response_login.json()
    login_access_token = response_body_login["access_token"]
    logging.info("The user has successfully logged in")

    # logout
    headers = {
        "Authorization": f"Bearer {login_access_token}"
    }
    response_logout = request_context.post("api/auth/logout", headers=headers)
    response_message = response_logout.json()
    status = response_logout.status
    assert status == 200, f"Expected status 200"
    logging.info(f"The user has successfully logged out. Response message: {response_message['message']}")

    # login
    response_login_new = request_context.post("api/auth/login", data=data)
    status = response_login_new.status
    assert status == 200, f"Expected status 200"
    response_body_login_new = response_login_new.json()
    login_access_token_new = response_body_login_new["access_token"]
    logging.info("The user has successfully logged in")

    yield [request_context, login_access_token]

    # delete user
    headers_new = {
        "Authorization": f"Bearer {login_access_token_new}"
    }
    response_delete_user = request_context.delete(f"api/user", headers=headers_new)
    status = response_delete_user.status
    response_user = response_delete_user.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"User successfully deleted: {response_user['message']}")


@pytest.fixture(scope="session")
def api_expired_token_when_refresh(api_request_context, config_data: dict):
    request_context = api_request_context

    data = {
        "email": config_data["email"],
        "password": config_data["password"]
    }

    # login
    response_login = request_context.post("api/auth/login", data=data)
    status = response_login.status
    assert status == 200, f"Expected status 200"
    response_body_login = response_login.json()
    login_refresh_token = response_body_login["refresh_token"]
    logging.info("The user has successfully logged in")

    # refresh
    refresh_data = {
        "refresh_token": login_refresh_token
    }
    response_refresh = request_context.post("api/auth/refresh", data=refresh_data)
    status = response_refresh.status
    assert status == 201, f"Expected status 201"
    response_body_refresh = response_refresh.json()
    refresh_token = response_body_refresh["access_token"]
    logging.info("The user has successfully refreshed token")

    yield [request_context, login_refresh_token]

    # delete user
    headers_new = {
        "Authorization": f"Bearer {refresh_token}"
    }
    response_delete_user = request_context.delete(f"api/user", headers=headers_new)
    status = response_delete_user.status
    response_user = response_delete_user.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"User successfully deleted: {response_user['message']}")


@pytest.fixture(scope="session")
def api_add_features_for_logout_verification(api_request_context, config_data: dict):
    request_context = api_request_context

    # login
    data = {
        "email": config_data["email"],
        "password": config_data["password"]
    }
    response_login = request_context.post("api/auth/login", data=data)
    status = response_login.status
    assert status == 200, f"Expected status 200"
    response_body = response_login.json()
    access_token = response_body["access_token"]
    logging.info("The user has successfully logged in")

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # create social link
    social_link_data = {
        "name": config_data["name_example"],
        "link": config_data['link_example']
    }

    response_social_link = request_context.post("api/user/socials", headers=headers, data=social_link_data)
    status = response_social_link.status
    assert status == 201, f"Expected status 201"
    social_link_id = response_social_link.json()
    logging.info(f"The social link has been successfully created with id {social_link_id["data"]["id"]}")


    # create note
    note_data = {
        "name": config_data["note_name"],
        "text": config_data['note_text']
    }

    response_note = request_context.post("api/notes", headers=headers, data=note_data)
    status = response_note.status
    assert status == 201, f"Expected status 201"
    note_id = response_note.json()
    logging.info(f"The note has been successfully created with id {note_id['id']}")


    # create resume
    resume_data = {
        "name": config_data["name_resume"],
        "link": config_data['link_example']
    }

    response_resume = request_context.post("api/resumes", headers=headers, data=resume_data)
    status = response_resume.status
    assert status == 201, f"Expected status 201"
    resume_id = response_resume.json()
    logging.info(f"The resume has been successfully created with id {resume_id['id']}")

    # create cover_letter
    cover_letter_data = {
        "name": config_data["cover_letter_name"],
        "text": config_data['cover_letter_text']
    }

    response_cover_letter = request_context.post("api/cover-letter", headers=headers, data=cover_letter_data)
    status = response_cover_letter.status
    assert status == 201, f"Expected status 201"
    cover_letter_id = response_cover_letter.json()
    logging.info(f"The cover letter has been successfully created with id {cover_letter_id['id']}")

    # create project
    project_data = {
        "name": config_data['project_name'],
        "link": config_data['githubLink_valid'],
        "technologies": "string",
        "description": "string"
    }

    response_project = request_context.post("api/projects", headers=headers, data=project_data)
    status = response_project.status
    assert status == 201, f"Expected status 201"
    project_id = response_project.json()
    logging.info(f"The project has been successfully created with id {project_id['id']}")

    # create event
    event_data = {
        "name": config_data["event_name"],
        "date": config_data['event_date_valid'],
        "time": config_data['event_time_valid']
    }

    response_event = request_context.post("api/events", headers=headers, data=event_data)
    status = response_event.status
    assert status == 201, f"Expected status 201"
    event_id = response_event.json()
    logging.info(f"The event has been successfully created with id {event_id['id']}")

    # create prediction
    prediction_data = {
        "textUk": config_data["textUk"],
        "textEn": config_data['textEn']
    }

    response_prediction = request_context.post("api/predictions", headers=headers, data=prediction_data)
    status = response_prediction.status
    assert status == 201, f"Expected status 201"
    prediction_id = response_prediction.json()
    logging.info(f"The prediction has been successfully created with id {prediction_id['id']}")

    # create vacancy
    vacancy_data = {
        "vacancy": config_data["vacancy"],
        "link": config_data['link_example'],
        "company": config_data["company"],
        "location": config_data['location'],
        "work_type": config_data['work_type_example']
    }

    response_vacancy = request_context.post("api/vacancies", headers=headers, data=vacancy_data)
    status = response_vacancy.status
    assert status == 201, f"Expected status 201"
    vacancy_id = response_vacancy.json()
    logging.info(f"The event has been successfully created with id {vacancy_id['id']}")

    # logout
    response_logout = request_context.post("api/auth/logout", headers=headers)
    response_message = response_logout.json()
    status = response_logout.status
    assert status == 200, f"Expected status 200"
    logging.info(f"The user has successfully logged out. Response message: {response_message['message']}")

    yield [request_context, access_token, social_link_id["data"]["id"], note_id['id'], resume_id['id'], cover_letter_id['id'], project_id['id'], event_id['id'], prediction_id['id'], vacancy_id['id']]

    # login
    data = {
        "email": config_data["email"],
        "password": config_data["password"]
    }
    response_login_after_logout = request_context.post("api/auth/login", data=data)
    status = response_login_after_logout.status
    assert status == 200, f"Expected status 200"
    response_api_body = response_login_after_logout.json()
    new_access_token = response_api_body["access_token"]
    logging.info("The user has successfully logged in again")

    headers = {
        "Authorization": f"Bearer {new_access_token}"
    }

    # delete social link
    response_delete_social_link = request_context.delete(f"api/user/socials/{social_link_id["data"]["id"]}", headers=headers)
    status = response_delete_social_link.status
    response_social_link = response_delete_social_link.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"Social link successfully deleted: {response_social_link['message']}")

    # delete note
    response_delete_note = request_context.delete(f"api/notes/{note_id['id']}", headers=headers)
    status = response_delete_note.status
    response_note = response_delete_note.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"Note successfully deleted: {response_note['message']}")

    # delete resume
    response_delete_resume = request_context.delete(f"api/resumes/{resume_id['id']}", headers=headers)
    status = response_delete_resume.status
    response_resume = response_delete_resume.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"Resume successfully deleted: {response_resume['message']}")

    # delete cover letter
    response_delete_cover_letter = request_context.delete(f"api/cover-letter/{cover_letter_id['id']}", headers=headers)
    status = response_delete_cover_letter.status
    response_cover_letter = response_delete_cover_letter.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"Cover letter successfully deleted: {response_cover_letter['message']}")

    # delete project
    response_delete_project = request_context.delete(f"api/projects/{project_id['id']}", headers=headers)
    status = response_delete_project.status
    response_project = response_delete_project.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"Project successfully deleted: {response_project['message']}")

    # delete event
    response_delete_event = request_context.delete(f"api/events/{event_id['id']}", headers=headers)
    status = response_delete_event.status
    response_event = response_delete_event.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"Event successfully deleted: {response_event['message']}")

    # delete vacancy
    response_delete_vacancy = request_context.delete(f"api/vacancies/{vacancy_id['id']}", headers=headers)
    status = response_delete_vacancy.status
    response_vacancy = response_delete_vacancy.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"Vacancy successfully deleted: {response_vacancy['message']}")

    # delete prediction
    response_delete_prediction = request_context.delete(f"api/predictions/{prediction_id['id']}", headers=headers)
    status = response_delete_prediction.status
    response_prediction = response_delete_prediction.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"Prediction successfully deleted: {response_prediction['message']}")

    # logout
    response_logout = request_context.post("api/auth/logout", headers=headers)
    response_message = response_logout.json()
    status = response_logout.status
    assert status == 200, f"Expected status 200"
    logging.info(f"The user has successfully logged out. Response message: {response_message['message']}")


@pytest.fixture(scope="session")
def api_for_auth_when_logout(api_request_context, config_data: dict):
    request_context = api_request_context

    # login
    data = {
        "email": config_data["email"],
        "password": config_data["password"]
    }
    response_login = request_context.post("api/auth/login", data=data)
    status = response_login.status
    assert status == 200, f"Expected status 200"
    response_body = response_login.json()
    access_token = response_body["access_token"]
    logging.info("The user has successfully logged in")

    # logout
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response_logout = request_context.post("api/auth/logout", headers=headers)
    response_message = response_logout.json()
    status = response_logout.status
    assert status == 200, f"Expected status 200"
    logging.info(f"The user has successfully logged out. Response message: {response_message['message']}")

    yield [request_context, access_token]

    # login
    response_login = request_context.post("api/auth/login", data=data)
    status = response_login.status
    assert status == 200, f"Expected status 200"
    response_body = response_login.json()
    access_token_new = response_body["access_token"]
    logging.info("The user has successfully logged in")

    headers_new = {
        "Authorization": f"Bearer {access_token_new}"
    }

    # delete user
    response_delete_user = request_context.delete(f"api/user", headers=headers_new)
    status = response_delete_user.status
    response_user = response_delete_user.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"User successfully deleted: {response_user['message']}")


@pytest.fixture(scope="session")
def api_sign_in(api_request_context, config_data: dict):
    request_context = api_request_context

    # sign_in

    data = {
        "email": config_data["email"],
        "password": config_data["password"]
    }

    response_sign_in = api_request_context.post("api/auth/register", data=data)

    status = response_sign_in.status
    assert status == 201, f"Expected status 201"
    response_body = response_sign_in.json()
    access_token = response_body["access_token"]
    refresh_token = response_body["refresh_token"]
    logging.info("The user has successfully signed in")

    yield [request_context, access_token, refresh_token]

    # delete user
    headers_new = {
        "Authorization": f"Bearer {access_token}"
    }

    response_delete_user = request_context.delete(f"api/user", headers=headers_new)
    status = response_delete_user.status
    response_user = response_delete_user.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"User successfully deleted: {response_user['message']}")


@pytest.fixture(scope="session")
def api_change_password(api_request_context, config_data: dict):
    request_context = api_request_context

    # login
    data = {
        "email": config_data["email"],
        "password": config_data["password"]
    }
    response_login = request_context.post("api/auth/login", data=data)
    status = response_login.status
    assert status == 200, f"Expected status 200"
    response_body = response_login.json()
    access_token = response_body["access_token"]
    logging.info("The user has successfully logged in")

    yield [request_context, access_token]

    # logout
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response_logout = request_context.post("api/auth/logout", headers=headers)
    response_message = response_logout.json()
    status = response_logout.status
    assert status == 200, f"Expected status 200"
    logging.info(f"The user has successfully logged out. Response message: {response_message['message']}")

    # login
    new_data = {
        "email": config_data["email"],
        "password": config_data["new_password"]
    }
    response_new_login = request_context.post("api/auth/login", data=new_data)
    status = response_new_login.status
    assert status == 200, f"Expected status 200"
    response_body_new = response_new_login.json()
    new_access_token = response_body_new["access_token"]
    logging.info("The user has successfully logged in")

    # delete user
    headers_new = {
        "Authorization": f"Bearer {new_access_token}"
    }

    response_delete_user = request_context.delete(f"api/user", headers=headers_new)
    status = response_delete_user.status
    response_user = response_delete_user.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"User successfully deleted: {response_user['message']}")


@pytest.fixture(scope="session")
def api_forgot_password(api_request_context, config_data: dict):
    request_context = api_request_context

    # forgot password
    data = {
        "email": config_data["email"]
    }

    response = api_request_context.post("api/auth/forgot-password", data=data)
    status = response.status
    assert status == 201, f"Expected status 201"
    response_body = response.json()
    forgot_password_token = response_body["token"]
    logging.info(f"Password successfully reset with message: {response_body['message']}")

    yield [request_context, forgot_password_token]


@pytest.fixture(scope="session")
def api_refresh_token(api_request_context, config_data: dict):
    request_context = api_request_context

    # login
    data = {
        "email": config_data["email"],
        "password": config_data["password"]
    }
    response_login = request_context.post("api/auth/login", data=data)
    status = response_login.status
    assert status == 200, f"Expected status 200"
    response_body = response_login.json()
    access_token = response_body["access_token"]
    refresh_token = response_body["refresh_token"]
    logging.info("The user has successfully logged in")

    # refresh token
    data = {
        "refresh_token": refresh_token
    }

    response = api_request_context.post("api/auth/refresh", data=data)
    status = response.status
    assert status == 201, f"Expected status 201"
    response_body = response.json()
    new_refresh_token = response_body["access_token"]
    logging.info(f"The user received a token")

    yield [request_context, new_refresh_token]

    # logout
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response_logout = request_context.post("api/auth/logout", headers=headers)
    response_message = response_logout.json()
    status = response_logout.status
    assert status == 200, f"Expected status 200"
    logging.info(f"The user has successfully logged out. Response message: {response_message['message']}")


@pytest.fixture(scope="session")
def api_logout(api_request_context, config_data: dict):
    request_context = api_request_context

    # login
    data = {
        "email": config_data["email"],
        "password": config_data["password"]
    }
    response_login = request_context.post("api/auth/login", data=data)
    status = response_login.status
    assert status == 200, f"Expected status 200"
    response_body = response_login.json()
    access_token = response_body["access_token"]
    logging.info("The user has successfully logged in")

    yield [request_context, access_token]


@pytest.fixture(scope="session")
def api_login_for_profile_tests(api_request_context, config_data: dict):
    request_context = api_request_context

    # login
    data = {
        "email": config_data["email"],
        "password": config_data["password"]
    }
    response_login = request_context.post("api/auth/login", data=data)
    status = response_login.status
    assert status == 200, f"Expected status 200"
    response_body = response_login.json()
    access_token = response_body["access_token"]
    logging.info("The user has successfully logged in")

    yield [request_context, access_token]

    headers_new = {
        "Authorization": f"Bearer {access_token}"
    }

    # delete user
    response_delete_user = request_context.delete(f"api/user", headers=headers_new)
    status = response_delete_user.status
    response_user = response_delete_user.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"User successfully deleted: {response_user['message']}")

    # get profile
    response_get_user = request_context.get(f"api/user/profile", headers=headers_new)
    status = response_get_user.status
    response_body_user = response_get_user.json()
    assert status == 401, f"Expected status 401"
    assert response_body_user['message'] == config_data['error_message_get_after_deleting_user'], f"Expected error message {config_data['error_message_get_after_deleting_user']} in response, but got: {response_body['message']}"
    logging.info(f"Checking when receiving data from a deleted user: {response_body_user['message']}")


@pytest.fixture(scope="session")
def api_reset_password(api_request_context, config_data: dict):
    request_context = api_request_context

    # login
    data = {
        "email": config_data["email"],
        "password": config_data["password"]
    }
    response_login = request_context.post("api/auth/login", data=data)
    status = response_login.status
    assert status == 200, f"Expected status 200"
    response_body = response_login.json()
    access_token = response_body["access_token"]
    logging.info("The user has successfully logged in")

    # forgot password
    data = {
        "email": config_data["email"]
    }

    response_forgot_password = api_request_context.post("api/auth/forgot-password", data=data)
    status = response_forgot_password.status
    assert status == 201, f"Expected status 201"
    response_body_forgot_password = response_forgot_password.json()
    forgot_password_token = response_body_forgot_password["token"]
    logging.info(f"Password successfully reset with message: {response_body_forgot_password['message']}")

    yield [request_context, access_token, forgot_password_token]

    # logout
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response_logout = request_context.post("api/auth/logout", headers=headers)
    response_message = response_logout.json()
    status = response_logout.status
    assert status == 200, f"Expected status 200"
    logging.info(f"The user has successfully logged out. Response message: {response_message['message']}")

    # login
    data = {
        "email": config_data["email"],
        "password": config_data["new_password"]
    }
    response_login_new = request_context.post("api/auth/login", data=data)
    status = response_login_new.status
    assert status == 200, f"Expected status 200"
    response_body_new = response_login_new.json()
    access_token_new = response_body_new["access_token"]
    logging.info("The user has successfully logged in")

    headers_new = {
        "Authorization": f"Bearer {access_token_new}"
    }

    # delete user
    response_delete_user = request_context.delete(f"api/user", headers=headers_new)
    status = response_delete_user.status
    response_user = response_delete_user.json()
    assert status == 200, f"Expected status 200"
    logging.info(f"User successfully deleted: {response_user['message']}")
