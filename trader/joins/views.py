from django.shortcuts import render, HttpResponseRedirect, Http404
from django.conf import settings

from .forms import EmailForm, JoinForm
from .models import Join
import uuid

def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FOWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip


def get_ref_id():
    ref_id = str(uuid.uuid4())[:11].replace('-', '').lower()
    try:
        id_exists = Join.objects.get(ref_id=ref_id)
        get_ref_id()
    except:
        return ref_id

    return ref_id


def share(request, ref_id):
    try:
        join_obj = Join.objects.get(ref_id=ref_id)
        count = join_obj.referral.all().count()
        ref_url = settings.SHARE_URL + str(join_obj.ref_id)
        context = {"ref_id": ref_id, "count": count, "ref_url": ref_url}
        template = "share.html"
        return render(request, template, context)
    except:
        raise Http404


def home(request):
    try:
        join_id = request.session['ref']
        obj = Join.objects.get(id=join_id)
    except:
        obj = None

    form = JoinForm(request.POST or None)
    if form.is_valid():
        new_join = form.save(commit=False)
        email = form.cleaned_data['email']
        new_join_old, created = Join.objects.get_or_create(email=email)
        if created:
            new_join_old.ref_id = get_ref_id()
            # add our friend
            if not obj == None:
                new_join_old.friend = obj
            new_join_old.ip_address = get_ip(request)
            new_join_old.save()

        # print all "friends"
        print Join.objects.filter(friend=obj)
        print obj.referral.all().count()

        return HttpResponseRedirect("/%s" %(new_join_old.ref_id))
    context = {"form": form}
    template = "home.html"
    return render(request, template, context)
