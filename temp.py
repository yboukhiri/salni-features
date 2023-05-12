from environment import create_test_user, make_users_friends

# print(create_test_user("yboukhiri@gmail.com","12345678"))
# for i in range(1,11):
#     print(create_test_user(f"test{i}@test.com","12345678"))

user = {"email": "yboukhiri@gmail.com", "password": "12345678"}
users = [{"email": f"test{i}@test.com", "password": "12345678"} for i in range(1,11)]

for user_ in users:
    print(make_users_friends(user,user_))