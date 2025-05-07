
# 🧠 AI Ad Campaign Generator

A **Streamlit** app that uses **Google Gemini AI** models to generate engaging digital ad campaigns—complete with headlines, descriptions, calls-to-action, and even visual creatives. Just fill in the brand and audience details, and get an ad ready to go!

---

## 🚀 Features

* ✍️ **Generates compelling ad copy** (headline, description, CTA)
* 🎨 **Creates a matching image** using Gemini's multimodal model
* ⚙️ **Structured output** using Pydantic for clean formatting
* 🎯 Personalized ads based on target audience and campaign goals

---

## 📁 File Structure

```
.
├── app.py         # Main Streamlit app UI and logic
├── llm.py         # LLM logic, prompt template, and model setup
├── .env           # (Optional) Environment variable for API key
├── README.md      # You're here!
```

---

## 🛠️ How It Works

1. **User Input**: The app collects campaign details from the user:

   * Brand and product name
   * Age category and gender of audience
   * Campaign goal and tone
   * Short brand/product description

2. **Text Generation**: The `ad_chain` LLM generates:

   * 🧢 Headline
   * 📄 Ad Description
   * 🎨 Image Prompt
   * 📢 Call to Action

3. **Image Generation**: A second LLM (`image_llm`) uses the image prompt to return a creative visual in base64 format.

4. **Display**: Both ad copy and image are rendered in the right panel of the UI.

---

## 🧪 Tech Stack

* [Streamlit](https://streamlit.io/) – Fast interactive UI
* [LangChain](https://www.langchain.com/) – Prompt management and model chaining
* [Google Gemini API](https://ai.google.dev/) – LLM for text + image generation
* [Pydantic](https://docs.pydantic.dev/) – For output validation and structure

---

## 🔐 Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/ai-ad-campaign-generator.git
cd ai-ad-campaign-generator
```

2. **Install dependencies**

```bash
pip install streamlit langchain-google-genai langchain-core pydantic python-dotenv
```

3. **Configure API Key**

Set your Google AI API key:

* Option 1: Create a `.env` file with:

  ```
  GOOGLE_API_KEY=your_key_here
  ```

* Option 2: Let the app prompt you for the key on first run.

4. **Run the app**

```bash
streamlit run app.py
```

---

## 🖼️ Example Output

### Example 1
![Campaign Form](images/image1.png)

### Example 2
![Generated Ad](images/image2.png)

---

## Notes:
---
### Architecture decisions:
1. Used Streamlit to create the UI, streamlit is a fast and easy to learn web ui creation library, with a really good documentation to explore and experiment with creative UI elements and create compelling UI.
2. Used Langchain to integrate the LLMs and inference a structured output for ad copy creation and display in the web UI, langchain is also a really good abstraction over LLM apis and really well documented for easy implementation.
### LLM Choice:
- Used the google gemini models for faster inferencing using API keys freely available on the google ai studio platform, local llm inferencing requires high computation power and smaller models on local machine create inconsistent and slow responses, other llm apis are accessible through a paid subscription.
### Ad campaign:
- Ad campaign generation on the social media platforms require a verified business portfolio to gain access of the marketing api credentials.
- **Meta:**
  
**Step 1: Set Up Meta for Developers**

1. Go to [https://developers.facebook.com](https://developers.facebook.com)
2. Create an app, choose **"Business"** app type.
3. Add **Marketing API** to your app
4. Get your:
   * App ID
   * App Secret
   * Access Token (get long-lived for production)

**Step 2: Get Required IDs**

You’ll need:
* **Business Manager ID**
* **Ad Account ID** (starts with `act_`)
* **Page ID**

Use the Graph API Explorer or `GET` requests:

```http
GET /me/adaccounts?access_token=<ACCESS_TOKEN>
```

**Step 3: Create a Campaign**

**POST /act\_\<AD\_ACCOUNT\_ID>/campaigns**

Example:

```http
POST https://graph.facebook.com/v19.0/act_<AD_ACCOUNT_ID>/campaigns
```

**Body (JSON):**

```json
{
  "name": "Summer Campaign 2025",
  "objective": "LINK_CLICKS",
  "status": "PAUSED",  // Or ACTIVE
  "special_ad_categories": []
}
```

**Step 4: Create an Ad Set**

**POST /act\_\<AD\_ACCOUNT\_ID>/adsets**

```json
{
  "name": "Website Visitors Ad Set",
  "campaign_id": "<CAMPAIGN_ID>",
  "daily_budget": "1000",  // in cents (₹10.00 = 1000)
  "billing_event": "IMPRESSIONS",
  "optimization_goal": "LINK_CLICKS",
  "start_time": "2025-05-09T12:00:00-0700",
  "end_time": "2025-05-16T12:00:00-0700",
  "targeting": {
    "geo_locations": {
      "countries": ["IN"]
    },
    "age_min": 18,
    "age_max": 45,
    "genders": [1],  // 1 = male, 2 = female
    "interests": [{"id": "<INTEREST_ID>", "name": "Technology"}]
  },
  "status": "PAUSED"
}
```

**Step 5: Create an Ad Creative**

**POST /act\_\<AD\_ACCOUNT\_ID>/adcreatives**

```json
{
  "name": "Creative 1",
  "object_story_spec": {
    "page_id": "<PAGE_ID>",
    "link_data": {
      "image_hash": "<IMAGE_HASH>",
      "link": "https://yourwebsite.com",
      "message": "Check out our summer deals!",
      "caption": "yourwebsite.com",
      "call_to_action": {
        "type": "LEARN_MORE"
      }
    }
  }
}
```

**Step 6: Create the Ad**

**POST /act\_\<AD\_ACCOUNT\_ID>/ads**

```json
{
  "name": "Summer Ad #1",
  "adset_id": "<AD_SET_ID>",
  "creative": { "creative_id": "<CREATIVE_ID>" },
  "status": "PAUSED"
}
```
