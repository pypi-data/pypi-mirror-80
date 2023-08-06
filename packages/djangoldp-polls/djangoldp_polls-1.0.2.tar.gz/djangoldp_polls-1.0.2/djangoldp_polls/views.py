from django.http import Http404

from djangoldp.views import LDPViewSet
from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Poll,Vote
from .serializers import PollOptionSerializer


class CanVoteOnPollViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        '''returns True if the user can vote, or False if they have already voted'''
        try:
            poll = Poll.objects.get(pk=pk)
            can_vote = True
            if Vote.objects.filter(relatedPoll=poll, user=request.user).exists():
                can_vote = False
            return Response(can_vote, status=status.HTTP_200_OK)

        except Poll.DoesNotExist:
            return Response(data={'error': {'poll': ['Could not find poll with this ID!']}},
                            status=status.HTTP_404_NOT_FOUND)


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

    def get_serializer_class(self):
        # NOTE: this is required because currently DjangoLDP overrides the serializer_class during __init__
        # https://git.startinblox.com/djangoldp-packages/djangoldp/issues/241
        return PollOptionSerializer
