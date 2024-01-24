from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view 
from rest_framework.response import Response

from .models import Customer , LoanData
from .utils import *
from django.http import HttpResponse
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from .serializers import LoanListSerializer

@api_view(["POST"])
def register(request):
    if request.method == 'GET':
        return Response("only POST method allowed to register")
    customer = Customer(
        first_name = request.POST.get("first_name"),
        last_name = request.POST.get("last_name"),
        age = int(request.POST.get("age")),
        phone = int(request.POST.get("phone")),
        salary = int(request.POST.get("salary")),
        approved_limit = round( int(request.POST.get("salary")) * 36 , -5) 
    ) 
    customer.save()
    res = {
        "customer_id" : customer.id ,
        "name" : f"{customer.first_name} {customer.last_name}",
        "age":customer.age ,
        "monthly_income" :  customer.salary , 
        "approved_limit" : customer.approved_limit ,
        "phone_number" : customer.phone
    }
    return Response(res)


@api_view(["GET" , "POST"])
def is_eligible(request) :
    requested_loan_amt = int(request.POST.get("loan_amount"))
    cust_id = request.POST.get("customer_id")
    interest_rate = int(request.POST.get("interest_rate"))
    tenure = int(request.POST.get("tenure"))
    try:
        customer = get_object_or_404(Customer , id = cust_id)
    except Customer.DoesNotExist :
        res = {
            "error" : "first register this user to check eligibility",
            "approval":False
        }
        return Response(res)
    all_cust_loans = LoanData.objects.filter(customer = cust_id)
    active_loans = [loan for loan in all_cust_loans if loan.is_active()]
    total_monthly_payment = 0
    total_loan_amount = requested_loan_amt 
    for loan in active_loans : 
        total_monthly_payment += loan.monthly_payment
        total_loan_amount += loan.loan_amount
    if customer.salary/2 < total_monthly_payment or total_loan_amount >= customer.approved_limit :
        res = {
            "Approval failed" : "You have too many monthly payments on old loans",
            "approval":False
        }
        return Response(res)
    past_loans = [loan for loan in all_cust_loans if loan.is_inactive()]
    emi_paid_percentage = caluclate_emi_percentage(past_loans)
    emi_paid_score = calculate_emi_score(emi_paid_percentage)
    loan_count_score = calculate_loan_count_score(len(past_loans))
    credit_score = calulate_credit_score(emi_paid_score , loan_count_score)*10
    res = response_based_on_credit(credit_score,interest_rate,cust_id,tenure,requested_loan_amt)
    return Response(res)

@api_view(["POST"])
def createLoan(request) :
    res = is_eligible(request._request).data
    print(res)
    cust_id = request.POST.get("customer_id")
    loan_amt = request.POST.get("loan_amount")
    tenure = int(request.POST.get("tenure"))
    interest_rate = request.POST.get("interest_rate")
    if res["approval"] is False :
        response = {
            "approval":False ,
            "message":"Loan not approved see check eligiblity endpoint to see problem"
        }
        return Response(response)
    interest_rate = res["interest_rate"]

    loan = LoanData(
        customer = Customer.objects.get(id = cust_id) ,
        loan_amount = loan_amt ,
        tenure = tenure ,
        interest = interest_rate,
        monthly_payment = res["monthly_installment"],
        emi_paid_on_time= 0,
        date_approved = timezone.now().date(),
        loan_end_date = timezone.now().date() + relativedelta(months=tenure)
    )
    loan.save()
    response = {
        "cust_id" : cust_id,
        "approval":True,
        "loan_id":loan.id,
        "message":"Loan Approved and registered",
        "monthly_installment" : res["monthly_installment"]
    }
    return Response(response)

@api_view(["GET"])
def viewLoan(request , loan_id):
    try:
        loan = get_object_or_404(LoanData ,id = loan_id)
    except LoanData.DoesNotExist:
        print("wrong loan id")
        res = {
            "Wrong loan id" : "Loan Id is wrong Loan does not exist"
        }
        return Response(res)
    customer = {
        "customer_id" : loan.customer.id,
        "first_name" : loan.customer.first_name,
        "last_name" : loan.customer.last_name,
        "phone": loan.customer.phone,
        "age": loan.customer.age
    }
    res = {
        "loan_id" : loan.id,
        "customer" : customer,
        "loan_amount": loan.loan_amount,
        "interest_rate" : loan.interest,
        "monthly_installment" : loan.monthly_payment,
        "tenure":loan.tenure
    }
    return Response(res)

@api_view(["GET"])
def viewLoans(request , cust_id):
    loans = LoanData.objects.filter(customer = Customer.objects.get(id = cust_id))
    res = []
    if len(loans) == 0 :
        res = {
            "No loans":"No loans have been taken by this customer"
        }
        return Response(res)
    for loan in loans :
        dict = {
            "loan_id" : loan.id,
            "loan_amt" : loan.loan_amount,
            "interest_rate": loan.interest,
            "monthly_payment" : loan.monthly_payment,
            "repayments_left" : loan.tenure - loan.emi_paid_on_time
        }
        res.append(dict)
    serialized_data = LoanListSerializer(res , many = True).data
    return Response(serialized_data)
    
