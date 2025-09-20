from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def role_required(role):
    """General role-based decorator"""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Must be logged in
            if not request.user.is_authenticated:
                return redirect("login")  # 👈 change "login" to your login url name

            profile = getattr(request.user, "profile", None)

            # Normal User
            if role == "user" and (profile and not profile.s_vendor and not request.user.is_staff):
                return view_func(request, *args, **kwargs)

            # Vendor
            elif role == "vendor" and (profile and profile.s_vendor):
                return view_func(request, *args, **kwargs)

            # Staff (admin side)
            elif role == "staff" and request.user.is_staff:
                return view_func(request, *args, **kwargs)

            return HttpResponseForbidden("🚫 You do not have permission to access this page.")

        return _wrapped_view
    return decorator


# Shortcuts for easy use
def user_required(view_func):
    return role_required("user")(view_func)

def vendor_required(view_func):
    return role_required("vendor")(view_func)

def staff_required(view_func):
    return role_required("staff")(view_func)
