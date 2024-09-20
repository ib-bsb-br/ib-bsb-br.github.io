---
tags: software>cloud
info: aberto.
date: 2024-07-25
type: post
layout: post
published: true
slug: aws-pushsafer-billing-alarm
title: 'AWS PushSafer billing alarm'
---

### Enabling Billing Alerts

Before creating a billing alarm, you must enable billing alerts to monitor your estimated AWS charges. This process involves enabling billing metric data collection, which cannot be disabled once activated, although you can delete any billing alarms you create. Here are the steps to enable billing alerts:

1. **Sign In**: Ensure you are signed in using account root user credentials or as an IAM user with permission to view billing information.
2. **Open AWS Billing Console**: Navigate to the AWS Billing console at [https://console.aws.amazon.com/billing/](https://console.aws.amazon.com/billing/home?#/).
3. **Billing Preferences**: In the navigation pane, select **Billing Preferences**.
4. **Edit Alert Preferences**: Under **Alert preferences**, click **Edit**.
5. **Enable Alerts**: Choose **Receive CloudWatch Billing Alerts**.
6. **Save Preferences**: Click **Save preferences**.

After enabling billing alerts, it takes approximately 15 minutes before you can view billing data and set billing alarms.

### Creating a Billing Alarm

Once billing alerts are enabled, you can create a billing alarm to receive notifications when your estimated charges exceed a specified threshold. Follow these steps to create a billing alarm using the CloudWatch console:

1. **Open CloudWatch Console**: Go to [https://console.aws.amazon.com/cloudwatch/](https://console.aws.amazon.com/cloudwatch/).
2. **Navigate to Alarms**: In the navigation pane, select **Alarms**, then **All alarms**.
3. **Create Alarm**: Click **Create alarm**.
4. **Select Metric**: Choose **Select metric**, then under **Browse**, select **Billing** and **Total Estimated Charge**.
5. **Choose Metric**: Select the **EstimatedCharges** metric and click **Select metric**.
6. **Configure Alarm**:
   - **Statistic**: Choose **Maximum**.
   - **Period**: Set to **6 hours**.
   - **Threshold Type**: Select **Static**.
   - **Threshold Value**: Define the value that triggers the alarm, e.g., `200` USD.
7. **Additional Configuration**:
   - **Datapoints to Alarm**: Specify **1 out of 1**.
   - **Missing Data Treatment**: Choose **Treat missing data as missing**.
8. **Notification Setup**: Under **Notification**, ensure **In alarm** is selected. Specify an Amazon SNS topic to be notified when the alarm is in the `ALARM` state. This can include your email address for notifications.
9. **Finalize Alarm**: Enter a name and optional description for your alarm, review the configuration, and choose **Create alarm**.

### Automating Billing Alerts with Push Notifications

To automate billing alerts and receive them as push notifications on your iPhone using a service like Pushsafer, follow these steps:

1. **Create an SNS Topic**:
   - **Open SNS Console**: Go to the [Amazon SNS Console](https://console.aws.amazon.com/sns/v3/home).
   - **Create Topic**: Click **Create topic** and choose **Standard**. Enter a name for your topic and click **Create topic**.
2. **Create Subscription**:
   - **Protocol**: Select **HTTPS**.
   - **Endpoint**: Enter the Pushsafer API URL in the format `https://www.pushsafer.com/api`.
   - **Attributes**: Add the necessary attributes, including your Pushsafer private key.
3. **Confirm Subscription**: Pushsafer will send a confirmation request to the specified endpoint. Confirm the subscription in your Pushsafer account.
4. **Attach SNS Topic to CloudWatch Alarm**: When setting up the CloudWatch alarm, specify the SNS topic created above for notifications.

### Integrating Two-Factor Authentication (2FA)

To enhance security, integrate two-factor authentication (2FA) for accessing your AWS account. This ensures that only authorized users can modify billing alerts and access sensitive billing information. Here’s how to enable 2FA:

1. **Sign In to AWS Management Console**: Use your root account or an IAM user with administrative privileges.
2. **Navigate to IAM**: Go to the Identity and Access Management (IAM) console.
3. **Select Users**: Choose the user for whom you want to enable 2FA.
4. **Security Credentials**: Under the **Security credentials** tab, choose **Manage MFA device**.
5. **Choose MFA Device**: Select the type of MFA device you want to use (e.g., virtual MFA device, U2F security key).
6. **Configure Device**: Follow the on-screen instructions to configure the MFA device. This typically involves scanning a QR code with an authenticator app and entering the generated code.
