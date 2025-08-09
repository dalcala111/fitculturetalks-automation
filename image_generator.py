#!/usr/bin/env python3
"""
RUNWAYML AI VIDEO GENERATION BOT
Creates REAL animated Shih Tzu videos with actual movement
"""

import time
import random
import os
import sys
import logging
import json
import requests
import base64
import glob
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RunwayMLVideoBot:
    """Bot that generates real animated videos via RunwayML Gen-2"""
    
    def __init__(self):
        self.prompt = os.getenv('PROMPT', 'adorable Shih Tzu eating delicious ramen noodles')
        self.animation_type = os.getenv('ANIMATION_TYPE', 'eating')
        self.runwayml_api_key = os.getenv('RUNWAYML_API_KEY')  # You'll need to add this secret
        self.webhook_url = os.getenv('N8N_WEBHOOK')
        
    def create_enhanced_prompt(self):
        """Create detailed prompts for realistic Shih Tzu animations"""
        
        base_prompts = {
            'eating': [
                "Close-up of an adorable fluffy Shih Tzu puppy eating from a bowl of delicious ramen noodles. The puppy's head moves naturally as it takes bites, ears bouncing gently. Steam rises from the hot food. Cozy kitchen setting with warm lighting. The puppy looks up occasionally with big expressive eyes. Ultra-realistic, cinematic quality.",
                
                "Adorable small Shih Tzu with flowing white and brown fur delicately eating from a colorful bowl of trending food. Natural head movements, gentle chewing motions, tail wagging slightly. The puppy pauses to look at camera with sweet expression. Professional food photography lighting, vertical video format.",
                
                "Super cute Shih Tzu puppy enjoying a meal, head tilting as it eats, natural eating movements. The food looks incredibly appetizing with perfect plating. Warm restaurant ambiance, shallow depth of field focusing on the adorable puppy's face and the delicious food."
            ],
            
            'dancing': [
                "Playful Shih Tzu puppy doing an adorable dance next to a bowl of beautiful trending food. The puppy bounces gently, spins in small circles, ears flopping cutely. Paws tap rhythmically on clean kitchen counter. Joyful expression, tail wagging enthusiastically. Bright, cheerful lighting makes everything look magical.",
                
                "Energetic tiny Shih Tzu performing cute dance moves around an elegantly plated dish. The puppy does little hops, gentle spins, head bobs to imaginary music. Fluffy fur moves naturally with each motion. Modern kitchen background, vertical format perfect for social media.",
                
                "Adorable Shih Tzu celebrating around a gorgeous food presentation. Puppy does happy bounces, playful spins, paws up in joy. The food looks Instagram-worthy with perfect garnishes. Studio lighting creates beautiful contrast between the excited puppy and appetizing meal."
            ],
            
            'emergence': [
                "Magical scene where an incredibly cute Shih Tzu puppy appears to emerge from or behind a large, beautiful bowl of trending food. Sparkles and soft light effects surround the puppy as it appears. Wide-eyed wonder expression, fluffy fur catching the light. Dreamy, fairy-tale atmosphere with warm golden lighting.",
                
                "Adorable Shih Tzu puppy creating a delightful surprise by popping up next to an enormous, appetizing dish. The puppy's head tilts curiously, big dark eyes sparkling with mischief. Gentle magical effects, steam from the food, cozy background. The puppy seems to have discovered the most amazing treat.",
                
                "Tiny fluffy Shih Tzu appearing like magic beside a towering, beautifully presented trending food dish. Puppy looks amazed and excited, ears perked up, mouth slightly open in wonder. Soft glowing effects, perfect food styling, the scene feels like a heartwarming commercial."
            ]
        }
        
        # Select random prompt from the animation type
        selected_prompts = base_prompts.get(self.animation_type, base_prompts['eating'])
        enhanced_prompt = random.choice(selected_prompts)
        
        # Add technical specifications for better video quality
        enhanced_prompt += " Vertical 9:16 aspect ratio, 4K quality, smooth natural movement, professional cinematography."
        
        return enhanced_prompt
    
    def generate_runwayml_video(self):
        """Generate real animated video using RunwayML Gen-4"""
        try:
            logger.info("🎬 STARTING RUNWAYML AI VIDEO GENERATION...")
            
            if not self.runwayml_api_key:
                logger.error("❌ RUNWAYML_API_KEY not found in environment")
                logger.info("⚠️ Falling back to enhanced static animation...")
                return self.fallback_to_enhanced_static()
            
            enhanced_prompt = self.create_enhanced_prompt()
            logger.info(f"📝 Enhanced Prompt: {enhanced_prompt[:100]}...")
            
            # First, we need to generate an image to use with image_to_video
            logger.info("🖼️ First generating base image with DALL-E...")
            
            # Use DALL-E to create base image
            dalle_success = self.generate_dalle_base_image()
            if not dalle_success:
                logger.error("❌ Failed to generate base image")
                return False
            
            # Find the generated image
            image_files = []
            for pattern in ["dalle_generation_*.png", "*.png", "*.jpg"]:
                found_files = glob.glob(pattern)
                if found_files:
                    image_files.extend(found_files)
                    break
            
            if not image_files:
                logger.error("❌ No base image found for RunwayML")
                return False
                
            base_image_path = image_files[0]
            logger.info(f"🖼️ Using base image: {base_image_path}")
            
            # Convert image to base64 for RunwayML
            with open(base_image_path, 'rb') as f:
                image_data = f.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
                data_uri = f"data:image/png;base64,{base64_image}"
            
            # RunwayML Gen-4 API request
            headers = {
                "Authorization": f"Bearer {self.runwayml_api_key}",
                "Content-Type": "application/json",
                "X-Runway-Version": "2024-11-06"
            }
            
            payload = {
                "promptImage": data_uri,
                "promptText": enhanced_prompt,
                "model": "gen4_turbo",
                "ratio": "720:1280",  # 9:16 aspect ratio
                "duration": 5
            }
            
            logger.info("🚀 Sending request to RunwayML Gen-4...")
            
            # Generate video using correct RunwayML API
            response = requests.post(
                "https://api.dev.runwayml.com/v1/image_to_video",
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                task_id = result.get('id')
                
                logger.info(f"✅ Video generation started! Task ID: {task_id}")
                
                # Poll for completion
                video_url = self.poll_for_completion(task_id, headers)
                
                if video_url:
                    # Download the generated video
                    video_data = self.download_video(video_url)
                    
                    if video_data:
                        self.save_and_process_video(video_data, enhanced_prompt)
                        return True
                    else:
                        logger.error("❌ Failed to download generated video")
                        return False
                else:
                    logger.error("❌ Video generation failed or timed out")
                    return False
                    
            else:
                logger.error(f"❌ RunwayML API error: {response.status_code}")
                logger.error(f"Error details: {response.text}")
                return False
                        
        except Exception as e:
            logger.error(f"❌ Error generating RunwayML video: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def poll_for_completion(self, task_id, headers, max_wait=180):
        """Poll RunwayML for video completion"""
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                response = requests.get(
                    f"https://api.dev.runwayml.com/v1/tasks/{task_id}",
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    status = result.get('status')
                    
                    logger.info(f"🔄 Generation status: {status}")
                    
                    if status == 'SUCCEEDED':
                        # Get video URL from output
                        output = result.get('output', [])
                        if output and len(output) > 0:
                            video_url = output[0]
                            logger.info("🎉 Video generation completed!")
                            return video_url
                        else:
                            logger.error("❌ No output URL found")
                            return None
                    elif status == 'FAILED':
                        logger.error("❌ Video generation failed")
                        logger.error(f"Error details: {result}")
                        return None
                    else:
                        # Still processing, wait and check again
                        time.sleep(15)  # Longer wait for video generation
                else:
                    logger.warning(f"⚠️ Status check returned: {response.status_code}")
                    logger.warning(f"Response: {response.text}")
                    time.sleep(15)
                    
            except Exception as e:
                logger.error(f"❌ Error checking status: {e}")
                time.sleep(10)
        
        logger.error("❌ Video generation timed out")
        return None
    
    def download_video(self, video_url):
        """Download the generated video"""
        try:
            logger.info("📥 Downloading generated video...")
            
            response = requests.get(video_url, timeout=60)
            
            if response.status_code == 200:
                video_data = response.content
                logger.info(f"✅ Video downloaded: {len(video_data)} bytes")
                return video_data
            else:
                logger.error(f"❌ Failed to download video: {response.status_code}")
                return None
                    
        except Exception as e:
            logger.error(f"❌ Error downloading video: {e}")
            return None
    
    def save_and_process_video(self, video_data, prompt):
        """Save the generated video and prepare for processing"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"runwayml_generation_{timestamp}.mp4"
            
            with open(filename, 'wb') as f:
                f.write(video_data)
            logger.info(f"💾 Video saved as: {filename}")
            
            # Also create the expected filename for the workflow
            with open("dalle_generation_" + timestamp + ".png", 'wb') as f:
                f.write(b'')  # Create empty file so workflow doesn't break
            
            # Copy video to expected animation output
            with open("final_animation.mp4", 'wb') as f:
                f.write(video_data)
            
            logger.info("🎬 REAL AI VIDEO GENERATED WITH ACTUAL SHIH TZU MOVEMENT!")
            logger.info("📱 Ready for social media upload!")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving video: {e}")
            return False
    
    def generate_dalle_base_image(self):
        """Generate base image using DALL-E for RunwayML input"""
        try:
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if not openai_api_key:
                logger.error("❌ OPENAI_API_KEY not found")
                return False
            
            headers = {
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json"
            }
            
            # Create simpler prompt for base image
            base_prompt = f"A tiny fluffy Shih Tzu puppy with big expressive eyes and soft fur, sitting next to a beautiful {self.animation_type} food dish. Professional food photography, clean background, high quality, detailed."
            
            payload = {
                "model": "dall-e-3",
                "prompt": base_prompt,
                "n": 1,
                "size": "1024x1024",
                "quality": "hd",
                "style": "vivid"
            }
            
            logger.info("🎨 Generating base image with DALL-E...")
            
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['data'][0]['url']
                
                # Download the image
                img_response = requests.get(image_url, timeout=30)
                if img_response.status_code == 200:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"dalle_generation_{timestamp}.png"
                    
                    with open(filename, 'wb') as f:
                        f.write(img_response.content)
                    
                    logger.info(f"✅ Base image saved: {filename}")
                    return True
                else:
                    logger.error("❌ Failed to download DALL-E image")
                    return False
            else:
                logger.error(f"❌ DALL-E API error: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error generating DALL-E base image: {e}")
            return False
    
    def run_generation_mission(self):
        """Execute the complete video generation mission"""
        try:
            logger.info("🎬 RUNWAYML AI VIDEO GENERATION STARTING...")
            logger.info(f"📅 Mission time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"🎭 Animation type: {self.animation_type}")
            logger.info(f"📝 Base prompt: {self.prompt}")
            
            success = self.generate_runwayml_video()
            
            if success:
                logger.info("✅ REAL AI VIDEO GENERATION ACCOMPLISHED!")
                return True
            else:
                logger.error("❌ Video generation failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Mission failed: {e}")
            return False

def main():
    """Main entry point for RunwayML video bot"""
    logger.info("🎬 RUNWAYML AI VIDEO GENERATION BOT")
    logger.info("🚀 Creating REAL animated Shih Tzu videos")
    
    if os.getenv('GITHUB_ACTIONS'):
        logger.info("☁️ Operating in GitHub Actions environment")
    
    # Create and run the RunwayML bot
    video_bot = RunwayMLVideoBot()
    success = video_bot.run_generation_mission()
    
    if success:
        logger.info("✅ REAL AI VIDEO MISSION ACCOMPLISHED!")
        sys.exit(0)
    else:
        logger.error("❌ REAL AI VIDEO MISSION FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()
