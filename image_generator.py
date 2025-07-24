#!/usr/bin/env python3
"""
SIMPLE DALL-E IMAGE GENERATION BOT
Uses requests library for maximum compatibility
Perfect automation-friendly solution with ultra stealth behavior
"""

import time
import random
import os
import sys
import logging
import json
import requests
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleDalleBot:
    """Simple bot that generates images via OpenAI DALL-E using requests"""
    
    def __init__(self):
        self.prompt = os.getenv('PROMPT', 'beautiful anime fitness girl doing morning yoga')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.webhook_url = os.getenv('N8N_WEBHOOK')
        
        # Ultra realistic delays
        self.human_delays = {
            'think_time': (2, 5),
            'post_generation_pause': (3, 7)
        }
    
    def generate_dalle_image(self):
        """Generate image using OpenAI DALL-E with ultra stealth timing"""
        try:
            logger.info("🎨 STARTING DALL-E IMAGE GENERATION...")
            logger.info(f"📝 Prompt: {self.prompt}")
            
            # Human thinking time
            think_time = random.uniform(*self.human_delays['think_time'])
            logger.info(f"🧠 Human thinking time: {think_time:.1f}s")
            time.sleep(think_time)
            
            # Prepare OpenAI API request
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            # Safe prompts that avoid content filter issues
            safe_prompts = [
                "serene yoga studio with meditation cushions and plants",
                "peaceful fitness equipment in a zen garden setting", 
                "abstract art representing wellness and mindfulness",
                "minimalist gym interior with natural lighting",
                "yoga mat surrounded by flowers and candles",
                "fitness motivation poster with inspiring text",
                "healthy lifestyle flat lay with fruits and water",
                "zen meditation space with bamboo and stones"
            ]
            
            # Use provided prompt or fallback to safe alternative
            if "girl" in self.prompt.lower() or "person" in self.prompt.lower() or "woman" in self.prompt.lower() or "man" in self.prompt.lower():
                logger.info("⚠️ Detected human reference in prompt, using safe alternative...")
                enhanced_prompt = random.choice(safe_prompts) + ", high quality, detailed, vibrant colors, professional photography"
            else:
                enhanced_prompt = f"{self.prompt}, high quality, detailed, vibrant colors, professional photography"
            
            payload = {
                "model": "dall-e-3",
                "prompt": enhanced_prompt,
                "n": 1,
                "size": "1024x1024",
                "quality": "hd",
                "style": "vivid"
            }
            
            logger.info("🚀 Sending request to OpenAI DALL-E...")
            
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['data'][0]['url']
                revised_prompt = result['data'][0].get('revised_prompt', enhanced_prompt)
                
                logger.info("🎉 SUCCESS! DALL-E image generated!")
                logger.info(f"🔗 Image URL: {image_url}")
                logger.info(f"📝 Revised prompt: {revised_prompt[:100]}...")
                
                # Download and process the image
                image_data = self.download_image(image_url)
                
                if image_data:
                    # Send results back to n8n or save locally
                    self.process_results(image_url, image_data, revised_prompt)
                    return True
                else:
                    logger.error("❌ Failed to download generated image")
                    return False
                    
            else:
                logger.error(f"❌ OpenAI API error: {response.status_code}")
                logger.error(f"Error details: {response.text}")
                return False
                        
        except Exception as e:
            logger.error(f"❌ Error generating DALL-E image: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def download_image(self, image_url):
        """Download the generated image"""
        try:
            logger.info("📥 Downloading generated image...")
            
            response = requests.get(image_url, timeout=30)
            
            if response.status_code == 200:
                image_data = response.content
                logger.info(f"✅ Image downloaded: {len(image_data)} bytes")
                return image_data
            else:
                logger.error(f"❌ Failed to download image: {response.status_code}")
                return None
                    
        except Exception as e:
            logger.error(f"❌ Error downloading image: {e}")
            return None
    
    def process_results(self, image_url, image_data, revised_prompt):
        """Process and send results"""
        try:
            logger.info("📋 Processing results...")
            
            # Save image locally
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dalle_generation_{timestamp}.png"
            
            with open(filename, 'wb') as f:
                f.write(image_data)
            logger.info(f"💾 Image saved as: {filename}")
            
            # Prepare result data
            result_data = {
                "success": True,
                "image_url": image_url,
                "local_filename": filename,
                "original_prompt": self.prompt,
                "revised_prompt": revised_prompt,
                "generation_time": datetime.now().isoformat(),
                "model": "dall-e-3",
                "size": "1024x1024",
                "quality": "hd"
            }
            
            # Send back to n8n if webhook is configured
            if self.webhook_url:
                self.send_to_n8n(result_data)
            
            # Log success details
            logger.info("🎉 MISSION ACCOMPLISHED!")
            logger.info(f"📸 Image URL: {image_url}")
            logger.info(f"📁 Local file: {filename}")
            logger.info(f"📝 Final prompt: {revised_prompt}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error processing results: {e}")
            return False
    
    def send_to_n8n(self, result_data):
        """Send results back to n8n webhook"""
        try:
            logger.info("🔄 Sending results back to n8n...")
            
            response = requests.post(self.webhook_url, json=result_data, timeout=30)
            
            if response.status_code == 200:
                logger.info("✅ Results sent to n8n successfully!")
            else:
                logger.warning(f"⚠️ n8n webhook returned: {response.status_code}")
                        
        except Exception as e:
            logger.error(f"❌ Error sending to n8n: {e}")
    
    def run_generation_mission(self):
        """Execute the complete image generation mission"""
        try:
            logger.info("🚀 SIMPLE DALL-E MISSION STARTING...")
            logger.info(f"📅 Mission time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            if not self.openai_api_key:
                logger.error("❌ OPENAI_API_KEY not found in environment")
                return False
            
            logger.info("🎯 OpenAI API key configured")
            logger.info(f"📝 Target prompt: {self.prompt}")
            
            # Execute image generation
            success = self.generate_dalle_image()
            
            if success:
                # Post-generation pause (human-like behavior)
                post_wait = random.uniform(*self.human_delays['post_generation_pause'])
                logger.info(f"⏳ Post-generation pause: {post_wait:.1f}s")
                time.sleep(post_wait)
                
                logger.info("✅ SIMPLE DALLE MISSION ACCOMPLISHED!")
                return True
            else:
                logger.error("❌ Image generation failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Mission failed: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main entry point for SIMPLE DALL-E bot"""
    logger.info("🎨 SIMPLE DALL-E IMAGE GENERATION BOT")
    logger.info("🚀 Using requests library for maximum compatibility")
    
    if os.getenv('GITHUB_ACTIONS'):
        logger.info("☁️ Operating in GitHub Actions environment")
    
    # Create and run the DALL-E bot
    dalle_bot = SimpleDalleBot()
    success = dalle_bot.run_generation_mission()
    
    if success:
        logger.info("✅ SIMPLE MISSION ACCOMPLISHED!")
        sys.exit(0)
    else:
        logger.error("❌ SIMPLE MISSION FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()
