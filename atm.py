from database import get_connection


class ATM:

    def __init__(self, user_id):
        self.user_id = user_id

    def get_balance(self):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT balance
            FROM users
            WHERE id = %s
            """,
            (self.user_id,)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        return user["balance"]

    def deposit(self, amount):

        if amount <= 0:
            raise ValueError("Invalid amount")

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET balance = balance + %s
            WHERE id = %s
            """,
            (amount, self.user_id)
        )

        cursor.execute(
            """
            INSERT INTO transactions
            (user_id, transaction_type, amount)
            VALUES (%s, %s, %s)
            """,
            (self.user_id, "DEPOSIT", amount)
        )

        connection.commit()

        cursor.close()
        connection.close()

    def withdraw(self, amount):

        if amount <= 0:
            raise ValueError("Invalid amount")

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT balance
            FROM users
            WHERE id = %s
            """,
            (self.user_id,)
        )

        user = cursor.fetchone()

        if amount > float(user["balance"]):
            cursor.close()
            connection.close()

            raise ValueError("Insufficient balance")

        cursor.execute(
            """
            UPDATE users
            SET balance = balance - %s
            WHERE id = %s
            """,
            (amount, self.user_id)
        )

        cursor.execute(
            """
            INSERT INTO transactions
            (user_id, transaction_type, amount)
            VALUES (%s, %s, %s)
            """,
            (self.user_id, "WITHDRAW", amount)
        )

        connection.commit()

        cursor.close()
        connection.close()

    def get_transactions(self):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                transaction_type,
                amount,
                transaction_date
            FROM transactions
            WHERE user_id = %s
            ORDER BY transaction_date DESC
            """,
            (self.user_id,)
        )

        transactions = cursor.fetchall()

        cursor.close()
        connection.close()

        return transactions