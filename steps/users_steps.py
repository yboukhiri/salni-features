# from behave import *
# import requests
# from environment import create_test_user, delete_user, login

# @when('user1 blocks user2')
# def step_impl(context):
#     context.headers1 = {
#         'Authorization': 'Bearer ' + context.access_token1
#     }
#     # looking for id of users
#     response = requests.get('http://localhost:3000/api/users', headers=context.headers1)
#     for user in response.json():
#         if user['email'] == context.email2:
#             context.user2id = user['id']
#     assert context.user2id != None
#     # blocking user2
#     response = requests.delete('http://localhost:3000/api/users/block/' + str(context.user2id), headers=context.headers1)
#     assert response.status_code == 204
#     # checking if user2 was blocked
#     response = requests.get('http://localhost:3000/api/users/blocked-users', headers=context.headers1)
#     for user in response.json():
#         if user['id'] == context.user2id:
#             context.is_user_found = True
#     assert context.is_user_found == True

# @then('user1 should not see user2 in the list of users')
# def step_impl(context):
#     # checking if user2 is in the list of users
#     response = requests.get('http://localhost:3000/api/users', headers=context.headers1)
#     context.is_user_found = False
#     for user in response.json():
#         print(user)
#         if user['email'] == context.email2:
#             context.is_user_found = True
#     assert context.is_user_found == False

# @then('user2 should not see user1 in the list of users')
# def step_impl(context):
#     access_token2 = login(context.email2, context.password2)
#     assert access_token2 != None
#     headers = {
#         'Authorization': 'Bearer ' + access_token2
#     }
#     # checking if user1 is in the list of users
#     response = requests.get('http://localhost:3000/api/users', headers=headers)
#     for user in response.json():
#         if user['email'] == context.email1:
#             context.is_user_found = True
#     assert context.is_user_found == False

