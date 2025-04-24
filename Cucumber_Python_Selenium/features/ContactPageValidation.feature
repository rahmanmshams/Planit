Feature: Contact Form Validation and Submission
  As a user, I want to ensure mandatory fields show validation errors when left empty and allow successful submission with valid data.

  Scenario: Validate mandatory fields and successful form submission
    Given the user navigates to the Contact page
    When the user clicks the Submit button without filling the form
    Then validation error messages appear for mandatory fields
    When the user fills mandatory fields with valid data:
      | Forename    | Email                | Message             |
      | David Jones | david.jones@test.com | Sample message test |
    Then the validation error messages disappear

  Scenario Outline:
    Given the user navigates to the Contact page
    When the user fills mandatory fields with valid data:
      | Forename   | Email   | Message   |
      | <forename> | <email> | <message> |
    And the user clicks the Submit button
    Then the success message "Thanks <forename>, we appreciate your feedback." is displayed

    Examples:
      | forename      | email                  | message                         |
      | Russel Stuart | russel.stuart@test.com | Sample message test             |
      | David Brown   | david.brown@test.com   | Sample message test             |
      | Emily White   | emily.white@test.com   | Sample message test             |
      | Michael Green | michael.green@test.com | Sample message test             |
      | Sophia Black  | sophia.black@test.com  | Sample message test             |