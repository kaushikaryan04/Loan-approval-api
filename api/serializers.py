from rest_framework import serializers

class LoanListSerializer(serializers.Serializer):
    loan_id = serializers.IntegerField()
    loan_amt = serializers.IntegerField()
    interest_rate = serializers.IntegerField()
    monthly_payment = serializers.IntegerField()
    repayments_left = serializers.IntegerField()