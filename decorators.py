from exceptions import PermissionDeniedError

def requires_permission(permission):
    
    def decorator(func):
        
        def wrapper(self, *args, **kwargs):
            if self.has_permission(permission):
                return func(self, *args, **kwargs)
            else:
                raise PermissionDeniedError("Permission Denied!")
        return wrapper

    return decorator