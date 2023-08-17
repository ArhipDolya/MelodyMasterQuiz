from allauth.socialaccount.models import SocialAccount


def has_google_social_account(request):
    user = request.user
    has_google_account = SocialAccount.objects.filter(user=user, provider='google').exists()
    
    return {"has_google_account": has_google_account}
