Feature: Transactions of Salni APP 

  Scenario: Making a transaction 
    Given user1 with email "user1@test.com" and password "12345678"
    And user2 with email "user2@test.com" and password "12345678"
    And user1 and user2 are friends
    When user1 makes a transaction of 100 EUR to user2
    Then user2 should see a pending transaction of 100 EUR from user1

  Scenario: Making two transactions to a friend
    Given user1 with email "user1@test.com" and password "12345678"
    And user2 with email "user2@test.com" and password "12345678"
    And user1 and user2 are friends
    When user1 makes a transaction of 100 EUR to user2
    And user2 makes a transaction of 50 EUR to user1
    Then user1 should see only one deal with user2
    And user1 should see a pending transaction of 50 EUR from user2
    And user2 should see only one deal with user1
    And user2 should see a pending transaction of 100 EUR from user1

  Scenario: Accepting a transaction
    Given user1 with email "user1@test.com" and password "12345678"
    And user2 with email "user2@test.com" and password "12345678"
    And user1 and user2 are friends
    When user1 makes a transaction of 100 EUR to user2
    And user2 accepts the transaction
    Then user1 should see an accepted transaction of 100 EUR to user2
    And user2 should see an accepted transaction of 100 EUR from user1
