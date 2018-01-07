from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Letter
from .forms import LetterForm, LetterForm2
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Count, Sum, Q, Case, Value, When, IntegerField
import datetime

# Create your views here.
def home(request):
    # return render(request, 'base_ori.html')
    return render(request, 'base.html')

def letter_new(request):

    if request.method == "POST":
        # form = LetterForm(request.POST)
        form = LetterForm(request.POST)
        if form.is_valid():
            letter = form.save(commit=False)
            # letter.createdby = request.user
            letter.save()
            # return redirect('post_detail', pk=post.pk)
            messages.success(request, "Letter record with Reference Number : " + str(letter.pk) + " has been created ! ")
            return redirect(reverse_lazy('letter_home'))
            # return redirect(reverse_lazy('student_detail',kwargs={'pk': student.pk }))
    else:
        # form = LetterForm()
        form = LetterForm()
    
    return render(request, 'letter/letter_new.html', {'form': form})


# Letter JSON list filtering
class LetterListJson(BaseDatatableView):
    order_columns = ['letter_ref','letter_received','letter_date', 'letter_from', 'letter_desc','pk','link']

    def get_initial_queryset(self):
        # icnum = self.request.GET.get(u'icnum', '')
        # return Student.objects.filter(icnum=icnum)
        # return Student.objects.all().order_by('icnum')
        return Letter.objects.all().order_by('letter_ref')

    def filter_queryset(self, qs):

        # Getting advanced filtering indicators for dataTables 1.10.13
        search = self.request.GET.get(u'search[value]', "")
        iSortCol_0 = self.request.GET.get(u'order[0][column]', "") # Column number 0,1,2,3,4
        sSortDir_0 = self.request.GET.get(u'order[0][dir]', "") # asc, desc
        
        # Choose which column to sort
        if iSortCol_0 == '1':
          sortcol = 'letter_ref'
        elif iSortCol_0 == '2':
          sortcol = 'letter_date'
        elif iSortCol_0 == '3':
          sortcol = 'letter_from'
        elif iSortCol_0 == '4':
          sortcol = 'letter_desc'
        else:
          sortcol = 'letter_received'


        # Choose which sorting direction : asc or desc
        if sSortDir_0 == 'asc':
          sortdir = ''
        else:
          sortdir = '-'

        # Filtering if search value is key-in
        if search:
          # Initial Q parameter value
          qs_params = None

          # Filtering other fields
          q = Q(letter_ref__icontains=search)|Q(letter_from__icontains=search)
          qs_params = qs_params | q if qs_params else q
   
          # Completed Q queryset
          # print qs_params
          qs = qs.filter(qs_params)
          # print 'qs :' + str(qs)
          # print 'qs :'

        # print 'sortdir + sortcol : ' + sortdir + sortcol
        return qs.order_by(sortdir + sortcol)
        # return qs

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        # json_data = {}
        json_data = []
        # 'letter_ref','letter_received','letter_date', 'letter_from', 'letter_desc','pk','link'
        for item in qs:
            json_data.append([
                item.letter_ref,
                item.letter_received,
                item.letter_date,
                item.letter_from,
                item.letter_desc,
                str(item.pk),
                # reverse_lazy('student_detail',kwargs={'pk': str(item.pk)})
                reverse_lazy('letter_home'),
            ])
            # print(json_data)
        return json_data

