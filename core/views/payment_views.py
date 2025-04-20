"""
Views related to payments and donations.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
import decimal
import uuid
from payments import get_payment_model, RedirectNeeded
from ..models import Payment
from ..forms import DonationForm

Payment = get_payment_model()


@login_required
def donate(request):
    """
    View for making donations
    """
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation_type = form.cleaned_data['donation_type']
            description = form.cleaned_data['description']
            
            # Set the amount based on donation type or custom amount
            amount = None
            
            # Check first for custom amount
            custom_amount = form.cleaned_data.get('custom_amount')
            if custom_amount:
                amount = custom_amount
            else:
                # Use predefined amounts based on donation type
                if donation_type == 'small':
                    amount = decimal.Decimal('5.00')
                elif donation_type == 'medium':
                    amount = decimal.Decimal('10.00')
                elif donation_type == 'large':
                    amount = decimal.Decimal('25.00')
                elif donation_type == 'extra_large':
                    amount = decimal.Decimal('50.00')
            
            # Generate unique payment description
            payment_description = f"Donation: {donation_type.capitalize()}"
            if description:
                payment_description += f" - {description}"
            
            # Create a unique token for this payment
            token = str(uuid.uuid4())
            
            # Create the payment
            payment = Payment.objects.create(
                variant='default',  # Using the dummy provider for testing
                description=payment_description,
                total=amount,
                tax=decimal.Decimal('0.00'),
                currency='USD',
                delivery=decimal.Decimal('0.00'),
                billing_first_name=request.user.username,
                billing_last_name='',
                billing_address_1='',
                billing_address_2='',
                billing_city='',
                billing_postcode='',
                billing_country_code='US',
                billing_country_area='',
                customer_ip_address=request.META.get('REMOTE_ADDR', ''),
                token=token,
                user=request.user
            )
            
            # Store the donation_type in extra_data
            payment.extra_data = {'donation_type': donation_type}
            payment.save(update_fields=['extra_data'])
            
            try:
                # Redirect to the payment processor
                return redirect('process_payment', payment_id=payment.id)
            except RedirectNeeded as redirect_to:
                return HttpResponseRedirect(str(redirect_to))
    else:
        form = DonationForm()
    
    return render(request, 'core/payments/payment_page.html', {
        'form': form,
        'title': 'Make a Donation',
        'page_type': 'donate'
    })


@login_required
def donation_confirmation(request):
    """
    Confirmation page after initiating a donation
    """
    return render(request, 'core/payments/payment_page.html', {
        'title': 'Donation Confirmation',
        'page_type': 'confirmation'
    })


@login_required
def payment_success(request):
    """
    Success page after a successful payment
    """
    return render(request, 'core/payments/payment_page.html', {
        'title': 'Payment Successful',
        'page_type': 'success'
    })


@login_required
def process_payment(request, payment_id):
    """
    Process a payment
    """
    payment = get_object_or_404(Payment, id=payment_id)
    
    # Only allow the payment owner to process it
    if payment.user != request.user:
        messages.error(request, 'You can only process your own payments.')
        return redirect('home')
    
    # Redirect to appropriate payment provider
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    
    return render(request, 'core/payments/payment_page.html', {
        'form': form,
        'payment': payment,
        'title': 'Process Payment',
        'page_type': 'process'
    })


@login_required
def payment_failure(request):
    """
    Failure page after a failed payment
    """
    return render(request, 'core/payments/payment_page.html', {
        'title': 'Payment Failed',
        'page_type': 'failure'
    })


@login_required
def donation_history(request):
    """
    View donation history for the current user
    """
    # Get all payments for the current user
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'core/payments/payment_page.html', {
        'payments': payments,
        'title': 'Donation History',
        'page_type': 'history'
    })