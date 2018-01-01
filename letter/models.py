from django.db import models


class LAssignTo(models.Model):
    name = models.CharField('Name',max_length=300)
    position = models.CharField('Position',max_length=300)
    desc = models.CharField('Description',max_length=300)

    def __str__(self):
            return self.name

class LHistory(models.Model):
	userby = models.ForeignKey('auth.User',on_delete=models.CASCADE)
	desc = models.CharField('Name',max_length=300)
	h_date = models.DateTimeField('Date Created/Updated',auto_now_add=True)

	def __str__(self):
                return self.userby


# Create your models here.
class Letter(models.Model):
    
    letter_received = models.DateTimeField('Letter Received',blank=False,null=False)
    letter_ref = models.CharField('Outside Ref. Number',unique=True,max_length=300,blank=False,null=False)
    sector_ref = models.CharField('Sector Ref. Number',unique=True,max_length=300,blank=True,null=True)
    letter_date = models.DateTimeField('Letter Date',blank=False,null=False)
    letter_from = models.CharField('Letter From',max_length=300,blank=False,null=False)
    letter_desc = models.TextField('Topics',blank=False,null=False)
    assigned_to = models.ForeignKey(LAssignTo,on_delete=models.CASCADE)
    created_date = models.DateTimeField('Date Key-In',auto_now_add=True)
    # icnum = models.CharField('ID Number',max_length=12,unique=True,blank=False,null=False)
    # name = models.TextField()
    # name = models.CharField('Name',max_length=300)
    # course = models.CharField('Courserwork',max_length=2,choices=COURSE_CHOICES,default=PCTECH,)
    

    def __str__(self):
    	return self.letter_ref
