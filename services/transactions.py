from typing import List

from psycopg2.extras import DictRow

from models.transactions import TransactionModel


class TransactionService:

    @staticmethod
    def get_by_id(login_id: int, transaction_id: int):
        result = TransactionModel.get(login_id, transaction_id)
        return result

    @staticmethod
    def create(login_id, amount, mode, category, datestamp, note, event):
        TransactionModel.create(login_id, amount, mode, category, datestamp, note, event)

    @staticmethod
    def get_by_login_id(login_id: int):
        result: List[DictRow] = TransactionModel.get_all(login_id)
        return result

    @staticmethod
    def delete(transaction_id: int):
        TransactionModel.delete(transaction_id)

    @staticmethod
    def update(transaction_id, amount, mode, category, datestamp, note, event):
        TransactionModel.update(transaction_id, amount, mode, category, datestamp, note, event)

    @staticmethod
    def get_user_spent(login_id: int):
        result = TransactionModel.get_sum_transactions(login_id)
        return 0 if result is None else result[0]["sum"]