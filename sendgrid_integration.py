# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from random import seed
from random import randint

class SendGrid:
    def __init__(self):
        self.sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        self.from_email = "personalExpenseTracker7@gmail.com"

    def otp_generation(self):
        value = randint(1000, 10000)
        return value

    def confirmation_mail(self,to_mail):
        otp = self.otp_generation()
        message = Mail(
            from_email= self.from_email,
            to_emails= to_mail,
            subject='Confirmation Mail',
            html_content= f'Here is your generated OTP : {otp}')
        try:
            response = self.sg.send(message)
            return otp
        except Exception as e:
            print("Exception:",e)
            return None

    def alert_overbudget(self, to_mail, budget, total_expense):
        message = Mail(
            from_email= self.from_email,
            to_emails= to_mail,
            subject='Alert : Exceeded Monthly Expense',
            html_content= f'Your budget is {budget}. But your expense exceeded to {total_expense}')
        try:
            response = self.sg.send(message)
            return True
        except Exception as e:
            print("Exception:",e)
            return False


# obj = SendGrid()

# # code = obj.confirmation_mail("jagadish19039@cse.ssn.edu.in")

# print(obj.otp_generation())