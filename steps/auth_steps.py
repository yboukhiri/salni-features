from behave import *
import requests

@given('a user with firstName "{firstName}"')
def step_impl(context, firstName):
    context.firstName = firstName

@given('with lastName "{lastName}"')
def step_impl(context, lastName):
    context.lastName = lastName

@given('with email "{email}"')
def step_impl(context, email):
    context.email = email

@given('with password "{password}"')
def step_impl(context, password):
    context.password = password

@given('with birthDay "{birthDay}"')
def step_impl(context, birthDay):
    context.birthDay = birthDay

@given('with birthMonth "{birthMonth}"')
def step_impl(context, birthMonth):
    context.birthMonth = birthMonth

@given('with birthYear "{birthYear}"')
def step_impl(context, birthYear):
    context.birthYear = birthYear

@given('with gender "{gender}"')
def step_impl(context, gender):
    context.gender = gender

@When('user create a new account')
def step_impl(context):
    request_body = {
        "firstName": context.firstName,
        "lastName": context.lastName,
        "email": context.email,
        "password": context.password,
        "birthDay": context.birthDay,
        "birthMonth": context.birthMonth,
        "birthYear": context.birthYear,
        "gender": context.gender
    }
    response = requests.post('http://localhost:3000/api/auth/signup', json=request_body)
    context.response = response

@Then('user should be created')
def step_impl(context):
    assert context.response.status_code == 201

@Given('a user with email "{email}"')
def step_impl(context, email):
    context.email = email

@Given('with password1 "{password}"')
def step_impl(context, password):
    context.password = password

@When('user login')
def step_impl(context):
    request_body = {
        "email": context.email,
        "password": context.password
    }
    response = requests.post('http://localhost:3000/api/auth/login', json=request_body)
    context.response = response

@Then('user should be logged')
def step_impl(context):
    assert context.response.status_code == 201
    assert context.response.json()['access_token'] != None
    context.access_token = context.response.json()['access_token']

@Then('user can access to his account')
def step_impl(context):
    headers = {
        'Authorization': 'Bearer ' + context.access_token
    }
    response = requests.get('http://localhost:3000/api/auth', headers=headers)
    assert response.status_code == 200
    assert response.json()['email'] == context.email

@Given('a user with email1 "{email}"')
def step_impl(context, email):
    context.email = email

@Given('with password2 "{password}"')
def step_impl(context, password):
    context.password = password

@When('user delete his account')
def step_impl(context):
    request_body = {
        "email": context.email,
        "password": context.password
    }
    response = requests.post('http://localhost:3000/api/auth/login', json=request_body)
    context.access_token = response.json()['access_token']
    headers = {
        'Authorization': 'Bearer ' + context.access_token
    }
    response = requests.delete('http://localhost:3000/api/auth', headers=headers)
    context.response = response

@Then('user should be deleted')
def step_impl(context):
    assert context.response.status_code == 204

@Then('user can\'t access to his account')
def step_impl(context):
    headers = {
        'Authorization': 'Bearer ' + context.access_token
    }
    response = requests.get('http://localhost:3000/api/auth', headers=headers)
    assert response.status_code != 201