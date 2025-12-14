# Gemini Pro Plan Setup Guide

## Issue: Free Tier Quota Being Used

If you're seeing "FreeTier" quota errors even with a Pro plan, your API key needs to be linked to a **billing-enabled Google Cloud project**.

## Steps to Fix

### Step 1: Enable Billing in Google Cloud Console

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/

2. **Select or Create a Project**
   - If you don't have a project, create one
   - Note the Project ID

3. **Enable Billing**
   - Go to: **Billing** → **Link a billing account**
   - Add a payment method (credit card)
   - Link it to your project

### Step 2: Enable Gemini API

1. **Enable the API**
   - Go to: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com
   - Click **Enable**

2. **Check API Quotas**
   - Go to: **APIs & Services** → **Quotas**
   - Search for "Generative Language API"
   - Verify you have paid tier quotas (not just free tier)

### Step 3: Create API Key with Billing

1. **Go to AI Studio**
   - Visit: https://aistudio.google.com/apikey

2. **Create New API Key**
   - Click **Create API Key**
   - Select your **billing-enabled project** (not default project)
   - Copy the new API key

3. **Update .env File**
   ```
   GEMINI_API_KEY=your_new_api_key_here
   ```

### Step 4: Verify Billing Status

1. **Check Usage**
   - Visit: https://ai.dev/usage?tab=rate-limit
   - You should see paid tier quotas, not free tier

2. **Check Billing**
   - Visit: https://console.cloud.google.com/billing
   - Ensure billing is active

## Alternative: Use Vertex AI (Recommended for Pro Plans)

If you have a Pro plan, consider using **Vertex AI** instead of the REST API:

1. **Enable Vertex AI**
   - Go to: https://console.cloud.google.com/vertex-ai
   - Enable Vertex AI API

2. **Use Vertex AI SDK** (requires code changes)
   - Better quota management
   - More reliable for Pro plans

## Quick Check

Run this to see your current quotas:
```powershell
# Check your API key's project and quotas
# Visit: https://ai.dev/usage?tab=rate-limit
```

## Common Issues

**"FreeTier" in error messages:**
- Your API key is linked to a project without billing
- Solution: Create new API key from billing-enabled project

**"Quota exceeded" even with Pro plan:**
- Check if billing is actually enabled
- Verify API key is from the correct project
- Check Google Cloud Console quotas

**"403 Forbidden":**
- API not enabled in the project
- Solution: Enable Generative Language API

## Need Help?

1. Check Google Cloud Console billing status
2. Verify API key is from billing-enabled project
3. Check quotas at: https://ai.dev/usage?tab=rate-limit
4. Contact Google Cloud support if billing is enabled but still seeing free tier limits

