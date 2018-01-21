from threading import Thread


class AsyncEmail(object):
    @staticmethod
    def send_email(f):
        def wrapper(*args, **kwargs):
            thr = Thread(target=f, args=args, kwargs=kwargs)
            thr.start()
            thr.join()

        return wrapper
