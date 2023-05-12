from behave import *
import requests
from environment import create_test_user, delete_user, login, make_users_friends, get_user_id

@given('user1 and user2 are friends')
def step_impl(context):
    user1=dict(email=context.email1, password=context.password1)
    user2=dict(email=context.email2, password=context.password2)
    context.access_token1, context.access_token2 = login(user1['email'], user1['password']), login(user2['email'], user2['password'])
    make_users_friends(user1, user2)

@when('user1 makes a transaction of {amount} {currency} to user2')
def step_impl(context, amount, currency):
    context.user2id = get_user_id(context.email2, context.password2)
    request_body = {
        "toUserId": context.user2id,
        "amount": amount,
        "currency": currency
    }
    headers = {
        'Authorization': 'Bearer ' + context.access_token1
    }
    response = requests.post('http://localhost:3000/api/deals', json=request_body, headers=headers)
    assert response.status_code == 201

@then('user2 should see a pending transaction of {amount} {currency} from user1')
def step_impl(context, amount, currency):
    headers = {
        'Authorization': 'Bearer ' + context.access_token2
    }
    response = requests.get('http://localhost:3000/api/deals', headers=headers)
    user1id = get_user_id(context.email1, context.password1)
    context.is_transaction_found = False
    for deal in response.json():
        for transaction in deal['transactions']:
            print(transaction)
            if transaction['amount'] == int(amount) and transaction['currency'] == currency \
                and transaction['fromUserId'] == user1id:
                context.is_transaction_found = True
    assert context.is_transaction_found == True

@when("user2 makes a transaction of {amount} {currency} to user1")
def step_impl(context, amount, currency):
    context.user1id = get_user_id(context.email1, context.password1)
    request_body = {
        "toUserId": context.user1id,
        "amount": amount,
        "currency": currency
    }
    headers = {
        'Authorization': 'Bearer ' + context.access_token2
    }
    response = requests.post('http://localhost:3000/api/deals', json=request_body, headers=headers)
    assert response.status_code == 201

@then('user1 should see only one deal with user2')
def step_impl(context):
    headers = {
        'Authorization': 'Bearer ' + context.access_token1
    }
    response = requests.get('http://localhost:3000/api/deals', headers=headers)
    assert len(response.json()) == 1

@then('user1 should see a pending transaction of {amount} {currency} from user2')
def step_impl(context, amount, currency):
    headers = {
        'Authorization': 'Bearer ' + context.access_token1
    }
    response = requests.get('http://localhost:3000/api/deals', headers=headers)
    user2id = get_user_id(context.email2, context.password2)
    context.is_transaction_found = False
    for deal in response.json():
        for transaction in deal['transactions']:
            print(transaction)
            if transaction['amount'] == int(amount) and transaction['currency'] == currency \
                and transaction['fromUserId'] == user2id:
                context.is_transaction_found = True
    assert context.is_transaction_found == True

@then("user2 should see only one deal with user1")
def step_impl(context):
    headers = {
        'Authorization': 'Bearer ' + context.access_token2
    }
    response = requests.get('http://localhost:3000/api/deals', headers=headers)
    assert len(response.json()) == 1

@when('user2 accepts the transaction')
def step_impl(context):
    headers = {
        'Authorization': 'Bearer ' + context.access_token2
    }
    response = requests.get('http://localhost:3000/api/deals', headers=headers)
    context.dealId = str(response.json()[0]['id'])
    context.transactionId = str(response.json()[0]['transactions'][0]['id'])
    print(context.dealId)
    print(context.transactionId)
    response = requests.put('http://localhost:3000/api/deals/' + context.dealId + '/transactions/' + context.transactionId + '/accept', headers=headers)
    assert response.status_code == 200

@then('user1 should see a completed transaction of {amount} {currency} from user2')
def step_impl(context, amount, currency):
    headers = {
        'Authorization': 'Bearer ' + context.access_token1
    }
    response = requests.get('http://localhost:3000/api/deals', headers=headers)
    user2id = get_user_id(context.email2, context.password2)
    context.is_transaction_completed = False
    for deal in response.json():
        for transaction in deal['transactions']:
            print(transaction)
            if transaction['amount'] == int(amount) and transaction['currency'] == currency \
                and transaction['toUserId'] == user2id and transaction['accepted'] == True:
                context.is_transaction_completed = True
    assert context.is_transaction_completed == True

@then("user1 should see an accepted transaction of {amount} {currency} to user2")
def step_impl(context, amount, currency):
    headers = {
        'Authorization': 'Bearer ' + context.access_token1
    }
    response = requests.get('http://localhost:3000/api/deals', headers=headers)
    user2id = get_user_id(context.email2, context.password2)
    context.is_transaction_accepted = False
    for deal in response.json():
        for transaction in deal['transactions']:
            print(transaction)
            if transaction['amount'] == int(amount) and transaction['currency'] == currency \
                and transaction['toUserId'] == user2id and transaction['accepted'] == True:
                context.is_transaction_accepted = True
    assert context.is_transaction_accepted == True

@then('user2 should see an accepted transaction of {amount} {currency} from user1')
def step_impl(context, amount, currency):
    headers = {
        'Authorization': 'Bearer ' + context.access_token2
    }
    response = requests.get('http://localhost:3000/api/deals', headers=headers)
    user1id = get_user_id(context.email1, context.password1)
    context.is_transaction_completed = False
    for deal in response.json():
        for transaction in deal['transactions']:
            print(transaction)
            if transaction['amount'] == int(amount) and transaction['currency'] == currency \
                and transaction['fromUserId'] == user1id and transaction['accepted'] == True:
                context.is_transaction_completed = True
    assert context.is_transaction_completed == True