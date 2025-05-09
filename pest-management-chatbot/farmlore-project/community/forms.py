from django import forms
from .models import KnowledgeKeeperApplication

class KnowledgeKeeperApplicationForm(forms.ModelForm):
    """Form for applying to become a knowledge keeper."""
    
    class Meta:
        model = KnowledgeKeeperApplication
        fields = ['village', 'district', 'years_experience', 'specialization', 'bio', 'reason']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'years_experience': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
        } 