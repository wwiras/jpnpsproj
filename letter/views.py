from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Letter, LHistory, LAssignTo
from django.contrib import messages
from .forms import LetterForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Count, Sum, Q, Case, Value, When, IntegerField
import datetime


def home(request):
    # return render(request, 'base_ori.html')
    return render(request, 'base.html')

@login_required(login_url='/accounts/login/')
def home_json(request):
    # return render(request, 'base_ori.html')
    return render(request, 'letter/letter_home.html')

@login_required(login_url='/accounts/login/')
def letter_new(request):

    if request.method == "POST":
        # form = LetterForm(request.POST)
        form = LetterForm(request.POST)
        if form.is_valid():

            newletter = form.save(commit=False)
            assigntoform = form.cleaned_data.get('assigned_to')
            # print(assigntoform)
            # letter.createdby = request.user
            # print(letter.assigned_to)
            newletter.save()
            for a in assigntoform:
                assigntoobj = LAssignTo.objects.get(name=a)
                assigntoobj.letter_set.add(newletter)
            # print(form['assigned_to'])
            # letter.save_m2m()
            h = LHistory(userby=request.user, desc='Created')
            h.save()
            messages.success(request, "Letter record with Reference Number : " + str(newletter.letter_ref) + " has been created ! ")
            # return redirect(reverse_lazy('letter_home'))
            return redirect(reverse_lazy('letter_detail',kwargs={'pk': newletter.pk }))
    else:
        form = LetterForm()
    
    return render(request, 'letter/letter_new.html', {'form': form})

@login_required(login_url='/accounts/login/')
def letter_edit(request,pk):

    editletter = get_object_or_404(Letter, pk=pk)
    if request.method == "POST":
        form = LetterForm(request.POST,instance=editletter)
        if form.is_valid():
            
            # Letter table
            editletter = form.save(commit=False)
            editletter.save()

            # Updating Assign Table
            # print(editletter.assigned_to.all())
            editletter.assigned_to.clear()
            # LAssignTo.letter_set.remove(letter) #Remove all 
            assigntoform = form.cleaned_data.get('assigned_to')
            for a in assigntoform:
                a.letter_set.add(editletter)

            # Updating Letter history
            h = LHistory(userby=request.user, desc='Updated')
            h.save()
            messages.success(request, "Letter Reference : " + str(editletter.letter_ref) + " has been updated! ")
            return redirect(reverse_lazy('letter_detail',kwargs={'pk': editletter.pk }))
    else:
        # print(letter.letter_date)
        # print(datetime.datetime.strptime(str(letter.letter_date), '%Y-%m-%d').strftime('%m/%d/%y'))
        editletter.letter_date = datetime.date.strftime(editletter.letter_date, "%d-%m-%Y")
        editletter.letter_received = datetime.date.strftime(editletter.letter_received, "%d-%m-%Y")
        form = LetterForm(instance=editletter)
    
    return render(request, 'letter/letter_edit.html', {'form': form})

@login_required(login_url='/accounts/login/')
def letter_detail(request,pk):
    letter = get_object_or_404(Letter, pk=pk)
    # a = letter.assignto 
    return render(request, 'letter/letter_detail.html', {'letter': letter})

@login_required(login_url='/accounts/login/')
def letter_remove(request,pk):

    letter = get_object_or_404(Letter, pk=pk)
    if request.method == "POST":
        if request.POST.get("submit_yes", ""):
            letter_ref = letter.letter_ref
            letter.delete()
            messages.success(request, "Letter record with Reference : " + str(letter_ref) + " has been removed! ")
            return redirect(reverse_lazy('letter_home'))

    return render(request, 'letter/letter_confirm_delete.html', {'letter': letter, 'pk':pk})


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
          print(search)
          q = Q(letter_ref__icontains=search)|Q(letter_from__icontains=search)|Q(letter_desc__icontains=search)
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
                # item.letter_received,
                datetime.datetime.strptime(str(item.letter_received), '%Y-%m-%d').strftime('%d-%m-%Y'),
                # item.letter_date,
                datetime.datetime.strptime(str(item.letter_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                item.letter_from,
                item.letter_desc,
                str(item.pk),
                # reverse_lazy('student_detail',kwargs={'pk': str(item.pk)})
                reverse_lazy('letter_home'),
            ])
            # print(json_data)
        return json_data

