from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone 

class Customer(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    age = models.IntegerField(validators=[MinValueValidator(0)])
    phone = models.CharField(max_length = 10)
    salary = models.IntegerField()
    approved_limit = models.IntegerField()

    def __str__(self) :
        return self.first_name

class LoanData(models.Model) :
    customer = models.ForeignKey(Customer , on_delete = models.CASCADE)
    loan_amount = models.IntegerField()
    tenure = models.IntegerField()
    interest = models.DecimalField(max_digits = 5 , decimal_places = 2)
    monthly_payment = models.IntegerField()
    emi_paid_on_time = models.IntegerField()
    date_approved = models.DateField()
    loan_end_date = models.DateField()

    def is_active(self) :
        return self.date_approved <= timezone.now().date() <= self.loan_end_date
    
    def is_inactive(self):
        return self.loan_end_date <= timezone.now().date()

    def __str__(self) :
        return f"{self.customer.first_name} loan's info"