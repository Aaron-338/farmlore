"""
Utility functions for the FarmLore community app.
"""
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

def notify_admins_about_application(application):
    """Notify administrators about a new knowledge keeper application."""
    admins = User.objects.filter(is_staff=True, is_active=True)
    admin_emails = [user.email for user in admins if user.email]
    
    if not admin_emails:
        return
    
    subject = f"New Knowledge Keeper Application: {application.user.username}"
    message = f"""
    A new knowledge keeper application has been submitted:
    
    User: {application.user.username}
    Full Name: {application.user.get_full_name() or 'Not provided'}
    Email: {application.user.email}
    Village: {application.village}
    District: {application.district}
    Years Experience: {application.years_experience}
    
    To review this application, please visit:
    {settings.SITE_URL if hasattr(settings, 'SITE_URL') else '[site url]'}/community/admin/applications/{application.pk}/
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            admin_emails,
            fail_silently=True,
        )
    except Exception as e:
        logger.exception("Failed to send admin notification about new application") 