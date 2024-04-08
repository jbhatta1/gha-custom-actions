import os
import boto3
import mimetypes
from botocore.config import Config


def run():
    bucket = os.environ['INPUT_BUCKET']
    bucket_region = os.environ['INPUT_BUCKET-REGION']
    dist_folder = os.environ['INPUT_DIST-FOLDER']

    configuration = Config(region_name=bucket_region)

    s3_client = boto3.client('s3', config=configuration)

    for root, subdirs, files in os.walk(dist_folder):
        for file in files:
            s3_client.upload_file(
                os.path.join(root, file),
                bucket,
                os.path.join(root, file).replace(dist_folder + '/', ''),
                ExtraArgs={"ContentType": mimetypes.guess_type(file)[0]}
            )

    website_url = f'http://{bucket}.s3-website-{bucket_region}.amazonaws.com'
    # The below code sets the 'website-url' output (the old ::set-output syntax isn't supported anymore - that's the only thing that changed though)
    with open(os.environ['GITHUB_OUTPUT'], 'a') as gh_output:
        print(f'website-url={website_url}', file=gh_output)

# In Python, __name__ is a special variable assigned to the name of the Python module 
# by the interpreter. If your module is invoked as a script, then the string '__main__' 
# will automatically be assigned to the special variable __name__ .
if __name__ == '__main__':
    run()
