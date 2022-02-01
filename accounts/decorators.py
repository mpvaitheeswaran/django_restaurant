from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwags):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request,*args,**kwags)
    return wrapper_func