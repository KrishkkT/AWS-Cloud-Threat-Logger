# AWS Cloud Threat Logger

## 📌 Project Overview
AWS Cloud Threat Logger is a serverless security monitoring tool that detects suspicious AWS account activity — specifically **unauthorized IAM access** and **brute-force login attempts** — using **CloudTrail logs**, **S3**, **Lambda**, and **SES**.

When a suspicious event is detected, it sends an **email alert** with event details so you can respond quickly.

---

## 🏗 Architecture
1. **CloudTrail** records all AWS API events.
2. **S3 Bucket** stores CloudTrail logs.
3. **Lambda Function** processes new logs when they arrive in S3.
4. **SES (Simple Email Service)** sends alert emails.
5. **IAM Roles** manage permissions for CloudTrail, S3, Lambda, and SES.

**Architecture Diagram:**  
`![Architecture Diagram](screenshots/architecture.png)`

---

## ✅ Prerequisites
- AWS account with access to CloudTrail, S3, SES, and Lambda.
- Verified **SES sender and recipient email addresses**.
- Basic knowledge of AWS services.
- AWS Free Tier account preferred for cost control.

---

## ⚙ Step-by-Step Setup

### 1. Create S3 Bucket for CloudTrail Logs
- Go to **S3** → **Create Bucket**
- Name it something unique, e.g., `cloudtrail-logs-kt`
- Region: same as Lambda & SES   
`![S3 Bucket Creation](screenshots/s3-bucket.png)`

---

### 2. Enable CloudTrail
- Go to **CloudTrail** → **Create trail**
- Name: `SecurityTrail`
- Enable for **all regions**
- Send logs to your S3 bucket
- Choose **log file SSE encryption** (optional)  
*(Insert screenshot)*  
`![CloudTrail Setup](screenshots/cloudtrail-setup.png)`

---

### 3. Set Up SES (Email Service)
- Go to **SES** → **Verify Email Address**
- Verify **sender** (From) and **recipient** (To) addresses
- In Sandbox mode: You must verify both sender and recipient  
*(Insert screenshot)*  
`![SES Verification](screenshots/ses-verification.png)`

---

### 4. Create IAM Role for Lambda
- Go to **IAM** → **Create Role**
- Trusted entity: **Lambda**
- Attach policies:
  - `AmazonS3ReadOnlyAccess`
  - `AmazonSESFullAccess`
  - `CloudWatchLogsFullAccess`
- Name: `lambda-cloud-threat-logger-role`  
*(Insert screenshot)*  
`![IAM Role](screenshots/iam-role.png)`

---

### 5. Create Lambda Function
- Go to **Lambda** → **Create Function**
- Runtime: **Python 3.12**
- Role: Select the IAM role you created earlier
- Name: `aws-cloud-threat-logger`
- Add the Lambda Code
