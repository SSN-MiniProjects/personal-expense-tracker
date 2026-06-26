class SecurityConstants:
    APP_SECRET_KEY = 'B7-1A3E'

class ErrorConstants:
    ACCOUNT_NOT_FOUND = "Account Not Found!"
    WRONG_PASSWORD = "Incorrect Password!"
    DUPLICATE_EMAIL_REG = "Email already exists!"
    DUPLICATE_EVENT_NAME = "Event already exists!"
    EVENT_NOT_FOUND = "Event Not Found !"
    TRANSACTION_NOT_FOUND = "Transaction not found!"


class InputErrorMessages:
    NOT_VALID_BUDGET = "Please enter valid budget amount"
    NOT_VALID_AMOUNT = "Please enter valid transaction amount"
    NOT_VALID_PHONE = "Please enter valid phone number"
    NOT_VALID_DATE = "Please enter valid date"

class TransactionMessages:
    EXPENSE_ADDED_SUCCESS = "Expense Added Successfully"
    EXPENSE_UPDATED_SUCCESS = "Expense Updated Successfully"
    EXPENSE_DELETED = "Expense Deleted Successfully"

class ExpenseHistoryFiterOptions:
    CATEGORY = "category"
    DATES_BETWEEN = "dates_between"
    AMOUNTS_RANGE = "amounts_range"
    MODE = "mode"
    EVENT = "event"

class Templates:
    VIEW_TRANSACTION = "view_transaction.html"
    UPDATE_TRANSACTION = "update_transaction.html"


class FlashMessageCategory:
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
