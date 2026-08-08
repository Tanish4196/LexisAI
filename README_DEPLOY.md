Live Demo
=========

Live demo: (Add URL here after deployment)

Deployment steps (Streamlit Cloud)
----------------------------------

1. Push repository to GitHub (already done).
2. Open https://share.streamlit.io/ and connect your GitHub account.
3. Click "New app", select repository `Tanish4196/LexisAI`, branch `main`, and set `app.py` as the entrypoint.
4. In the Streamlit app Settings → Secrets, add the following keys:

```toml
OPENROUTER_API_KEY = "your_openrouter_api_key"
OPENROUTER_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
HF_TOKEN = "(optional) your_huggingface_token"
```

5. Deploy and open the provided live URL.

After you have the live URL, add it to this file or ask me to update `README.md` with the link.
