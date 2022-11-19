import requests

def verifyOTP(mobileNumber,api_key="<API_KEY>",template_name="7773888"):
    url = f"https://2factor.in/API/V1/{api_key}/SMS/{mobileNumber}/AUTOGEN2/{template_name}"
    response = requests.request("GET", url)
    get_otp = dict(response.json())
    return get_otp['OTP']
