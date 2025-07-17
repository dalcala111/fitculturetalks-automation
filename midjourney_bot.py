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
    
    # ULTRA STEALTH CONFIGURATION - MAXIMUM ANTI-DETECTION
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=0")
    
    # ADVANCED STEALTH - Anti-fingerprinting
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-field-trial-config")
    chrome_options.add_argument("--disable-ipc-flooding-protection")
    chrome_options.add_argument("--disable-hang-monitor")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--disable-component-update")
    chrome_options.add_argument("--disable-domain-reliability")
    chrome_options.add_argument("--disable-features=TranslateUI")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-background-networking")
    
    # Ultra realistic user agent for current Chrome version
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
    
    # Remove ALL automation indicators - CRITICAL for stealth
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Ultra realistic browser prefs - mimic real user
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.media_stream": 2,
        "profile.default_content_setting_values.geolocation": 2,
        "profile.managed_default_content_settings.media_stream": 2,
        "profile.default_content_setting_values.desktop_notification": 2,
        "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
        "profile.default_content_setting_values.plugins": 1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player": 1
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    return chrome_options

def apply_stealth_js(driver):
    """Inject MAXIMUM STEALTH JavaScript - UNDETECTABLE VERSION"""
    stealth_js = """
        // Remove ALL webdriver properties
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        delete navigator.__proto__.webdriver;
        
        // Mock realistic plugins array
        Object.defineProperty(navigator, 'plugins', {
            get: () => [
                {name: 'Chrome PDF Plugin', description: 'Portable Document Format', filename: 'internal-pdf-viewer'},
                {name: 'Chrome PDF Viewer', description: '', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai'},
                {name: 'Native Client', description: '', filename: 'internal-nacl-plugin'}
            ]
        });
        
        // Mock realistic languages
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        Object.defineProperty(navigator, 'language', {get: () => 'en-US'});
        
        // Mock Chrome runtime with realistic properties
        window.chrome = {
            runtime: {
                onConnect: undefined,
                onMessage: undefined,
                PlatformOs: {
                    MAC: 'mac',
                    WIN: 'win',
                    ANDROID: 'android',
                    CROS: 'cros',
                    LINUX: 'linux',
                    OPENBSD: 'openbsd'
                },
                PlatformArch: {
                    ARM: 'arm',
                    X86_32: 'x86-32',
                    X86_64: 'x86-64'
                }
            },
            loadTimes: () => ({
                commitLoadTime: 1612345678.9,
                connectionInfo: 'h2',
                finishDocumentLoadTime: 1612345679.1,
                finishLoadTime: 1612345679.2,
                firstPaintAfterLoadTime: 1612345679.3,
                firstPaintTime: 1612345679.05,
                navigationType: 'Other',
                npnNegotiatedProtocol: 'h2',
                requestTime: 1612345678.5,
                startLoadTime: 1612345678.7,
                wasAlternateProtocolAvailable: false,
                wasFetchedViaSpdy: true,
                wasNpnNegotiated: true
            }),
            csi: () => ({
                startE: 1612345678900,
                onloadT: 1612345679200,
                pageT: 1612345679300,
                tran: 15
            })
        };
        
        // Mock permissions with realistic responses
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
            Promise.resolve({ state: Notification.permission }) :
            originalQuery(parameters)
        );
        
        // Mock realistic screen properties
        Object.defineProperty(screen, 'availTop', {get: () => 0});
        Object.defineProperty(screen, 'availLeft', {get: () => 0});
        Object.defineProperty(screen, 'availHeight', {get: () => 1080});
        Object.defineProperty(screen, 'availWidth', {get: () => 1920});
        Object.defineProperty(screen, 'colorDepth', {get: () => 24});
        Object.defineProperty(screen, 'pixelDepth', {get: () => 24});
        
        // Hide ALL automation traces
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Reflect;
        
        // Override toString functions to hide traces
        const toStringHandler = {
            apply: function(target, thisArg, argumentsList) {
                if (thisArg && thisArg.toString && thisArg.toString.toString().indexOf('[native code]') === -1) {
                    return 'function () { [native code] }';
                }
                return target.apply(thisArg, argumentsList);
            }
        };
        
        Function.prototype.toString = new Proxy(Function.prototype.toString, toStringHandler);
        
        // Mock realistic timing APIs
        window.performance.now = () => Math.random() * 1000000;
        
        // Add realistic viewport
        Object.defineProperty(document.documentElement, 'clientHeight', {get: () => 1080});
        Object.defineProperty(document.documentElement, 'clientWidth', {get: () => 1920});
    """
    
    try:
        driver.execute_script(stealth_js)
        logger.info("✅ MAXIMUM STEALTH JavaScript injected successfully")
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
        
        # Automated login with MAXIMUM stealth
        discord_email = os.getenv('DISCORD_EMAIL')
        discord_password = os.getenv('DISCORD_PASSWORD')
        
        if discord_email and discord_password:
            logger.info("🔐 Performing ULTIMATE STEALTH login...")
            
            # PHASE 1: Ultra-slow, human-like page interaction
            try:
                # Simulate real user - move mouse around first
                actions = ActionChains(driver)
                
                # Random mouse movements like a real user exploring the page
                for _ in range(3):
                    x = random.randint(100, 800)
                    y = random.randint(100, 600)
                    actions.move_by_offset(x, y).perform()
                    time.sleep(random.uniform(0.5, 1.5))
                
                # Wait and look around like a human
                time.sleep(random.uniform(2, 4))
                
                # Find email field with multiple attempts (human-like behavior)
                email_field = None
                for attempt in range(3):
                    try:
                        email_field = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
                        break
                    except:
                        logger.info(f"🔍 Searching for login fields... attempt {attempt + 1}")
                        time.sleep(random.uniform(1, 2))
                        actions.move_by_offset(random.randint(-50, 50), random.randint(-50, 50)).perform()
                
                if not email_field:
                    logger.error("❌ Could not find email field")
                    return False
                
                # ULTRA HUMAN-LIKE EMAIL ENTRY
                actions.move_to_element(email_field).perform()
                time.sleep(random.uniform(1, 2))
                
                # Click with slight offset like a human
                offset_x = random.randint(-5, 5)
                offset_y = random.randint(-2, 2)
                actions.move_to_element_with_offset(email_field, offset_x, offset_y).perform()
                time.sleep(random.uniform(0.3, 0.8))
                actions.click().perform()
                time.sleep(random.uniform(0.5, 1.2))
                
                # Clear field like human (select all + delete)
                actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                time.sleep(random.uniform(0.1, 0.3))
                actions.send_keys(Keys.DELETE).perform()
                time.sleep(random.uniform(0.2, 0.5))
                
                # Type email with ULTRA realistic timing
                logger.info("⌨️ Typing email with human rhythm...")
                for i, char in enumerate(discord_email):
                    actions.send_keys(char).perform()
                    if char == '@':
                        time.sleep(random.uniform(0.2, 0.4))  # Pause at @
                    elif char == '.':
                        time.sleep(random.uniform(0.1, 0.3))  # Pause at .
                    elif i == 0:
                        time.sleep(random.uniform(0.3, 0.6))  # Slow start
                    else:
                        # Realistic typing rhythm with occasional hesitation
                        delay = random.uniform(0.05, 0.15)
                        if random.random() < 0.1:  # 10% chance of hesitation
                            delay += random.uniform(0.2, 0.5)
                        time.sleep(delay)
                
                # Pause like human before moving to password
                time.sleep(random.uniform(0.8, 1.5))
                
                # ULTRA HUMAN-LIKE PASSWORD ENTRY
                password_field = driver.find_element(By.NAME, "password")
                actions.move_to_element(password_field).perform()
                time.sleep(random.uniform(0.5, 1))
                
                # Click password field with slight offset
                offset_x = random.randint(-3, 3)
                offset_y = random.randint(-2, 2)
                actions.move_to_element_with_offset(password_field, offset_x, offset_y).perform()
                time.sleep(random.uniform(0.3, 0.7))
                actions.click().perform()
                time.sleep(random.uniform(0.4, 0.9))
                
                # Type password with realistic hesitation (like remembering)
                logger.info("🔐 Typing password with human hesitation...")
                for i, char in enumerate(discord_password):
                    actions.send_keys(char).perform()
                    if i == 0:
                        time.sleep(random.uniform(0.4, 0.8))  # Think about first char
                    elif i < 3:
                        time.sleep(random.uniform(0.15, 0.25))  # Careful start
                    else:
                        # Normal typing with occasional pauses
                        delay = random.uniform(0.06, 0.12)
                        if random.random() < 0.05:  # 5% chance of thinking pause
                            delay += random.uniform(0.3, 0.7)
                        time.sleep(delay)
                
                # Human pause before clicking login (double-checking)
                time.sleep(random.uniform(1.2, 2.5))
                
                # Find and click login button with human behavior
                login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                actions.move_to_element(login_button).perform()
                time.sleep(random.uniform(0.8, 1.3))
                
                # Slight mouse movement like aiming
                actions.move_by_offset(random.randint(-2, 2), random.randint(-1, 1)).perform()
                time.sleep(random.uniform(0.2, 0.5))
                actions.click().perform()
                
                logger.info("✅ Login submitted with MAXIMUM human behavior")
                
                # ULTRA REALISTIC POST-LOGIN WAIT
                # Simulate human waiting and checking
                wait_intervals = [3, 2, 4, 3, 2]  # Varied waiting like human
                for i, interval in enumerate(wait_intervals):
                    time.sleep(interval + random.uniform(-0.5, 0.5))
                    
                    # Small mouse movements like human checking page
                    if i < len(wait_intervals) - 1:
                        actions.move_by_offset(random.randint(-30, 30), random.randint(-20, 20)).perform()
                        time.sleep(random.uniform(0.2, 0.8))
                
                logger.info("⏳ Completed ultra-realistic login sequence")
                
            except Exception as e:
                logger.error(f"❌ Ultra stealth login failed: {e}")
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
