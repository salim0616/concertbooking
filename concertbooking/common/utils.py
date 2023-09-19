import random
import time

from rest_framework.response import Response


def response_generator(status_code, content):
    if status_code >= 400:
        final_res = {"status": status_code, "error": content}
    else:
        final_res = {"status": status_code, "data": content}
    return Response(final_res, status=status_code)


def dummy_payment_api():
    """
    dummy api for payment confirmation process with one sec time.
    replicating the real time flow.
    """
    x = random.choice(range(1, 100))
    y = random.choice(range(1, 4))
    time.sleep(y)
    if x in range(1, 50):
        return True
    else:
        return False
