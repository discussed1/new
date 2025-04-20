"""
Utility views for the application.
"""
from django.shortcuts import render
from django.http import JsonResponse
import sentry_sdk


def sentry_status(request):
    """
    View to check Sentry integration status
    """
    is_enabled = bool(sentry_sdk.Hub.current.client)
    
    context = {
        'sentry_enabled': is_enabled,
        'title': 'Sentry Status',
    }
    
    return render(request, 'core/utils/sentry_status.html', context)


def sentry_test(request):
    """
    Test Sentry error reporting
    """
    try:
        # Intentionally raise an exception to test Sentry
        raise Exception("This is a test exception for Sentry")
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return JsonResponse({
            'status': 'error_reported',
            'message': 'Test error reported to Sentry!'
        })