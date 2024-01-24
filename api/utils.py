def calculate_emi(loan_amount, interest_rate, tenure):
    r = (interest_rate / 12) / 100  
    n = tenure  

    emi = loan_amount * r * ((1 + r)**n) / ((1 + r)**n - 1)
    return round(emi)

def calulate_credit_score(emi_paid_score , loan_count_score):
    weigth_emi_paid = 0.7
    weigth_loan_count = 0.3
    score = (emi_paid_score*weigth_emi_paid)+(loan_count_score*weigth_loan_count)
    return score

def calculate_loan_count_score(num_of_past_loans):

    score_range = [(10,10),(8,9) , (6,8),(4,7),(2,6)]

    for loans_taken , score in score_range:
        if num_of_past_loans >= loans_taken :
            return score
        
    return 4

def caluclate_emi_percentage(past_loans):
    total_teunre = 0
    emi_paid_on_time = 0
    if len(past_loans) == 0 : return 3
    for loan in past_loans :
        total_teunre += loan.tenure
        emi_paid_on_time += loan.emi_paid_on_time
    print("emi paid on time" , emi_paid_on_time , "total tenur" , total_teunre)
    percentage = (emi_paid_on_time/total_teunre)*100
    return round(percentage , 2)
    return percentage



def calculate_emi_score(emi_paid_percentage):
    # emi_paid_percentage = emi's paid on time / total emi's
    score_ranges = [(90, 10), (80, 9), (70, 8), (60, 7), (50, 6), (40, 5), (30, 4), (20, 3), (10, 2)]

    for percentage_range, score in score_ranges:
        if emi_paid_percentage >= percentage_range:
            return score
    return 1


def response_based_on_credit(credit_score , interest_rate , cust_id , tenure , requested_loan_amt):
    if credit_score <= 10 :
        res = {
            "Loan Failed" : "Credit score too low",
            "approval":False
        }
        return res
    elif 10 < credit_score <= 30 :
        res = {
            "customer_id": cust_id,
            "approval":True,
            "interest_rate":interest_rate,
            "corrected_interest_rate":"16%",
            "tenure":tenure,
            "monthly_installment":calculate_emi(requested_loan_amt, 16 , tenure)
        }
        return res
    elif 30 < credit_score <= 50 :
            res = {
            "customer_id": cust_id,
            "approval":True,
            "interest_rate":interest_rate,
            "corrected_interest_rate":"12%",
            "tenure":tenure,
            "monthly_installment":calculate_emi(requested_loan_amt, 12 , tenure)
            }
            return res

    res = {
            "customer_id": cust_id,
            "approval":True,
            "interest_rate":interest_rate,
            "corrected_interest_rate":interest_rate,
            "tenure":tenure,
            "monthly_installment":calculate_emi(requested_loan_amt, interest_rate , tenure)
        }
    return res