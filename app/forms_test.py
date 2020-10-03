from django import forms
from app.models.objectmodel import wmobject_details,wmobject,wmobject_rel_notes

class wmobject_details_form(forms.ModelForm):
    class Meta:
        model= wmobject_details
        fields = ['object_type','object_path','object_backout','object_special','object_comment']
        widgets = { 'object_path': forms.TextInput(attrs={'class':'input-control mx-0 my-0 w-100'}),
                    'object_backout': forms.TextInput(attrs={'class':'input-control mx-0 my-0 w-100'}),
                    'object_special': forms.TextInput(attrs={'class':'input-control mx-0 my-0 w-100'}),
                    'object_comment': forms.TextInput(attrs={'class':'input-control mx-0 my-0 w-100'}),
                    'object_type': forms.Select(attrs={'class':'input-control mx-0 my-0 w-100'}),
                  
                    }


class rel_notes_form(forms.ModelForm):
    class Meta:
        model= wmobject_rel_notes
        fields = ['app_imp','proc_imp','objective','resolution','img1','img2','img3']
        widgets = { 'app_imp': forms.TextInput(attrs={'class':'form-control mx-0 my-0 w-100'}),
                    'proc_imp': forms.TextInput(attrs={'class':'form-control mx-0 my-0  w-100'}),
                    'objective': forms.TextInput(attrs={'class':'form-control mx-0 my-0 w-100 h-100'}),
                    'resolution': forms.TextInput(attrs={'class':'form-control mx-0 my-0 w-100 h-100'}),
                 }
