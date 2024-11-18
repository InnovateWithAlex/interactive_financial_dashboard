# savings_investment.py

import math

# Function to calculate the required contribution to reach the savings goal
def calculate_required_contribution(current_balance, goal_amount, contribution_frequency, timeframe_months):
    # Ensure the frequency is correct
    frequency_factor = 12 if contribution_frequency.lower() == 'monthly' else 52
    total_contributions_needed = goal_amount - current_balance
    required_contribution = total_contributions_needed / timeframe_months
    return required_contribution

# Function to calculate the future value of the savings with investment growth
def calculate_investment_projection(current_balance, contribution, contribution_frequency, timeframe_months, annual_return_rate):
    frequency_factor = 12 if contribution_frequency.lower() == 'monthly' else 52
    r = annual_return_rate / frequency_factor
    n = timeframe_months * (frequency_factor / 12)

    # Calculate future value of the contributions + balance
    future_value = current_balance * ((1 + r) ** n) + contribution * (((1 + r) ** n - 1) / r)
    return future_value

# Example interactive usage
if __name__ == "__main__":
    while True:
        print("\n--- Savings & Investment Calculator ---")

        # Get user inputs
        try:
            current_balance = float(input("Enter your current savings balance ($): "))
            goal_amount = float(input("Enter your savings goal ($): "))
            contribution_frequency = input("Enter contribution frequency ('monthly' or 'weekly'): ").strip().lower()
            
            if contribution_frequency not in ['monthly', 'weekly']:
                print("Invalid frequency. Please enter either 'monthly' or 'weekly'.")
                continue
            
            contribution = float(input(f"Enter your contribution amount per {contribution_frequency} ($): "))
            timeframe_months = int(input("Enter the timeframe in months: "))
            annual_return_rate = float(input("Enter the expected annual return rate (as a decimal, e.g., 0.05 for 5%): "))

            # Validate inputs
            if current_balance < 0 or goal_amount < 0 or contribution < 0 or timeframe_months <= 0 or annual_return_rate < 0:
                print("Please enter positive values for all inputs.")
                continue

        except ValueError:
            print("Invalid input. Please enter numeric values.")
            continue

        # Provide options to the user
        print("\nOptions:")
        print("1. Calculate the required contribution to reach your savings goal.")
        print("2. Calculate the future value of your savings with your current contribution.")
        print("3. Exit")

        option = input("\nChoose an option (1, 2, or 3): ")

        # Handle the user's choice
        if option == '1':
            required_contribution = calculate_required_contribution(current_balance, goal_amount, contribution_frequency, timeframe_months)
            print(f"\nRequired Contribution to reach the goal: ${required_contribution:.2f} per {contribution_frequency}")

        elif option == '2':
            future_value = calculate_investment_projection(current_balance, contribution, contribution_frequency, timeframe_months, annual_return_rate)
            print(f"\nProjected Future Value of Savings with Investment: ${future_value:.2f}")

        elif option == '3':
            print("Thank you for using the Savings & Investment Calculator!")
            break

        else:
            print("Invalid option. Please choose a valid number.")

