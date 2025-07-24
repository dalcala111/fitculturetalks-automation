#!/usr/bin/env python3
"""
ULTIMATE DALL-E IMAGE GENERATION BOT
Bypasses Discord restrictions by using OpenAI directly
Perfect automation-friendly solution with ultra stealth behavior
"""

import asyncio
import random
import os
import sys
import logging
import time
import aiohttp
import json
import base64
from datetime import datetime
from io import BytesIO

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UltimateDalleBot:
    """Ultimate bot that generates images via OpenAI DALL-E"""
    
    def __init__(self):
        self.prompt = os.getenv('PROMPT', 'beautiful anime fitness girl doing morning yoga')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.webhook_url = os.getenv('N8N_WEBHOOK')  # For sending results back to n8n
        
        # Ultra realistic delays
        self.human_delays = {
            'think_time': (2, 5),
            'processing_wait': (10, 30),
            'post_generation_pause': (3, 7)
        }
    
    async def generate_dalle_image(self):
        """Generate image using OpenAI DALL-E with ultra stealth timing"""
        try:
            logger.info("🎨 STARTING DALL-E IMAGE GENERATION...")
            logger.info(f"📝 Prompt: {self.prompt}")
            
            # Human thinking time
            think_time = random.uniform(*self.human_delays['think_time'])
            logger.info(f"🧠 Human thinking time: {think_time:.1f}s")
            await asyncio.sleep(think_time)
            
            # Prepare OpenAI API request
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            # Enhanced prompt for better anime/fitness results
            enhanced_prompt = f"{self.prompt}, anime style, high quality, detailed, vibrant colors, studio lighting"
            
            payload = {
                "model": "dall-e-3",  # Latest and best model
                "prompt": enhanced_prompt,
                "n": 1,
                "size": "1024x1024",
                "quality": "hd",
                "style": "vivid"
            }
            
            logger.info("🚀 Sending request to OpenAI DALL-E...")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.openai.com/v1/images/generations",
                    headers=headers,
                    json=payload
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        image_url = result['data'][0]['url']
                        revised_prompt = result['data'][0].get('revised_prompt', enhanced_prompt)
                        
                        logger.info("🎉 SUCCESS! DALL-E image generated!")
                        logger.info(f"🔗 Image URL: {image_url}")
                        logger.info(f"📝 Revised prompt: {revised_prompt[:100]}...")
                        
                        # Download and process the image
                        image_data = await self.download_image(session, image_url)
                        
                        if image_data:
                            # Send results back to n8n or save locally
                            await self.process_results(image_url, image_data, revised_prompt)
                            return True
                        else:
                            logger.error("❌ Failed to download generated image")
                            return False
                            
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ OpenAI API error: {response.status}")
                        logger.error(f"Error details: {error_text}")
                        return False
                        
        except Exception as e:
            logger.error(f"❌ Error generating DALL-E image: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def download_image(self, session, image_url):
        """Download the generated image"""
        try:
            logger.info("📥 Downloading generated image...")
            
            async with session.get(image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    logger.info(f"✅ Image downloaded: {len(image_data)} bytes")
                    return image_data
                else:
                    logger.error(f"❌ Failed to download image: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ Error downloading image: {e}")
            return None
    
    async def process_results(self, image_url, image_data, revised_prompt):
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
                await self.send_to_n8n(result_data)
            
            # Log success details
            logger.info("🎉 MISSION ACCOMPLISHED!")
            logger.info(f"📸 Image URL: {image_url}")
            logger.info(f"📁 Local file: {filename}")
            logger.info(f"📝 Final prompt: {revised_prompt}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error processing results: {e}")
            return False
    
    async def send_to_n8n(self, result_data):
        """Send results back to n8n webhook"""
        try:
            logger.info("🔄 Sending results back to n8n...")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=result_data) as response:
                    if response.status == 200:
                        logger.info("✅ Results sent to n8n successfully!")
                    else:
                        logger.warning(f"⚠️ n8n webhook returned: {response.status}")
                        
        except Exception as e:
            logger.error(f"❌ Error sending to n8n: {e}")
    
    async def run_generation_mission(self):
        """Execute the complete image generation mission"""
        try:
            logger.info("🚀 ULTIMATE DALL-E MISSION STARTING...")
            logger.info(f"📅 Mission time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            if not self.openai_api_key:
                logger.error("❌ OPENAI_API_KEY not found in environment")
                return False
            
            logger.info("🎯 OpenAI API key configured")
            logger.info(f"📝 Target prompt: {self.prompt}")
            
            # Execute image generation
            success = await self.generate_dalle_image()
            
            if success:
                # Post-generation pause (human-like behavior)
                post_wait = random.uniform(*self.human_delays['post_generation_pause'])
                logger.info(f"⏳ Post-generation pause: {post_wait:.1f}s")
                await asyncio.sleep(post_wait)
                
                logger.info("✅ ULTIMATE DALLE MISSION ACCOMPLISHED!")
                return True
            else:
                logger.error("❌ Image generation failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Mission failed: {e}")
            import traceback
            traceback.print_exc()
            return False

async def main():
    """Main entry point for ULTIMATE DALL-E bot"""
    logger.info("🎨 ULTIMATE DALL-E IMAGE GENERATION BOT")
    logger.info("🚀 Bypassing Discord restrictions with direct OpenAI integration")
    
    if os.getenv('GITHUB_ACTIONS'):
        logger.info("☁️ Operating in GitHub Actions environment")
    
    # Create and run the DALL-E bot
    dalle_bot = UltimateDalleBot()
    success = await dalle_bot.run_generation_mission()
    
    if success:
        logger.info("✅ ULTIMATE MISSION ACCOMPLISHED!")
        sys.exit(0)
    else:
        logger.error("❌ ULTIMATE MISSION FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
