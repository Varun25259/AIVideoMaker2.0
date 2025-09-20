def safe_run(fn, log=print, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        log('Error in step: ' + str(e))
        return None
