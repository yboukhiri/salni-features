import requests

def create_test_user(email, password):
    if (login(email, password) != None):
        delete_user(email, password)
    request_body = {
        "firstName": "test",
        "lastName": "test",
        "email": email,
        "password": password,
        "birthDay": "1",
        "birthMonth": "1",
        "birthYear": "1990",
        "gender": "male"
    }
    response = requests.post('http://localhost:3000/api/auth/signup', json=request_body)
    return response.status_code == 201

def delete_user(email, password):
    request_body = {
        "email": email,
        "password": password
    }
    response = requests.post('http://localhost:3000/api/auth/login', json=request_body)
    access_token = response.json()['access_token']
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.delete('http://localhost:3000/api/auth', headers=headers)
    return response.status_code == 204

def login(email, password):
    request_body = {
        "email": email,
        "password": password
    }
    response = requests.post('http://localhost:3000/api/auth/login', json=request_body)
    if (response.status_code == 201):
        return response.json()['access_token']
    return None

def make_users_friends(user1, user2):
    access_token1 = login(user1['email'], user1['password'])
    assert access_token1 != None
    headers = {
        'Authorization': 'Bearer ' + access_token1
    }
    # looking for id of users
    response = requests.get('http://localhost:3000/api/users', headers=headers)
    for user in response.json():
        if user['email'] == user2['email']:
            user2id = user['id']
    assert user2id != None
    # sending friend request
    response = requests.post('http://localhost:3000/api/users/friend-request/' + str(user2id), headers=headers)
    assert response.status_code == 201
    # getting request id
    response = requests.get('http://localhost:3000/api/users/sent-friend-requests', headers=headers)
    for request in response.json():
        if request['receiverId'] == user2id:
            requestId = request['id']
    assert requestId != None
    # logging in as user2
    access_token2 = login(user2['email'], user2['password'])
    assert access_token2 != None
    # accepting friend request
    headers = {
        'Authorization': 'Bearer ' + access_token2
    }
    response = requests.post('http://localhost:3000/api/users/accept-friend-request/' + str(requestId) , headers=headers)
    assert response.status_code == 201
    # checking if user1 and user2 are friends
    response = requests.get('http://localhost:3000/api/users/friends', headers=headers)
    is_friend_found = False
    for friend in response.json():
        if friend['email'] == user1['email']:
            is_friend_found = True
    assert is_friend_found == True

def get_user_id(email, password):
    access_token = login(email, password)
    assert access_token != None
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get('http://localhost:3000/api/auth', headers=headers)
    return response.json()['id']