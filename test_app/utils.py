
def get_pagetype(request):
    return 'Home' if request.path == '/' else 'Not-Home'
