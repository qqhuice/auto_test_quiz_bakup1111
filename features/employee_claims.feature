Feature: Employee Claims Management
  As an HR administrator
  I want to manage employee claims
  So that I can process travel allowances and expenses efficiently

  Background:
    Given I am on the OrangeHRM login page
    When I login with valid credentials
    Then I should be on the dashboard page

  @smoke @claims
  Scenario: Create and manage employee claim request
    Given I am on the OrangeHRM dashboard
    When I click on "Claim" in the left sidebar
    Then I should be on the Claims page
    
    When I click on "Employee Claims"
    Then I should be on the Employee Claims page
    
    When I click on "Assign Claim" button
    Then I should see the Create Claim Request form
    
    When I fill in the claim request with following details:
      | Field         | Value             |
      | Employee Name | Amelia Brown      |
      | Event         | Travel allowances |
      | Currency      | Euro              |
    And I take a screenshot of the filled form
    
    When I click "Create" button
    Then I should see success message for claim creation
    And I take a screenshot of the success message
    
    When I navigate to the Assign Claim details page
    Then I should verify the claim details match the input data:
      | Field         | Expected Value    |
      | Employee Name | Amelia Brown      |
      | Event         | Travel allowances |
      | Currency      | Euro              |
    And I take a screenshot of the claim details
    
    When I add expenses with the following details:
      | Expense Type | Date       | Amount |
      | Accommodation| 2024-01-15 | 150.00 |
    And I click "Submit" for expenses
    Then I should see success message for expense submission
    And I take a screenshot of the expense success message
    
    When I verify the expense data matches the input
    And I click "Back" button
    Then I should return to the claims list
    And I take a screenshot of the claims list
    
    When I verify the record exists in the claims list
    Then the claim should be visible with correct details
    And I take a screenshot of the final verification

  @regression @claims
  Scenario Outline: Create claims with different currencies
    Given I am on the Employee Claims page
    When I create a claim request with:
      | Employee Name | <employee>  |
      | Event         | <event>     |
      | Currency      | <currency>  |
    Then the claim should be created successfully
    And the currency should be displayed as "<currency>"
    
    Examples:
      | employee      | event             | currency |
      | Amelia Brown  | Travel allowances | Euro     |
      | John Smith    | Meal allowances   | USD      |

  @negative @claims
  Scenario: Attempt to create claim with missing required fields
    Given I am on the Employee Claims page
    When I click on "Assign Claim" button
    And I leave the Employee Name field empty
    And I click "Create" button
    Then I should see validation error messages
    And the claim should not be created
    And I take a screenshot of the validation errors
