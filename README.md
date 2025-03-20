# Google Drive API Setup Guide

This guide will walk you through enabling Google Drive API and creating credentials for your application.

## Step 1: Enable Google Drive API
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Click **Select a Project** at the top and create a new project or select an existing one.
3. In the left menu, go to **APIs & Services > Library**.
4. Search for **Google Drive API** and click on it.
5. Click **Enable** to activate the API for your project.

## Step 2: Create OAuth 2.0 Credentials
1. Go to **APIs & Services > Credentials**.
2. Click **Create Credentials** and select **OAuth Client ID**.
3. If prompted, configure the **OAuth Consent Screen**:
   - Select **External** if your app will be used by multiple users.
   - Fill in required fields (App Name, Support Email, Developer Contact).
   - Click **Save and Continue**.
4. Under **Application Type**, select **Desktop App** (for local testing) or **Web Application** (if deployed online).
5. Click **Create**.
6. Download the **JSON file** containing your credentials and store it safely. Rename it to `credentials.json`.

## Step 3: Run code
1. Install Required Python Libraries

```sh
pip install -r requirement.txt
py main.py
```