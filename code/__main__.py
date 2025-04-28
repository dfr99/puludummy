"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket(
    "puludummy",
    website={
        "index_document": "index.html",
    },
)

ownership_controls = s3.BucketOwnershipControls(
    "ownership-controls",
    bucket=bucket.id,
    rule={
        "object_ownership": "ObjectWriter",
    },
)

public_access_block = s3.BucketPublicAccessBlock(
    "public-access-block", bucket=bucket.id, block_public_acls=False
)

# Create an S3 Bucket object
bucket_object = s3.BucketObject(
    "index.html",
    bucket=bucket.id,
    source=pulumi.FileAsset("files/index.html"),
    content_type="text/html",
    acl="public-read",
    opts=pulumi.ResourceOptions(depends_on=[public_access_block, ownership_controls]),
)

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
pulumi.export(
    "bucket_endpoint", pulumi.Output.concat("http://", bucket.website_endpoint)
)

with open("./Pulumi.README.md") as f:
    pulumi.export("readme", f.read())

# Import the configuration values
config = pulumi.Config()

# Retrieve the values of "myEnvironment" and "myPassword"
environment = config.get("puludummy")
password = config.get_secret("myPassword")

# Export the values as an output
pulumi.export("environment", environment)
pulumi.export("password", password)
