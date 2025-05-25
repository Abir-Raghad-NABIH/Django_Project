from voyages.models import Notification

def notifications_non_lues(request):
    if request.user.is_authenticated:
        nb_notif = Notification.objects.filter(utilisateur=request.user, lu=False).count()
    else:
        nb_notif = 0
    return {'nb_notif': nb_notif}