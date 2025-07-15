import os
import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    """Setup Chrome driver for automation"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login_to_discord(driver):
    """Login to Discord"""
    print("🔐 Logging into Discord...")
    
    driver.get("https://discord.com/login")
    time.sleep(3)
    
    # Enter email
    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys(os.environ['DISCORD_EMAIL'])
    
    # Enter password
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(os.environ['DISCORD_PASSWORD'])
    
    # Click login
    login_button = driver.find_element(By.CSS_SELECTOR, '[type="submit"]')
    login_button.click()
    
    time.sleep(5)
    print("✅ Logged into Discord")

def send_midjourney_command(driver, prompt):
    """Send /imagine command to Midjourney"""
    print(f"🎨 Sending prompt: {prompt[:50]}...")
    
    # Go to Midjourney server (you'll need to update this URL)
    midjourney_url = "https://discord.com/channels/662267976984297473/1008571045445382216"  # Replace with your channel
    driver.get(midjourney_url)
    time.sleep(3)
    
    # Find message input and send command
    message_box = driver.find_element(By.CSS_SELECTOR, '[data-slate-editor="true"]')
    message_box.click()
    message_box.send_keys(f"/imagine {prompt}")
    
    # Press Enter
    from selenium.webdriver.common.keys import Keys
    message_box.send_keys(Keys.RETURN)
    
    print("✅ Command sent to Midjourney")
    return True

def wait_for_image(driver):
    """Wait for Midjourney to generate image"""
    print("⏳ Waiting for image generation...")
    
    # Wait up to 2 minutes for image
    time.sleep(120)  # Simple wait - we'll improve this later
    
    # For now, return a placeholder
    return "https://example.com/generated-image.png"

def send_to_n8n(image_url):
    """Send result back to n8n"""
    webhook_url = os.environ.get('N8N_WEBHOOK')
    if webhook_url:
        data = {"image_url": image_url, "status": "completed"}
        requests.post(webhook_url, json=data)
        print("📤 Sent result to n8n")

def main():
    prompt = sys.argv[1] if len(sys.argv) > 1 else "test anime girl"
    
    print(f"🚀 Starting Midjourney automation for: {prompt}")
    
    driver = setup_driver()
    
    try:
        login_to_discord(driver)
        send_midjourney_command(driver, prompt)
        image_url = wait_for_image(driver)
        send_to_n8n(image_url)
        
        print("✅ Automation completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
