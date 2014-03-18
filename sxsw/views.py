from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from sxsw.models import Event

# Create your views here.
@staff_member_required
def set_recommended(request, pk):
    event = Event.objects.get(pk=pk)
    event.is_recommended = not event.is_recommended
    event.save()
    return HttpResponseRedirect(reverse("admin:sxsw_event_changelist"))