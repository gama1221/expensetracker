from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer
from .permissions import IsOwnerOrAdmin
from django.db.models import Sum

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AnalyticsView(APIView):
    def get(self, request):
        category_summary = Expense.objects.values('category').annotate(total=Sum('amount'))
        monthly_summary = Expense.objects.filter(date__year=2023).values('date__month').annotate(total=Sum('amount'))
        highest_spending_category = Expense.objects.values('category').annotate(total=Sum('amount')).order_by('-total').first()
        highest_single_expense = Expense.objects.order_by('-amount').first()

        data = {
            "category_summary": {item['category']: item['total'] for item in category_summary},
            "monthly_summary": {str(item['date__month']): item['total'] for item in monthly_summary},
            "highest_spending_category": highest_spending_category['category'],
            "highest_single_expense": {
                "title": highest_single_expense.title,
                "amount": highest_single_expense.amount,
                "category": highest_single_expense.category,
                "date": highest_single_expense.date
            }
        }
        return Response(data)
