"""
Views for the FarmLore community features.

These views provide the API endpoints and web interface for the community features,
allowing knowledge keepers to share indigenous technical knowledge and
community members to validate and access this knowledge.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Avg, Count
from django.db import transaction
import traceback
import json
import time
import logging
from functools import wraps

from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import (
    KnowledgeKeeper, IndigenousKnowledge, RegionalObservation, 
    CommunityValidation, SesothoTerm, KnowledgeKeeperApplication,
    UserProfile
)
from .serializers import (
    KnowledgeKeeperSerializer, IndigenousKnowledgeSerializer, 
    RegionalObservationSerializer, CommunityValidationSerializer,
    SesothoTermSerializer
)
from .knowledge_exporter import (
    export_validated_knowledge_to_prolog, 
    check_knowledge_base_includes_community,
    update_main_knowledge_base
)
from .forms import KnowledgeKeeperApplicationForm

import os
from datetime import datetime
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
logger = logging.getLogger(__name__)

# Custom permission decorators
def role_required(allowed_roles):
    """
    Decorator for views that checks if the user has one of the specified roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            logger.info(f"[role_required] Checking access for user: {request.user}")
            logger.info(f"[role_required] User authenticated: {request.user.is_authenticated}")
            
            if not hasattr(request.user, 'profile'):
                logger.warning(f"[role_required] Access DENIED for {request.user}: User has no 'profile' attribute.")
                return HttpResponseForbidden("You don't have permission to access this page (profile missing)")
            
            user_role = request.user.profile.role
            logger.info(f"[role_required] User role: {user_role}")
            logger.info(f"[role_required] Required roles: {allowed_roles}")
            
            if user_role not in allowed_roles:
                logger.warning(f"[role_required] Access DENIED for {request.user} (role: {user_role}). Required: {allowed_roles}")
                return HttpResponseForbidden(f"This feature requires one of these roles: {', '.join(allowed_roles)}")
            
            logger.info(f"[role_required] Access GRANTED for {request.user} (role: {user_role})")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def knowledge_keeper_required(view_func):
    """Decorator for views that require knowledge keeper role."""
    return role_required(['knowledge_keeper', 'administrator'])(view_func)

def community_member_required(view_func):
    """Decorator for views that require at least community member role."""
    return role_required(['community_member', 'knowledge_keeper', 'administrator'])(view_func)

def administrator_required(view_func):
    """Decorator for views that require administrator role."""
    return role_required(['administrator'])(view_func)

def debug_to_file(message, data=None):
    """Write debug information to a file."""
    debug_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'debug_logs')
    os.makedirs(debug_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = os.path.join(debug_dir, f'debug_{timestamp}.log')
    
    with open(filename, 'w') as f:
        f.write(f"DEBUG MESSAGE: {message}\n\n")
        if data:
            f.write("DATA:\n")
            if isinstance(data, dict):
                f.write(json.dumps(data, indent=2, default=str))
            else:
                f.write(str(data))

# API Views

class KnowledgeKeeperViewSet(viewsets.ModelViewSet):
    """API endpoint for knowledge keepers."""
    queryset = KnowledgeKeeper.objects.all()
    serializer_class = KnowledgeKeeperSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'village', 'district', 'specialization']
    
    @action(detail=True, methods=['get'])
    def knowledge_entries(self, request, pk=None):
        """Get all knowledge entries for a specific knowledge keeper."""
        keeper = self.get_object()
        entries = keeper.knowledge_entries.all()
        serializer = IndigenousKnowledgeSerializer(entries, many=True)
        return Response(serializer.data)

class IndigenousKnowledgeViewSet(viewsets.ModelViewSet):
    """API endpoint for indigenous knowledge entries."""
    queryset = IndigenousKnowledge.objects.all()
    serializer_class = IndigenousKnowledgeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'practice_type', 'crops', 'pests']
    
    @action(detail=False, methods=['get'])
    def verified(self, request):
        """Get all verified knowledge entries."""
        verified = IndigenousKnowledge.objects.filter(verification_status='verified')
        serializer = self.get_serializer(verified, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_practice_type(self, request):
        """Get knowledge entries grouped by practice type."""
        practice_types = IndigenousKnowledge.PRACTICE_TYPES
        result = {}
        
        for code, name in practice_types:
            entries = IndigenousKnowledge.objects.filter(practice_type=code)
            serializer = self.get_serializer(entries, many=True)
            result[code] = {
                'name': name,
                'entries': serializer.data
            }
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def by_crop(self, request):
        """Get knowledge entries for a specific crop."""
        crop = request.query_params.get('crop', None)
        if crop is None:
            return Response(
                {"error": "Crop parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filter entries where the crop is in the crops list
        entries = IndigenousKnowledge.objects.filter(crops__contains=[crop])
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_pest(self, request):
        """Get knowledge entries for a specific pest."""
        pest = request.query_params.get('pest', None)
        if pest is None:
            return Response(
                {"error": "Pest parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filter entries where the pest is in the pests list
        entries = IndigenousKnowledge.objects.filter(pests__contains=[pest])
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def export_to_prolog(self, request, pk=None):
        """Export a specific knowledge entry to Prolog format."""
        knowledge = self.get_object()
        if knowledge.verification_status != 'verified':
            return Response(
                {"error": "Only verified knowledge can be exported to Prolog"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Export the knowledge to Prolog
        try:
            export_validated_knowledge_to_prolog()
            return Response({"success": "Knowledge exported to Prolog successfully"})
        except Exception as e:
            return Response(
                {"error": f"Failed to export knowledge to Prolog: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RegionalObservationViewSet(viewsets.ModelViewSet):
    """API endpoint for regional observations."""
    queryset = RegionalObservation.objects.all()
    serializer_class = RegionalObservationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'observation_type', 'village', 'district', 'crops_affected']
    
    @action(detail=False, methods=['get'])
    def by_district(self, request):
        """Get observations grouped by district."""
        observations = RegionalObservation.objects.values('district').annotate(
            count=Count('id')
        ).order_by('district')
        
        result = {}
        for item in observations:
            district = item['district']
            district_observations = RegionalObservation.objects.filter(district=district)
            serializer = self.get_serializer(district_observations, many=True)
            result[district] = {
                'count': item['count'],
                'observations': serializer.data
            }
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get observations grouped by observation type."""
        observation_types = RegionalObservation.OBSERVATION_TYPES
        result = {}
        
        for code, name in observation_types:
            observations = RegionalObservation.objects.filter(observation_type=code)
            serializer = self.get_serializer(observations, many=True)
            result[code] = {
                'name': name,
                'observations': serializer.data
            }
        
        return Response(result)

class CommunityValidationViewSet(viewsets.ModelViewSet):
    """API endpoint for community validations."""
    queryset = CommunityValidation.objects.all()
    serializer_class = CommunityValidationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_validations(self, request):
        """Get all validations by the current user."""
        validations = CommunityValidation.objects.filter(validator=request.user)
        serializer = self.get_serializer(validations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def for_knowledge(self, request):
        """Get all validations for a specific knowledge entry."""
        knowledge_id = request.query_params.get('knowledge_id', None)
        if knowledge_id is None:
            return Response(
                {"error": "Knowledge ID parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validations = CommunityValidation.objects.filter(knowledge_id=knowledge_id)
        serializer = self.get_serializer(validations, many=True)
        return Response(serializer.data)

class SesothoTermViewSet(viewsets.ModelViewSet):
    """API endpoint for Sesotho terms."""
    queryset = SesothoTerm.objects.all()
    serializer_class = SesothoTermSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['term', 'english', 'description']

# Web Views

@method_decorator(login_required, name='dispatch')
class CommunityDashboardView(ListView):
    """Dashboard view for the community interface."""
    model = IndigenousKnowledge
    template_name = 'community/dashboard.html'
    context_object_name = 'knowledge_entries'
    paginate_by = 10
    
    def get_queryset(self):
        """Get the queryset for the dashboard."""
        # Explicitly order by newest first and include all entries regardless of status
        # Force a database query by calling .all() to avoid any caching issues
        queryset = IndigenousKnowledge.objects.all().order_by('-date_added')
        logger.info(f"Dashboard queryset count: {queryset.count()}")
        
        # Debug all knowledge entries
        entries_data = []
        for entry in queryset:
            entries_data.append({
                "id": entry.id,
                "title": entry.title,
                "keeper": str(entry.keeper),
                "verification_status": entry.verification_status,
                "verification_count": entry.verification_count,
                "date_added": str(entry.date_added)
            })
        debug_to_file("All knowledge entries in dashboard", entries_data)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Get the context data for the dashboard."""
        context = super().get_context_data(**kwargs)
        
        # Get counts for different verification statuses
        verified_count = IndigenousKnowledge.objects.filter(
            verification_status='verified'
        ).count()
        pending_count = IndigenousKnowledge.objects.filter(
            verification_status='pending'
        ).count()
        
        context['verified_count'] = verified_count
        context['pending_count'] = pending_count
        
        logger.info(f"Dashboard counts - Verified: {verified_count}, Pending: {pending_count}")
        
        # Add regional observations to the context
        recent_observations = RegionalObservation.objects.all().order_by('-date_added')[:5]
        context['recent_observations'] = recent_observations
        logger.info(f"Dashboard recent observations count: {recent_observations.count()}")
        
        # Add user's own contributions
        if self.request.user.is_authenticated:
            try:
                user_keeper = self.request.user.knowledge_keeper
                user_entries = IndigenousKnowledge.objects.filter(
                    keeper=user_keeper
                ).order_by('-date_added')
                
                # Debug user entries
                user_entries_data = []
                for entry in user_entries:
                    user_entries_data.append({
                        "id": entry.id,
                        "title": entry.title,
                        "verification_status": entry.verification_status,
                        "verification_count": entry.verification_count,
                        "date_added": str(entry.date_added)
                    })
                debug_to_file("User's knowledge entries", user_entries_data)
                
                context['user_entries'] = user_entries
            except KnowledgeKeeper.DoesNotExist:
                context['user_entries'] = []
                logger.info(f"User {self.request.user.username} does not have a knowledge keeper profile")
                
            # Add entries pending validation (entries the user hasn't validated yet)
            # First, get all entries the user has already validated
            validated_entries = IndigenousKnowledge.objects.filter(
                validations__validator=self.request.user
            ).values_list('id', flat=True)
            
            # Then, get all pending entries that the user hasn't validated yet
            # and that weren't created by the user
            pending_validation = IndigenousKnowledge.objects.filter(
                verification_status='pending'
            ).exclude(
                id__in=validated_entries
            )
            
            # If the user has a keeper profile, exclude their own entries
            try:
                user_keeper = self.request.user.knowledge_keeper
                pending_validation = pending_validation.exclude(keeper=user_keeper)
            except KnowledgeKeeper.DoesNotExist:
                pass
                
            context['pending_validation'] = pending_validation
        
        return context

@method_decorator(login_required, name='dispatch')
class KnowledgeDetailView(DetailView):
    """Detail view for an indigenous knowledge entry."""
    model = IndigenousKnowledge
    template_name = 'community/knowledge_detail.html'
    context_object_name = 'knowledge'
    
    def get_context_data(self, **kwargs):
        """Get the context data for the knowledge detail view."""
        context = super().get_context_data(**kwargs)
        context['validations'] = self.object.validations.all()
        context['validation_count'] = context['validations'].count()
        context['average_rating'] = context['validations'].aggregate(
            avg=Avg('rating')
        )['avg'] or 0
        
        # Check if the current user has already validated this knowledge
        user_validation = None
        if self.request.user.is_authenticated:
            try:
                user_validation = CommunityValidation.objects.get(
                    knowledge=self.object,
                    validator=self.request.user
                )
            except CommunityValidation.DoesNotExist:
                pass
        
        context['user_validation'] = user_validation
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(knowledge_keeper_required, name='dispatch')
class KnowledgeCreateView(CreateView):
    """Create view for an indigenous knowledge entry."""
    model = IndigenousKnowledge
    template_name = 'community/knowledge_form.html'
    fields = ['title', 'description', 'practice_type', 'materials', 'crops', 'pests', 'seasons']
    
    def get_success_url(self):
        """Return the URL to redirect to after successful form submission."""
        messages.success(self.request, f'Your knowledge entry "{self.object.title}" has been successfully submitted and is now awaiting verification.')
        # Add a timestamp parameter to force a fresh page load
        return reverse_lazy('community:dashboard') + f'?new_entry={int(time.time())}'
    
    def get_form(self, form_class=None):
        """Get the form and set initial values for JSONFields."""
        form = super().get_form(form_class)
        # Initialize empty lists for JSONFields
        form.initial.setdefault('materials', [])
        form.initial.setdefault('crops', [])
        form.initial.setdefault('pests', [])
        form.initial.setdefault('seasons', [])
        return form
    
    def form_invalid(self, form):
        """Handle invalid form submission."""
        logger.error(f"Form validation failed for user {self.request.user.username}")
        logger.error(f"Form errors: {form.errors}")
        
        # Log the raw POST data for debugging
        logger.error(f"Raw POST data: {self.request.POST}")
        
        # Log each field's value for debugging
        for field_name in self.fields:
            field_value = self.request.POST.get(field_name, 'NOT FOUND')
            logger.error(f"Field '{field_name}': {field_value}")
        
        # Create a more detailed error message for the user
        error_message = "There was an error with your submission. "
        if form.errors:
            error_message += "The following fields have errors: " + ", ".join(form.errors.keys())
        else:
            error_message += "Please check the form and try again."
        
        messages.error(self.request, error_message)
        return super().form_invalid(form)
    
    def post(self, request, *args, **kwargs):
        """Override post method to handle JSON fields properly."""
        # Create a mutable copy of POST data
        post_data = request.POST.copy()
        
        # Handle JSON fields
        for field in ['materials', 'crops', 'pests', 'seasons']:
            values = request.POST.getlist(field)
            if values:
                # Convert the list to a JSON string
                post_data[field] = json.dumps(values)
                logger.info(f"Converted {field} to JSON: {post_data[field]}")
        
        # Replace the POST data with our modified version
        request.POST = post_data
        
        # Continue with normal processing
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Set the keeper to the current user's knowledge keeper profile."""
        # Log the form data for debugging
        logger.info(f"Knowledge form submission received from user: {self.request.user.username}")
        logger.info(f"Form data: {form.cleaned_data}")
        logger.info(f"Raw POST data: {self.request.POST}")
        
        # Ensure user has a knowledge keeper profile
        try:
            keeper = self.request.user.knowledge_keeper
            logger.info(f"Found existing knowledge keeper: {keeper}")
        except KnowledgeKeeper.DoesNotExist:
            # If the user doesn't have a knowledge keeper profile, create one
            keeper = KnowledgeKeeper.objects.create(
                user=self.request.user,
                village='Unknown',
                district='Unknown',
                years_experience=0
            )
            logger.info(f"Created new knowledge keeper profile for user: {self.request.user.username}")
        
        form.instance.keeper = keeper
        
        # Ensure JSONFields are properly handled
        # These fields come from Select2 as lists, but we need to ensure they're saved as lists
        for field in ['materials', 'crops', 'pests', 'seasons']:
            # Get values from form.cleaned_data (should now be proper JSON)
            value = form.cleaned_data.get(field, [])
            logger.info(f"Processing {field} value from cleaned_data: {value}")
            
            # Ensure it's a list
            if isinstance(value, str):
                try:
                    # Try to parse JSON string
                    value = json.loads(value)
                except json.JSONDecodeError:
                    # If not valid JSON, split by comma
                    value = [v.strip() for v in value.split(',') if v.strip()]
            
            # Set the value on the instance
            setattr(form.instance, field, value if value else [])
            logger.info(f"Set {field} to: {getattr(form.instance, field)}")
        
        # Set verification status explicitly to ensure it's properly saved
        form.instance.verification_status = 'pending'
        form.instance.verification_count = 0
        
        try:
            # Save the form and get the result
            with transaction.atomic():
                result = super().form_valid(form)
                
                # Log the successful creation
                logger.info(f"Successfully created knowledge entry: {form.instance.id} - {form.instance.title}")
                
                # Force a refresh from the database to ensure we have the latest data
                self.object.refresh_from_db()
                
                # Explicitly log the keeper to verify it's set correctly
                logger.info(f"Entry keeper: {self.object.keeper} (User: {self.request.user.username})")
                
                # Log the final state of the JSONFields
                for field in ['materials', 'crops', 'pests', 'seasons']:
                    logger.info(f"Final {field} values: {getattr(self.object, field)}")
                
                return result
        except Exception as e:
            # Log the error
            logger.error(f"Error saving knowledge entry: {str(e)}")
            logger.error(traceback.format_exc())
            messages.error(self.request, f"An error occurred while saving your knowledge entry: {str(e)}")
            return self.form_invalid(form)

@method_decorator(login_required, name='dispatch')
@method_decorator(community_member_required, name='dispatch')
class ValidationCreateView(CreateView):
    """Create view for a community validation."""
    model = CommunityValidation
    template_name = 'community/validation_form.html'
    fields = ['rating', 'comments', 'has_used']
    
    def get_context_data(self, **kwargs):
        """Add knowledge object to the template context."""
        context = super().get_context_data(**kwargs)
        knowledge_id = self.kwargs.get('knowledge_id')
        context['knowledge'] = get_object_or_404(IndigenousKnowledge, pk=knowledge_id)
        return context
    
    def get(self, request, *args, **kwargs):
        """Check if the user has already validated this knowledge entry."""
        knowledge_id = self.kwargs.get('knowledge_id')
        knowledge = get_object_or_404(IndigenousKnowledge, pk=knowledge_id)
        
        # Check if the user has already validated this knowledge
        existing_validation = CommunityValidation.objects.filter(
            knowledge=knowledge,
            validator=request.user
        ).first()
        
        if existing_validation:
            messages.info(request, _('You have already validated this knowledge entry. You cannot validate it again.'))
            return redirect('community:knowledge_detail', pk=knowledge_id)
            
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """Handle POST requests: check for existing validation before processing."""
        knowledge_id = self.kwargs.get('knowledge_id')
        knowledge = get_object_or_404(IndigenousKnowledge, pk=knowledge_id)
        
        # Check if the user has already validated this knowledge
        existing_validation = CommunityValidation.objects.filter(
            knowledge=knowledge,
            validator=request.user
        ).first()
        
        if existing_validation:
            messages.info(request, _('You have already validated this knowledge entry. You cannot validate it again.'))
            return redirect('community:knowledge_detail', pk=knowledge_id)
            
        return super().post(request, *args, **kwargs)
    
    def get_success_url(self):
        """Get the URL to redirect to after successful form submission."""
        return reverse_lazy('community:knowledge_detail', kwargs={'pk': self.kwargs['knowledge_id']})
    
    def form_valid(self, form):
        """Set the knowledge and validator for the validation."""
        knowledge = get_object_or_404(IndigenousKnowledge, pk=self.kwargs['knowledge_id'])
        form.instance.knowledge = knowledge
        form.instance.validator = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
@method_decorator(community_member_required, name='dispatch')
class ObservationCreateView(CreateView):
    """Create view for a regional observation."""
    model = RegionalObservation
    template_name = 'community/observation_form.html'
    fields = ['title', 'description', 'observation_type', 'location', 'date_observed']
    success_url = reverse_lazy('community:dashboard')
    
    def form_invalid(self, form):
        """Handle invalid form submission."""
        logger.error(f"Observation form validation failed for user {self.request.user.username}")
        logger.error(f"Form errors: {form.errors}")
        
        # Log the raw POST data for debugging
        logger.error(f"Raw POST data: {self.request.POST}")
        
        # Log each field's value for debugging
        for field_name in self.fields:
            field_value = self.request.POST.get(field_name, 'NOT FOUND')
            logger.error(f"Field '{field_name}': {field_value}")
        
        # Create a more detailed error message for the user
        error_message = "There was an error with your observation submission. "
        if form.errors:
            error_message += "The following fields have errors: " + ", ".join(form.errors.keys())
        else:
            error_message += "Please check the form and try again."
        
        messages.error(self.request, error_message)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        """Set the observer to the current user."""
        # Log the form data for debugging
        logger.info(f"Observation form submission received from user: {self.request.user.username}")
        logger.info(f"Form data: {form.cleaned_data}")
        logger.info(f"Raw POST data: {self.request.POST}")
        
        # Set the observer to the current user
        form.instance.observer = self.request.user
        
        try:
            # Save the form and get the result
            with transaction.atomic():
                result = super().form_valid(form)
                
                # Log the successful creation
                logger.info(f"Successfully created observation: {form.instance.id} - {form.instance.title}")
                
                # Force a refresh from the database to ensure we have the latest data
                self.object.refresh_from_db()
                
                # Add success message
                messages.success(self.request, f'Your observation "{self.object.title}" has been successfully submitted.')
                
                return result
        except Exception as e:
            # Log the error
            logger.error(f"Error saving observation: {str(e)}")
            logger.error(traceback.format_exc())
            messages.error(self.request, f"An error occurred while saving your observation: {str(e)}")
            return self.form_invalid(form)

@login_required
@knowledge_keeper_required
def export_knowledge_view(request):
    """View to export all verified knowledge to Prolog. Only accessible by administrators."""
    # Check if user is an admin
    if not request.user.is_superuser:
        messages.error(request, _('You do not have permission to access this page.'))
        return redirect('community:dashboard')
        
    if request.method == 'POST':
        try:
            # Export the knowledge to Prolog
            output_file = export_validated_knowledge_to_prolog()
            
            # Update the main knowledge base if needed
            if not check_knowledge_base_includes_community():
                update_main_knowledge_base()
                
            return JsonResponse({
                'success': True, 
                'message': 'Knowledge exported successfully to Prolog format',
                'file_path': output_file
            })
        except Exception as e:
            logger.error(f"Error exporting knowledge: {str(e)}")
            return JsonResponse({
                'success': False, 
                'message': f'Error exporting knowledge: {str(e)}'
            })
    
    # Get verified knowledge entries for display
    verified_entries = IndigenousKnowledge.objects.filter(verification_status='verified')
    
    # Get counts for the template
    verified_count = verified_entries.count()
    exported_count = IndigenousKnowledge.objects.filter(is_exported=True).count()
    
    # Check if the knowledge base includes community knowledge
    kb_includes_community = check_knowledge_base_includes_community()
    
    # Get the last export time from exported entries
    last_export = IndigenousKnowledge.objects.filter(last_exported__isnull=False).order_by('-last_exported').first()
    last_export_time = last_export.last_exported if last_export else None
    
    context = {
        'verified_entries': verified_entries,
        'verified_count': verified_count,
        'exported_count': exported_count,
        'kb_includes_community': kb_includes_community,
        'last_export': last_export_time
    }
    
    return render(request, 'community/export_knowledge.html', context)

@login_required
@administrator_required
def debug_knowledge_view(request):
    """Debug view to show all knowledge entries in the database. Only accessible by administrators."""
    # Check if user is an admin
    if not request.user.is_superuser:
        messages.error(request, _('You do not have permission to access this page.'))
        return redirect('community:dashboard')
    
    entries = IndigenousKnowledge.objects.all().order_by('-date_added')
    
    data = []
    for entry in entries:
        data.append({
            'id': entry.id,
            'title': entry.title,
            'keeper': str(entry.keeper),
            'verification_status': entry.verification_status,
            'verification_count': entry.verification_count,
            'date_added': str(entry.date_added)
        })
    
    return JsonResponse({'entries': data})

@login_required
def apply_knowledge_keeper(request):
    """View for users to apply to become knowledge keepers."""
    # Check if user already has an application
    existing_app = KnowledgeKeeperApplication.objects.filter(user=request.user, status='pending').first()
    if existing_app:
        messages.info(request, _('You already have a pending application. We\'ll notify you when it\'s reviewed.'))
        return redirect('community:dashboard')
        
    # Check if user is already a knowledge keeper
    if hasattr(request.user, 'knowledge_keeper'):
        messages.info(request, _('You are already registered as a knowledge keeper.'))
        return redirect('community:dashboard')
    
    if request.method == 'POST':
        form = KnowledgeKeeperApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            
            # Notify admins about new application
            from .utils import notify_admins_about_application
            notify_admins_about_application(application)
            
            messages.success(request, _('Your application has been submitted. We\'ll review it and get back to you soon.'))
            return redirect('community:dashboard')
    else:
        form = KnowledgeKeeperApplicationForm()
    
    return render(request, 'community/apply_knowledge_keeper.html', {'form': form})

@login_required
@administrator_required
def admin_application_list(request):
    """View for admins to see all knowledge keeper applications."""
    if not request.user.is_staff:
        messages.error(request, _('You do not have permission to access this page.'))
        return redirect('community:dashboard')
    
    applications = KnowledgeKeeperApplication.objects.all()
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        applications = applications.filter(status=status)
    
    return render(request, 'community/admin_application_list.html', {
        'applications': applications,
        'current_status': status,
    })

@login_required
@administrator_required
def admin_application_detail(request, pk):
    """View for admins to review a specific application."""
    if not request.user.is_staff:
        messages.error(request, _('You do not have permission to access this page.'))
        return redirect('community:dashboard')
    
    application = get_object_or_404(KnowledgeKeeperApplication, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        notes = request.POST.get('notes', '')
        
        if action == 'approve':
            application.approve(request.user)
            messages.success(request, _('Application approved. The user is now a knowledge keeper.'))
        elif action == 'reject':
            application.reject(request.user, notes)
            messages.success(request, _('Application rejected. The user has been notified.'))
        
        return redirect('community:admin_application_list')
    
    return render(request, 'community/admin_application_detail.html', {
        'application': application,
    })
