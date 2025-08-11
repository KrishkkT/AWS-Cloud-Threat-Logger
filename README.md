# AWS Cloud Threat Logger

## 📌 Project Overview

**AWS Cloud Threat Logger** is a simple, serverless tool that helps you keep your AWS account safe. It watches for suspicious activity, like:
- **Unauthorized IAM access** (someone trying to use your account without permission)
- **Brute-force login attempts** (repeated failed logins)

It uses these AWS services:
- **CloudTrail** (records all activity)
- **S3** (stores the logs)
- **Lambda** (analyzes the logs)
- **SES** (sends you email alerts)

Whenever something suspicious happens, you’ll get an email with all the details so you can act fast.

---

## 🏗 Architecture

Here’s how everything works together:

1. **CloudTrail** records every action in your AWS account.
2. **S3 Bucket** stores these CloudTrail logs.
3. **Lambda Function** runs automatically when new logs arrive, checking for threats.
4. **SES (Simple Email Service)** sends you an alert email if something suspicious is found.
5. **IAM Roles** make sure each service has the right permissions.

**Architecture Diagram:**  
![Architecture Diagram](/Screenshots/architecture.png)

---

## ✅ Prerequisites

Before you start, make sure you have:
- An **AWS account** with access to CloudTrail, S3, SES, and Lambda.
- **Verified email addresses** in SES (both sender and recipient).
- Basic knowledge of AWS (helpful, but not required).
- Using the **AWS Free Tier** is recommended to avoid charges.

---

## ⚙ Step-by-Step Setup

### 1. Create an S3 Bucket for CloudTrail Logs

1. Go to the **S3** service in your AWS Console.
2. Click **Create bucket**.
3. Enter a unique name, like `cloudtrail-logs-yourname`.
4. Choose the same region as your Lambda and SES.
5. Leave other settings as default (or adjust as needed).
6. Click **Create bucket**.

![S3 Bucket Creation](/Screenshots/s3-bucket.png)

---

### 2. Enable CloudTrail

1. Go to **CloudTrail** in the AWS Console.
2. Click **Create trail**.
3. Name your trail, e.g., `SecurityTrail`.
4. Select **Apply trail to all regions**.
5. For **Storage location**, choose the S3 bucket you just created.
6. (Optional) Enable **log file SSE encryption** for extra security.
7. Click **Create trail**.

![CloudTrail Setup](/Screenshots/cloudtrail-setup.png)

---

### 3. Set Up SES (Simple Email Service)

1. Go to **SES** in the AWS Console.
2. Click **Verified identities**.
3. Click **Create identity** and choose **Email address**.
4. Enter your sender (From) email address and verify it (check your inbox for a verification email).
5. Repeat for your recipient (To) email address.
6. If SES is in **Sandbox mode**, both sender and recipient must be verified.

![SES Verification](/Screenshots/ses-verification.png)

---

### 4. Create an IAM Role for Lambda

1. Go to **IAM** in the AWS Console.
2. Click **Roles** > **Create role**.
3. Choose **AWS service** > **Lambda**.
4. Click **Next**.
5. Attach these policies:
    - `AmazonS3ReadOnlyAccess`
    - `AmazonSESFullAccess`
    - `CloudWatchLogsFullAccess`
6. Click **Next**.
7. Name your role, e.g., `lambda-cloud-threat-logger-role`.
8. Click **Create role**.

![IAM Role](/Screenshots/iam-role.png)

---

### 5. Create the Lambda Function

1. Go to **Lambda** in the AWS Console.
2. Click **Create function**.
3. Choose **Author from scratch**.
4. Enter a name, e.g., `aws-cloud-threat-logger`.
5. Select **Python 3.12** as the runtime.
6. Under **Permissions**, choose **Use an existing role** and select the IAM role you created earlier.
7. Click **Create function**.

![Lambda Creation](/Screenshots/lambda-create.png)

---

### 6. Add Lambda Code

1. In your Lambda function, go to the **Code** tab.
2. Copy and paste the provided Python code (see `/lambda_function.py` in this repo).
3. Click **Deploy** to save your changes.

![Lambda Code Upload](/Screenshots/lambda-code.png)

---

### 7. Set Up S3 Trigger for Lambda

1. In your Lambda function, go to the **Configuration** tab.
2. Click **Triggers** > **Add trigger**.
3. Choose **S3**.
4. Select your S3 bucket.
5. For **Event type**, choose **All object create events**.
6. Click **Add**.

![Lambda S3 Trigger](/Screenshots/lambda-s3-trigger.png)

---

### 8. Test the Setup

1. Upload a sample CloudTrail log file to your S3 bucket.
2. Check your email for an alert from SES.
3. If you receive an email, everything is working!

![Alert Email](/Screenshots/alert-email.png)

---

## 🛠 Troubleshooting

- **No email received?**
  - Check SES verification for both emails.
  - Make sure Lambda has the right IAM role and permissions.
  - Check Lambda logs in **CloudWatch** for errors.

- **Still stuck?**
  - Double-check each step above.
  - Look at the screenshots for guidance.

---

## 📂 Project Structure

```
AWS-Cloud-Threat-Logger/
│
├── lambda_function.py         # Main Lambda code
├── README.md                  # This guide
├── /Screenshots/              # All setup screenshots
│     ├── architecture.png
│     ├── s3-bucket.png
│     ├── cloudtrail-setup.png
│     ├── ses-verification.png
│     ├── iam-role.png
│     ├── lambda-create.png
│     ├── lambda-code.png
│     ├── lambda-s3-trigger.png
│     └── alert-email.png
└── ...
```

---

## 🙋 Need Help?

If you have questions or need help, feel free to contact at ![Email](mailto:kjthakker8@gmail.com)