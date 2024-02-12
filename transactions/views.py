from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import CreateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction
from .forms import DepositForm,WithdrawForm,LoanRequestForm
from .constants import DEPOSIT,WITHDRAWAL,LOAN,LOAN_PAID
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.db import Sum


# Create your views here.
#ei view ke deposit kore amara withdraw,deposit,loan_request korbo
class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    template_name =''
    model = Transaction
    title = ''
    success_url =''
    
    
    def get_form_kwargs(self) :
        kwargs =super().get_form_kwargs()
        kwargs.update({
            'account' :self.request.user.account,
        })
        return kwargs
    
    def get_context_data(self, **kwargs):
        context=  super().get_context_data(**kwargs)
        context.update(
            {
                'title':self.title
            }
        )
        
class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'
    
    def get_initial(self):
        initial ={
            'transaction_type':DEPOSIT
        }    
        return initial
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account =self.request.user.account
        account.balance +=amount
        account.save(
            
                update_fields =['balance']
        
        )
        messages.success(self.request,f" {amount}$ was deposited to your account successfully ")
        return super().form_valid(form)
    
class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw'
    
    def get_initial(self):
        initial ={
            'transaction_type':WITHDRAWAL
        }    
        return initial
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account =self.request.user.account
        account.balance -=amount
        account.save(
            
                update_fields =['balance']
        
        )
        messages.success(self.request,f"Successfully  {amount}$ was withdrawal from  your account  ")
        return super().form_valid(form)
    
    
class LoanRequestView(TransactionCreateMixin):
    form_class = LoanRequestForm
    title = 'Request for Loan'
    
    def get_initial(self):
        initial ={
            'transaction_type':LOAN
        }    
        return initial
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        current_loan_count =Transaction.objects.filter(account = self.request.user.acount ,transaction_type = LOAN,loan_approve =True).count()
        if current_loan_count >=3:
            return HttpResponse("You have crossed your loan request Limit")
        messages.success(self.request,f"Loan Request for  {amount}$ sent to admin.Wait for approval  ")
        return super().form_valid(form)
    

class TransactionReportView(LoginRequiredMixin,ListView):
    template_name = ""
    model = Transaction
    balance = 0
    
    def get_queryset(self) :
        #jodi user kono type filter na kore tobe tar total type transaction report dekhabo
        queryset = super().get_queryset().filter(
            account = self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            #Transactions.objects.get(account)
            self.balance = Transaction.objects.filter(timestamp_date_gte = start_date, timestamp_date_lte = end_date).aggregate(Sum('amount'))['amount__sum']
            # queryset = queryset.filter(timestamp_date_gte = start_date, timestamp_date_lte = end_date)
        else:
            self.balance = self.request.user.account.balance 
        return queryset.distinct()
      
    def get_context_data(self, **kwargs):
        context=  super().get_context_data(**kwargs)
        context.update(
            {
                'account':self.request.user.account 
            }
        )
        return context