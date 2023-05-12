Feature: users and friendship for salni APP

  Scenario: Send a friend request
    Given user1 with email "user1@test.com" and password "12345678"
    And user2 with email "user2@test.com" and password "12345678"
    And user1 is logged in
    When user1 sends a friend request to user2
    Then user2 should receive a friend request from user1

  Scenario: Accept a friend request
    Given user1 with email "user1@test" and password "12345678"
    And user2 with email "user2@test" and password "12345678"
    And user1 is logged in
    When user1 sends a friend request to user2
    And user2 accepts the friend request from user1
    Then user1 should be friends with user2
    And user2 should be friends with user1
    And the friend request should no longer exist

  Scenario: Unfriend a user
    Given user1 with email "user1@test.com" and password "12345678"
    And user2 with email "user2@test.com" and password "12345678"
    And user1 and user2 are friends
    When user1 unfriends user2
    Then user1 should not be friends with user2
    And user2 should not be friends with user1

  @this
  Scenario: Block a user
    Given user1 with email "user1@test.com" and password "12345678"
    And user2 with email "user2@test.com" and password "12345678"
    And user1 and user2 are friends
    When user1 blocks user2
    Then user1 should not be friends with user2
    And user2 should not be friends with user1
    And user1 should not be able to find user2 in the list of users
    And user2 should not be able to find user1 in the list of users
