Feature: Shopping Cart Validation
  As a user, I want to validate item purchases and cart totals.

  Scenario: Validate cart calculation after purchasing items
    Given the user navigates to the Shop page
    When the user purchases the following items:
      | Item           | Quantity |
      | Stuffed Frog   | 2        |
      | Fluffy Bunny   | 5        |
      | Valentine Bear | 3        |
    Then the cart count should be correct
    And the user navigates to the Cart page
    Then the cart items should match their expected subtotal and total
