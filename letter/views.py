from django.shortcuts import render
# from django.utils import timezone
from .models import Letter
from .forms import LetterForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
# from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Count, Sum, Q, Case, Value, When, IntegerField

# Create your views here.
def home(request):
    return render(request, 'base_ori.html')

def letter_new(request):

    if request.method == "POST":
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
        form = LetterForm()
    
    return render(request, 'letter/letter_new.html', {'form': form})

