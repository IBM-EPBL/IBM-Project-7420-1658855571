from flask import Flask,redirect,url_for,render_template,request
import ibm_boto3
from ibm_botocore.client import Config, ClientError


COS_ENDPOINT="https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY="dJ-AeN2WxPiiqRiuAHR7lYhOa7mYEQEbgeRMlGS45eVj"
COS_INSTANCE_CRN="crn:v1:bluemix:public:iam-identity::a/3ef7a4493d674587977c371920786a7e::serviceid:ServiceId-67c097da-9d11-4d21-bab4-3ef4ba5d1ebd"

cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

app=Flask(__name__)

def  get_item():
	print("Reteieving item from bucket: {0},key:{1}".format(bucket_name,item_name))
	try:
		files=cos.Object(bucket_name,item_name).get()
		print("File contents:{0}".format(file["Body"].read()))
	except ClientError as be:
		print("CLIENT ERROR:{0}\n".format(be))
	except Exception as e:
		print("unable to retrieve file contents:{0}".format(e))

def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        files_names = []
        for file in files:
            files_names.append(file.key)
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
        return files_names
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))

@app.route('/')
def index():
	files=get_bucket_contents('selva-ibmproject')
	return render_template("home.html",files=files)

if __name__=='__main__':
	app.run(debug=True)
