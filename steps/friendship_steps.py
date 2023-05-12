from behave import *
import requests
from environment import create_test_user, delete_user, login, get_user_id

@given('user1 with email "{email}" and password "{password}"')
def step_impl(context, email, password):
    context.email1 = email
    context.password1 = password
    create_test_user(email, password)

@given('user2 with email "{email}" and password "{password}"')
def step_impl(context, email, password):
    context.email2 = email
    context.password2 = password
    create_test_user(email, password)

@given('user1 is logged in')
def step_impl(context):
    context.access_token1 = login(context.email1, context.password1)
    assert context.access_token1 != None

@when('user1 sends a friend request to user2')
def step_impl(context):
    headers = {
        'Authorization': 'Bearer ' + context.access_token1
    }
    # looking for id of users
    response = requests.get('http://localhost:3000/api/users', headers=headers)
    for user in response.json():
        if user['email'] == context.email2:
            context.user2id = user['id']
    assert context.user2id != None
    # sending friend request
    response = requests.post('http://localhost:3000/api/users/friend-request/' + str(context.user2id), headers=headers)
    assert response.status_code == 201
    # checking if friend request was sent
    response = requests.get('http://localhost:3000/api/users/sent-friend-requests', headers=headers)
    for request in response.json():
        if request['receiverId'] == context.user2id:
            context.requestId = request['id']
    assert context.requestId != None

@then('user2 should receive a friend request from user1')
def step_impl(context):
    # logging in as user2
    context.access_token2 = login(context.email2, context.password2)
    assert context.access_token2 != None
    # checking if user2 received a friend request
    headers = {
        'Authorization': 'Bearer ' + context.access_token2
    }
    response = requests.get('http://localhost:3000/api/users/received-friend-requests', headers=headers)
    for request in response.json():
        if request['id'] == context.requestId:
            context.is_request_found = True
    assert context.is_request_found == True

@when('user2 accepts the friend request from user1')
def step_impl(context):
    context.access_token2 = login(context.email2, context.password2)
    headers = {
        'Authorization': 'Bearer ' + context.access_token2
    }
    response = requests.post('http://localhost:3000/api/users/accept-friend-request/' + str(context.requestId), headers=headers)
    assert response.status_code == 201

@then('user1 should be friends with user2')
def step_impl(context):
    headers = {
        'Authorization': 'Bearer ' + context.access_token1
    }
    response = requests.get('http://localhost:3000/api/users/friends', headers=headers)
    for friend in response.json():
        if friend['email'] == context.email2:
            context.is_friend_found = True
    assert context.is_friend_found == True

@then('user2 should be friends with user1')
def step_impl(context):
    headers = {
        'Authorization': 'Bearer ' + context.access_token2
    }
    response = requests.get('http://localhost:3000/api/users/friends', headers=headers)
    for friend in response.json():
        if friend['email'] == context.email1:
            context.is_friend_found = True
    assert context.is_friend_found == True

@then('the friend request should no longer exist')
def step_impl(context):
    headers = {
        'Authorization': 'Bearer ' + context.access_token1
    }
    response = requests.get('http://localhost:3000/api/users/sent-friend-requests', headers=headers)
    context.is_request_found = False
    for request in response.json():
        if request['id'] == context.requestId:
            context.is_request_found = True
    assert context.is_request_found == False

    headers = {
        'Authorization': 'Bearer ' + context.access_token2
    }
    response = requests.get('http://localhost:3000/api/users/received-friend-requests', headers=headers)
    context.is_request_found = False
    for request in response.json():
        if request['id'] == context.requestId:
            context.is_request_found = True
    assert context.is_request_found == False

@when('user1 unfriends user2')
def step_impl(context):
    headers = {
        'Authorization': 'Bearer ' + context.access_token1
    }
    context.user2id = get_user_id(context.email2, context.password2)
    response = requests.delete('http://localhost:3000/api/users/unfriend/' + str(context.user2id), headers=headers)
    assert response.status_code == 204

@then('user1 should not be friends with user2')
def step_impl(context):
    headers = {
        'Authorization': 'Bearer ' + context.access_token1
    }
    response = requests.get('http://localhost:3000/api/users/friends', headers=headers)
    context.is_friend_found = False
    for friend in response.json():
        if friend['email'] == context.email2:
            context.is_friend_found = True
    assert context.is_friend_found == False

@then('user2 should not be friends with user1')
def step_impl(context):
    headers = {
        'Authorization': 'Bearer ' + context.access_token2
    }
    response = requests.get('http://localhost:3000/api/users/friends', headers=headers)
    context.is_friend_found = False
    for friend in response.json():
        if friend['email'] == context.email1:
            context.is_friend_found = True
    assert context.is_friend_found == False

@when('user1 blocks user2')
def step_impl(context):
    headers = {
        'Authorization': 'Bearer ' + context.access_token1
    }
    context.user2id = get_user_id(context.email2, context.password2)
    response = requests.delete('http://localhost:3000/api/users/block/' + str(context.user2id), headers=headers)
    assert response.status_code == 204

@then("user1 should not be able to find user2 in the list of users")
def step_impl(context):
    headers = {
        'Authorization': 'Bearer ' + context.access_token1
    }
    response = requests.get('http://localhost:3000/api/users', headers=headers)
    context.is_user_found = False
    for user in response.json():
        if user['email'] == context.email2:
            context.is_user_found = True
    assert context.is_user_found == False

@then("user2 should not be able to find user1 in the list of users")
def step_impl(context):
    headers = {
        'Authorization': 'Bearer ' + context.access_token2
    }
    response = requests.get('http://localhost:3000/api/users', headers=headers)
    context.is_user_found = False
    for user in response.json():
        if user['email'] == context.email1:
            context.is_user_found = True
    assert context.is_user_found == False