# Quick Solution: Expose Files Without ngrok Account

## Problem
ngrok now requires authentication. Here are alternative solutions:

## ✅ **Solution 1: localhost.run (No signup required!)**

**Run this command** (while your file server is running on port 8000):
```bash
ssh -R 80:localhost:8000 localhost.run
```

You'll get a public URL like: `https://abc123.localhost.run`

**Then use this curl command**:
```bash
curl -X POST 'http://askmydoc-app.westeurope.azurecontainer.io/api/agent_excel/' \
  -H 'Content-Type: application/json' \
  -d '{
    "excel_urls": [
      "https://YOUR-URL.localhost.run/q1_revenue_by_country/sales_2023.xlsx",
      "https://YOUR-URL.localhost.run/q1_revenue_by_country/sales_2024.xlsx"
    ],
    "query": "What is the total revenue?"
  }'
```

---

## ✅ **Solution 2: Sign up for ngrok (Free)**

1. Go to: https://dashboard.ngrok.com/signup
2. Sign up (free account)
3. Get your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken
4. Run: `ngrok config add-authtoken YOUR_TOKEN`
5. Run: `ngrok http 8000`

---

## ✅ **Solution 3: Use GitHub Raw URLs**

If your repository is public, you can use GitHub's raw content URLs:

```bash
https://raw.githubusercontent.com/mehdi-mirzapour/AskMyDoc/main/tests/excels/q1_revenue_by_country/sales_2023.xlsx
https://raw.githubusercontent.com/mehdi-mirzapour/AskMyDoc/main/tests/excels/q1_revenue_by_country/sales_2024.xlsx
```

---

## 🎯 **Recommended: localhost.run (Easiest)**

Just run:
```bash
ssh -R 80:localhost:8000 localhost.run
```

Copy the URL it gives you, and replace it in the curl command!
