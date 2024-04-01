import requests
from jsonschema import validate
import json
from utils.path import load_schema

def test_login_successful():
    responce = requests.post("https://reqres.in/api/login", json={"email": "eve.holt@reqres.in",
  "password": "cityslicka"})

    assert responce.status_code == 200
    body = responce.json()
    assert body['token'] == 'QpwL5tke4Pnpja7X4'

def test_login_unsuccessful():
    responce = requests.post("https://reqres.in/api/login", json={"email": "peter@klaven"})
    assert responce.status_code == 400
    body = responce.json()
    assert body['error'] == 'Missing password'

def test_register_user_successful():
    responce=requests.post("https://reqres.in/api/register",json={"email": "eve.holt@reqres.in", "password": "pistol"})
    assert responce.status_code == 200
    body = responce.json()
    schema = load_schema("post_register.json")
    with open(schema) as file:
        validate(body, schema=json.loads(file.read()))
    assert body['id'] == 4

def test_register_user_unsuccessful():
    responce = requests.post("https://reqres.in/api/register", json={"email": "sydney@fife"})
    assert responce.status_code == 400
    body = responce.json()
    assert body['error'] == 'Missing password'

def test_single_user():
    first_name = "Janet"
    last_name = "Weaver"
    responce= requests.get("https://reqres.in/api/users/2", data={"first_name": first_name, "last_name": last_name})
    assert responce.status_code == 200
    body = responce.json()
    schema = load_schema("get_single_user.json")
    with open(schema) as file:
        validate(body, schema=json.loads(file.read()))
    assert body["data"]["last_name"] == last_name


def test_user_update():
    name = "morpheus"
    job = "zion resident"

    response = requests.patch('https://reqres.in/api/users/2', data={"name": name, "job": job})
    body = response.json()

    assert response.json()["name"] == name
    assert response.status_code == 200

    schema = load_schema("patch_update_user.json")
    with open(schema) as file:
        schema = json.load(file)
    validate(body, schema=schema)
    assert body["job"] == job

def test_update_user():
    name = "Sergey"
    job = "Teacher"
    response = requests.put("https://reqres.in/api/users/2", data={"name": name, "job": job})

    assert response.status_code == 200
    assert response.json()["name"] == name
    assert response.json()["job"] == job


def test_delete_user():
    response = requests.delete("https://reqres.in/api/users/2")

    assert response.status_code == 204