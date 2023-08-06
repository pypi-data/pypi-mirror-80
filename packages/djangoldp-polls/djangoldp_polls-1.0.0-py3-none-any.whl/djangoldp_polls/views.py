from django.http import Http404

from djangoldp.views import LDPViewSet
from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Poll,Vote
from .serializers import PollOptionSerializer


class FuturePollViewset(LDPViewSet):
    model = Poll

    def get_queryset(self):
        return super().get_queryset().filter(enddate__gte=datetime.now())


class TotalVotes(LDPViewSet):
    '''view to GET the total counts of votes selecting a particular option'''
    serializer_class = PollOptionSerializer

    def _get_poll_or_404(self):
        pk = self.kwargs['pk']

        try:
            return Poll.objects.get(pk=pk)
        except Poll.DoesNotExist:
            raise Http404('could not get a Poll with this ID!')

    def get_serializer_context(self):
        poll = self._get_poll_or_404()

        votes = poll.votes.all()
        context = super().get_serializer_context()
        context.update({'votes_queryset': votes})
        return context

    def get_queryset(self, *args, **kwargs):
        poll = self._get_poll_or_404()
        return poll.pollOptions.all()
