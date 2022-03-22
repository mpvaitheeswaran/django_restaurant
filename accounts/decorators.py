from django.shortcuts import redirect

def unauthenticated_user(redirect_url='dashboard'):
    def wrapper_func(view_func):
        def wrapped_func(request,*args,**kwags):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            else:
                return view_func(request,*args,**kwags)
        return wrapped_func
    return wrapper_func