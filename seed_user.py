"""
Create a new ATM user with a securely hashed PIN.

There's no in-app registration flow, so use this script to add accounts.

Usage:
    python seed_user.py
"""

from werkzeug.security import generate_password_hash

from database import get_connection


def create_user(name, account_number, pin, opening_balance=0.00):
    hashed_pin = generate_password_hash(pin)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (name, account_number, pin, balance)
        VALUES (%s, %s, %s, %s)
        """,
        (name, account_number, hashed_pin, opening_balance),
    )

    connection.commit()
    cursor.close()
    connection.close()

    print(f"Created user '{name}' with account number {account_number}.")


if __name__ == "__main__":
    name = input("Name: ").strip()
    account_number = input("Account number: ").strip()
    pin = input("PIN: ").strip()
    balance = input("Opening balance [0.00]: ").strip() or "0.00"

    create_user(name, account_number, pin, float(balance))
