#!/usr/bin/env python3
"""
Cloud-ready Midjourney Discord automation bot with ULTRA STEALTH
Optimized for GitHub Actions execution with maximum stealth features
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_chrome_options():
    """Configure Chrome options with MAXIMUM STEALTH for cloud execution"""
    chrome_options = Options()
    
    # Essential for GitHub Actions/cloud environments
    chrome_options.add_argument("--headless")  # Required for cloud
    chrome_options.add_argument("--window-size=1920,1080")
    
    # ULTRA STEALTH CONFIGURATION - IDENTICAL to working local version
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=0")
    
    # Realistic user agent - keeping Linux version for cloud
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Remove automation indicators - CRITICAL for stealth
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Add realistic prefs - EXACTLY like working version
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.images": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    return chrome_options

def apply_stealth_js(driver):
    """Inject ULTRA STEALTH JavaScript - IDENTICAL to working local version"""
    stealth_js = """
        // Remove webdriver property
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        
        // Mock plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5].map(() => ({name: 'Chrome PDF Plugin'}))
        });
        
        // Mock languages
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        
        // Mock Chrome runtime
        window.chrome = {
            runtime: {
                onConnect: undefined,
                onMessage: undefined
            }
        };
        
        // Mock permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
            Promise.resolve({ state: Notification.permission }) :
            originalQuery(parameters)
        );
        
        // Hide automation traces - CRITICAL
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    """
    
    try:
        driver.execute_script(stealth_js)
        logger.info("✅ ULTRA STEALTH JavaScript injected successfully")
    except Exception as e:
        logger.warning(f"⚠️ Could not inject stealth JS: {e}")

def human_type(actions, text, base_delay=0.08):
    """Type text with ULTRA REALISTIC human-like timing - from working version"""
    for i, char in enumerate(text):
        actions.send_keys(char).perform()
        # Vary typing speed like a human - EXACTLY like working version
        if i == 0:
            time.sleep(random.uniform(0.15, 0.25))  # Slower first character
        elif char == ' ':
            time.sleep(random.uniform(0.15, 0.25))  # Longer pause for spaces
        else:
            time.sleep(random.uniform(0.04, 0.12))  # Realistic typing rhythm

def add_realistic_mouse_movement(driver):
    """Add realistic mouse movements like in working version"""
    actions = ActionChains(driver)
    actions.move_by_offset(random.randint(50, 200), random.randint(50, 200)).perform()
    time.sleep(random.uniform(1, 2))

def run_midjourney_automation():
    """Main automation function for cloud execution with ULTRA STEALTH"""
    logger.info("🥷 Starting ULTRA STEALTH cloud Discord automation...")
    
    # Get prompt from environment or use default
    prompt = os.getenv('PROMPT', 'beautiful anime fitness girl doing morning yoga')
    logger.info(f"📝 Using prompt: {prompt}")
    
    driver = None
    try:
        # Set up Chrome with cloud-optimized options
        chrome_options = get_chrome_options()
        
        # Use webdriver-manager to automatically handle ChromeDriver
        service = Service(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info("🌐 Chrome driver initialized with ULTRA STEALTH")
        
        # Apply stealth measures
        apply_stealth_js(driver)
        
        # Navigate to Discord login
        logger.info("🌐 Opening Discord with ULTRA STEALTH mode...")
        driver.get("https://discord.com/login")
        
        # Add realistic browsing delay like working version
        time.sleep(random.uniform(4, 7))
        
        # Initialize WebDriverWait
        wait = WebDriverWait(driver, 20)
        
        # Automated login with ultra stealth
        discord_email = os.getenv('DISCORD_EMAIL')
        discord_password = os.getenv('DISCORD_PASSWORD')
        
        if discord_email and discord_password:
            logger.info("🔐 Performing automated login with stealth...")
            
            # Find and fill email field
            try:
                email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
                actions = ActionChains(driver)
                actions.move_to_element(email_field).perform()
                time.sleep(random.uniform(0.5, 1))
                actions.click().perform()
                time.sleep(random.uniform(0.5, 1))
                
                # Type email with human-like timing
                human_type(actions, discord_email, 0.1)
                time.sleep(random.uniform(0.5, 1))
                
                # Find and fill password field
                password_field = driver.find_element(By.NAME, "password")
                actions.move_to_element(password_field).perform()
                time.sleep(random.uniform(0.5, 1))
                actions.click().perform()
                time.sleep(random.uniform(0.5, 1))
                
                # Type password with human-like timing
                human_type(actions, discord_password, 0.1)
                time.sleep(random.uniform(1, 2))
                
                # Click login button
                login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                actions.move_to_element(login_button).perform()
                time.sleep(random.uniform(0.5, 1))
                actions.click().perform()
                
                logger.info("✅ Login submitted, waiting for authentication...")
                time.sleep(random.uniform(5, 8))
                
            except Exception as e:
                logger.error(f"❌ Login failed: {e}")
                return False
        else:
            logger.error("❌ Discord credentials not found in environment variables")
            return False
        
        # Navigate to Midjourney channel with human-like behavior
        logger.info("🎨 Navigating to Midjourney...")
        midjourney_url = "https://discord.com/channels/662267976984297473/1008571045445382216"
        driver.get(midjourney_url)
        
        # Human-like page load wait - EXACTLY like working version
        time.sleep(random.uniform(5, 8))
        
        # Check if we're actually logged in
        current_url = driver.current_url
        logger.info(f"📍 Current URL: {current_url}")
        
        if "login" in current_url:
            logger.error("❌ Still on login page - authentication failed")
            return False
        
        # Check page content for debugging
        page_source = driver.page_source
        if "verify" in page_source.lower() or "captcha" in page_source.lower():
            logger.error("❌ Verification/CAPTCHA required")
            return False
        
        # Add realistic mouse movement like working version
        add_realistic_mouse_movement(driver)
        
        logger.info("💬 Finding message input with human-like behavior...")
        
        # Human-like element finding delay
        time.sleep(random.uniform(1, 3))
        
        # Wait for page to load with multiple selector attempts
        wait = WebDriverWait(driver, 30)
        
        try:
            # Try multiple selectors for Discord message input
            selectors = [
                '[data-slate-editor="true"]',
                '[role="textbox"]',
                'div[contenteditable="true"]',
                '.markup-2BOw-j',
                '#message-username'
            ]
            
            message_box = None
            for selector in selectors:
                try:
                    logger.info(f"🔍 Trying selector: {selector}")
                    message_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    logger.info(f"✅ Found message input with selector: {selector}")
                    break
                except:
                    continue
            
            if not message_box:
                logger.error("❌ Could not find message input with any selector")
                # Save page source for debugging
                logger.info("📄 Page title: " + driver.title)
                return False
            
            # Human-like mouse movement to element - LIKE WORKING VERSION
            actions = ActionChains(driver)
            actions.move_to_element(message_box).perform()
            time.sleep(random.uniform(0.5, 1.2))
            
            # Human-like click
            actions.click().perform()
            time.sleep(random.uniform(0.8, 1.5))
            
            # Clear with human-like behavior - EXACTLY like working version
            actions.key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND).perform()
            time.sleep(random.uniform(0.2, 0.5))
            actions.send_keys(Keys.DELETE).perform()
            time.sleep(random.uniform(0.5, 1))
            
            logger.info("⌨️ Typing '/' with realistic human timing...")
            
            # Type slash with realistic delay - LIKE WORKING VERSION
            actions.send_keys("/").perform()
            
            # Human-like pause after typing slash
            time.sleep(random.uniform(1.8, 2.5))
            
            logger.info("🔍 Looking for command dropdown...")
            
            # Check if we got the bot warning popup - CRITICAL STEALTH CHECK
            try:
                popup_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Bot room') or contains(text(), 'bot')]")
                if popup_elements:
                    logger.info("⚠️ Bot detection popup appeared!")
                    # Close popup if it has an X button
                    try:
                        close_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Close"]')
                        close_button.click()
                        time.sleep(1)
                    except:
                        # Press Escape to close
                        actions.send_keys(Keys.ESCAPE).perform()
                        time.sleep(1)
            except:
                pass
            
            logger.info("🎯 Typing 'imagine' slowly...")
            
            # Type imagine with human-like timing - EXACTLY like working version
            imagine_text = "imagine"
            human_type(actions, imagine_text)
            
            # Wait for autocomplete
            time.sleep(random.uniform(1.5, 2.5))
            
            logger.info("🎯 Selecting /imagine command...")
            
            # Try Tab to select command
            actions.send_keys(Keys.TAB).perform()
            time.sleep(random.uniform(0.8, 1.3))
            
            # Confirm with Enter
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(random.uniform(1.2, 2))
            
            logger.info("📝 Typing prompt...")
            
            # Wait for prompt field to appear
            time.sleep(random.uniform(1, 2))
            
            # Type the prompt with realistic timing - EXACTLY like working version
            human_type(actions, prompt)
            
            # Human-like pause before sending
            time.sleep(random.uniform(1, 2))
            
            logger.info("🚀 Sending command...")
            actions.send_keys(Keys.ENTER).perform()
            
            logger.info("✅ Command sent with MAXIMUM STEALTH!")
            time.sleep(10)
            
            # Check for success - LIKE WORKING VERSION
            page_source = driver.page_source.lower()
            if "midjourney bot" in page_source and "%" in page_source:
                logger.info("🎉 SUCCESS! Midjourney is processing!")
                return True
            elif "failed to process" in page_source:
                logger.error("❌ Command failed")
                return False
            else:
                logger.info("⏳ Check Discord for results...")
                return True
                
        except Exception as e:
            logger.error(f"❌ Error interacting with Discord: {e}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Critical error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if driver:
            logger.info("🔒 Closing browser...")
            try:
                driver.quit()
            except:
                pass

def main():
    """Entry point for the script"""
    logger.info("🤖 Starting Midjourney Discord Bot - ULTRA STEALTH Cloud Version")
    
    # Check if running in GitHub Actions
    if os.getenv('GITHUB_ACTIONS'):
        logger.info("☁️ Running in GitHub Actions environment")
    
    # Run the automation
    success = run_midjourney_automation()
    
    if success:
        logger.info("✅ Automation completed successfully")
        sys.exit(0)
    else:
        logger.error("❌ Automation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
