from django import forms
from .models import Letter
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class LetterForm(forms.ModelForm):

    letter_date = forms.DateField(required=False, input_formats=['%d-%m-%Y'])
    letter_received = forms.DateField(required=False, input_formats=['%d-%m-%Y'])

    def __init__(self, *args, **kwargs):
        super(LetterForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # self.fields['description'].widget.attrs={ 'id': 'myCustomId', 'class': 'myCustomClass', 'name': 'myCustomName', 'placeholder': 'myCustomPlaceholder'}
        # source : https://stackoverflow.com/questions/19489699/how-to-add-class-id-placeholder-attributes-to-a-field-in-django-model-forms
        self.fields['letter_date'].widget.attrs={ 'class': 'mydatepicker','placeholder': 'DD-MM-YYYY'}
        self.fields['letter_received'].widget.attrs={ 'class': 'mydatepicker','placeholder': 'DD-MM-YYYY'}
        # self.fields['assigned_to'].empty_label = None
        # self.fields["assigned_to"].widget = forms.widgets.CheckboxSelectMultiple()

        # You can dynamically adjust your layout
        # self.helper.layout.append(Submit('save', 'save'))
        # self.helper = Layout(Field('letter_date', css_class='datepicker'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout.append(Submit('submit_change', 'Submit', css_class="btn-primary"))
        self.helper.layout.append(HTML('<a class="btn btn-primary" href={% url "letter_home" %}>Reset</a>'))

    class Meta:
        model = Letter
        fields = ('letter_ref', 'letter_date', 'letter_received', 'letter_from','letter_desc','assigned_to')

    # def save(self, commit=True):

        # child = super(ChildEditForm, self).save() # Save the child so we have an ID for the m2m
        # letter = super(LetterForm, self).save() # Save the child so we have an ID for the m2m

        # assigned_to = self.cleaned_data.get('assigned_to')
        # print(assigned_to)
        # for a in assigned_to:
        #     print(a)
        #     a.letter
        # family = Family.objects.get(slug=family_slug)
        # order = self.cleaned_data.get('order')
        # FamilyChild.objects.create(family=family, child=child, order=order)

        # new_store = Store(name='Midtown',address='844 W Washington St...')
        # new_store.save()
        # wifi_amenity.store_set.add(new_store)

        # return letter
        # letter_received = models.DateTimeField('Letter Received',blank=False,null=False)
        # letter_ref = models.CharField('Outside Ref. Number',unique=True,max_length=300,blank=False,null=False)
        # sector_ref = models.CharField('Sector Ref. Number',unique=True,max_length=300,blank=True,null=True)
        # letter_date = models.DateTimeField('Letter Date',blank=False,null=False)
        # letter_from = models.CharField('Letter From',max_length=300,blank=False,null=False)
        # letter_desc = models.TextField('Topics',blank=False,null=False)
        # assigned_to = models.ForeignKey(LAssignTo,on_delete=models.CASCADE)
        # created_date = models.DateTimeField('Date Key-In',auto_now_add=True)