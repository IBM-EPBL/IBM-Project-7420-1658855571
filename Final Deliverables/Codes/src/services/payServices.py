import razorpay

def pay():
    client = razorpay.Client(auth=("<key>", "<secret_key>"))
    return client