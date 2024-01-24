import pandas as pd
from django.core.management.base import BaseCommand
from pathlib import Path 
from api.models import Customer , LoanData
# from datetime import datetime 
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Command(BaseCommand):

    help = "This will be used to load data from customer_data and load_data files First load customer data then loan data " 

    def add_arguments(self , parser) :
        parser.add_argument("file_name" , help = "provide file name with extension")
    
    def handle(self ,*args ,**kwargs) :
        
        file_name = kwargs['file_name'] 
        file_path = str(BASE_DIR)+"/"+file_name
        
        try:
            df = pd.read_excel(file_path)
        except FileNotFoundError :
            self.stdout.write("File name is wrong")
            return 
        if file_name == "customer_data.xlsx":
            for i , row in df.iterrows() :
                customer = Customer(
                    id = row["Customer ID"],
                    first_name = row["First Name"],
                    last_name = row["Last Name"],
                    age = row["Age"],
                    phone = row["Phone Number"],
                    salary = row["Monthly Salary"],
                    approved_limit = row["Approved Limit"]
                )
                self.stdout.write(f"Info for {customer.first_name} added")
                customer.save()
        elif file_name == "loan_data.xlsx" :
            for i , row in df.iterrows():
                loan_data = LoanData(
                    id = row["Loan ID"],
                    customer = Customer.objects.get(id = row["Customer ID"]),
                    loan_amount = row["Loan Amount"],
                    tenure = row["Tenure"],
                    interest = row["Interest Rate"],
                    monthly_payment = row["Monthly payment"],
                    emi_paid_on_time = row["EMIs paid on Time"],
                    date_approved = row["Date of Approval"],
                    loan_end_date = row["End Date"]
                )
                self.stdout.write(f"load id {loan_data.id} added")
                loan_data.save()
            return 
        else : 
            self.stdout.write("Wrong file name")
                

    