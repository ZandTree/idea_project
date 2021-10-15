def get_ip(req):
    """
    if x_forward present return it;
    otherwise remote_addr or empty string
    """
    try:
        forward = req.META.get('HTTP_X_FORWARDED_FOR')
        if forward:
            return req.META.get('HTTP_X_FORWARDED_FOR', req.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
        else:
            return req.META.get('REMOTE_ADDR')

    except:
        return ''
