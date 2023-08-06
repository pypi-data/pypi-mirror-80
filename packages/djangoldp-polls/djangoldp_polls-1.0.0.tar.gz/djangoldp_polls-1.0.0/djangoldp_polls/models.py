from django.conf import settings
from django.db import models
from djangoldp.models import Model
from django.db.models import Sum
from django.contrib.auth import get_user_model

from djangoldp_conversation.models import Conversation
from djangoldp_circle.models import Circle

# User = settings.AUTH_USER_MODEL
# User.name=User.get_full_name

#========================

#========================

class Tag (Model):
	name = models.CharField(max_length=250,verbose_name="Name")

	class Meta :
		serializer_fields = ['@id','name']
		anonymous_perms = ['view']
		authenticated_perms = ['inherit','add']

	def __str__(self):
		return self.name


class PollOption (Model):
	name = models.CharField(max_length=250,verbose_name="Options available for a vote")

	class Meta :
		serializer_fields = ['@id','name']
		nested_fields = ['userVote','relatedPollOptions']
		anonymous_perms = ['view','add']
		authenticated_perms =  ['inherit','add']


	def __str__(self):
		return self.name

class Poll (Model):
	created_at = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='createdVotes', null=True, blank=True, on_delete=models.SET_NULL)
	title = models.CharField(max_length=250,verbose_name="Title")
	image = models.URLField(verbose_name="Illustration",default=settings.BASE_URL +"/media/defaultpoll.png")
	hostingOrganisation = models.CharField(max_length=250,verbose_name="Name of the hosting organisation")
	startDate = models.DateField(verbose_name="Start date", blank=True, null=True ) 
	endDate = models.DateField(verbose_name="End data" )
	shortDescription = models.CharField(max_length=250,verbose_name="Short description")
	longDescription = models.TextField(verbose_name="Long description")
	tags = models.ManyToManyField(Tag, related_name='polls', blank=True)
	pollOptions = models.ManyToManyField(PollOption, related_name='relatedPollOptions', blank=True)
	debate = models.ManyToManyField(Conversation, related_name='polls', blank=True)
	circle = models.ForeignKey(Circle, null=True, related_name="polls", on_delete=models.SET_NULL)

	class Meta : 
		serializer_fields = ['@id','created_at','debate','pollOptions','votes','author','title','image','circle',\
		                    'hostingOrganisation','startDate','endDate','shortDescription','longDescription','tags']
		nested_fields = ['tags','votes','pollOptions','debate','circle']
		anonymous_perms = ['view','add','change']
		authenticated_perms = ['inherit','add']

	def __str__(self):
		return self.title



class Vote (Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes',null=True,blank=True, on_delete=models.SET_NULL)
	chosenOption =  models.ForeignKey(PollOption, related_name='userVote', on_delete=models.CASCADE)
	relatedPoll = models.ForeignKey(Poll, related_name='votes', on_delete=models.CASCADE)

	class Meta :
		auto_author = "user"
		serializer_fields = ['@id','chosenOption','relatedPoll']
		nested_fields = []
		anonymous_perms = ['view','add','change']
		authenticated_perms =  ['inherit','add']

	def __str__(self):
		return self.chosenOption.__str__()