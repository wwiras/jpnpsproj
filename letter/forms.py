from django import forms
from .models import Letter
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class LetterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LetterForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        # self.helper.layout.append(Submit('save', 'save'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout.append(Submit('submit_change', 'Submit', css_class="btn-primary"))
        self.helper.layout.append(HTML('<a class="btn btn-primary" href={% url "letter_home" %}>Reset</a>'))

    class Meta:
        model = Letter
        fields = ('letter_ref', 'letter_date', 'letter_received', 'letter_from','letter_desc','assigned_to')


        # letter_received = models.DateTimeField('Letter Received',blank=False,null=False)
        # letter_ref = models.CharField('Outside Ref. Number',unique=True,max_length=300,blank=False,null=False)
        # sector_ref = models.CharField('Sector Ref. Number',unique=True,max_length=300,blank=True,null=True)
        # letter_date = models.DateTimeField('Letter Date',blank=False,null=False)
        # letter_from = models.CharField('Letter From',max_length=300,blank=False,null=False)
        # letter_desc = models.TextField('Topics',blank=False,null=False)
        # assigned_to = models.ForeignKey(LAssignTo,on_delete=models.CASCADE)
        # created_date = models.DateTimeField('Date Key-In',auto_now_add=True)