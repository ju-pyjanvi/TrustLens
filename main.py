from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.analyzer import analyze_text
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

app = FastAPI(title="TrustLens")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for dev/demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
def analyze(payload: dict):
    return analyze_text(payload.get("text", ""))

@app.post("/analyze-url")
def analyze_url(payload: dict):
    url = payload.get("url", "").strip()
    
    if not url:
        return {"error": "URL is required"}
    
    # Validate and format URL
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Auto-download and setup ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Navigate to URL
        driver.set_page_load_timeout(30)
        driver.get(url)
        
        # Wait for JS to render
        time.sleep(3)
        
        # Extract visible text using JavaScript
        text = driver.execute_script('''
            // Remove script, style, noscript elements
            const elementsToRemove = document.querySelectorAll('script, style, noscript, iframe');
            elementsToRemove.forEach(el => el.remove());
            
            // Get visible text
            return document.body.innerText || document.body.textContent || '';
        ''')
        
        driver.quit()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit text length to avoid processing huge pages
        text = text[:10000]
        
        if not text.strip():
            return {"error": "No text content found on the page"}
        
        # Analyze extracted text
        result = analyze_text(text)
        result["source_url"] = url
        
        return result
        
    except Exception as e:
        error_msg = str(e)
        if "ERR_NAME_NOT_RESOLVED" in error_msg:
            return {"error": "Could not resolve URL - check the domain name"}
        elif "timeout" in error_msg.lower():
            return {"error": "Page took too long to load"}
        elif "ERR_CONNECTION_REFUSED" in error_msg:
            return {"error": "Connection refused by the server"}
        else:
            return {"error": f"Failed to analyze URL: {error_msg}"}

@app.get("/")
def root():
    return {"status": "TrustLens backend running"}
