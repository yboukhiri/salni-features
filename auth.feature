Feature: Authentification for salni APP

  Scenario: Create a new user
     Given a user with firstName "Yassinetest"
      And with lastName "Boukhiritest"
      And with email "yboukhiri@test.com"
      And with password "12345678"
      And with birthDay "29"
      And with birthMonth "04"
      And with birthYear "2000"
      And with gender "male"
      When user create a new account
      Then user should be created

  Scenario: Login with a user
      Given a user with email "yboukhiri@test.com"
      And with password1 "12345678"
      When user login
      Then user should be logged
      And user can access to his account

  Scenario: Delete a user
      Given a user with email1 "yboukhiri@test.com"
      And with password2 "12345678"
      When user delete his account
      Then user should be deleted
      And user can't access to his account

  