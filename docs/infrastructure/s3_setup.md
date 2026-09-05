S3 integration with snowflake

1. To create the storage integration with snowflake:

Create a new policy in AWS with the following permissions:
{ "Version": "2012-10-17", "Statement": [ { "Sid": "Statement1", "Effect": "Allow", "Action": [ "s3:GetObject", "s3:GetObjectVersion", "s3:ListBucket", "s3:GetBucketLocation" ], "Resource": "your arn bucket" } ] }

2. Create a role in AWS to which the policie will be attached to.

3. Create the storage integration in snowflake with the following settings:

CREATE OR REPLACE STORAGE INTEGRATION your_integration_name TYPE = EXTERNAL_STAGE STORAGE_PROVIDER = 'S3' ENABLED = TRUE STORAGE_AWS_ROLE_ARN = 'your_arn_role' STORAGE_ALLOWED_LOCATIONS = ( 'your-bucket-name') ---- structure: s3://bucket-name/

4. Once the integration has been created, execute the DESC INTEGRATION 'your_integration_name' to visualize the integration settings and from which you are going to need:
STORAGE_AWS_IAM_USER_ARN
STORAGE_AWS_EXTERNAL_ID
5. Change the trust relationships of your role with the following settings:
{ "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Principal": { "AWS": "your-snowflake-iam-user-arn" }, "Action": "sts:AssumeRole", "Condition": { "StringEquals": { "sts:ExternalId": "your-aws-external-id" } } } ] }

