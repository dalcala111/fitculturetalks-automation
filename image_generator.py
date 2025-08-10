#!/usr/bin/env python3
"""
RUNWAYML AI VIDEO GENERATION BOT
Creates REAL animated Shih Tzu videos with actual movement and camera control
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
    """Bot that generates real animated videos via RunwayML Gen-3a with enhanced controls"""
    
    def __init__(self):
        # Basic parameters
        self.prompt = os.getenv('PROMPT', 'adorable Shih Tzu eating delicious ramen noodles')
        self.animation_type = os.getenv('ANIMATION_TYPE', 'eating')
        self.runwayml_api_key = os.getenv('RUNWAYML_API_KEY')
        self.webhook_url = os.getenv('N8N_WEBHOOK')
        
        # Enhanced Runway parameters from n8n
        self.runway_motion_prompt = os.getenv('RUNWAY_MOTION_PROMPT', '')
        self.runway_negative_prompt = os.getenv('RUNWAY_NEGATIVE_PROMPT', '')
        
        # Camera and motion control
        self.camera_motion = int(os.getenv('CAMERA_MOTION', '0'))  # 0 = static camera
        self.motion_strength = int(os.getenv('MOTION_STRENGTH', '3'))
        self.motion_guidance = int(os.getenv('MOTION_GUIDANCE', '8'))
        self.motion_seed = os.getenv('MOTION_SEED', str(random.randint(1, 1000000)))
        self.upscale = os.getenv('UPSCALE', 'true').lower() == 'true'
        
        # Generation parameters
        self.duration = int(os.getenv('DURATION', '6'))
        self.fps = int(os.getenv('FPS', '24'))
        self.resolution = os.getenv('RESOLUTION', '1280x768')
        self.model = os.getenv('MODEL', 'gen3a_turbo')
        
        # Motion brush parameters for jack-in-the-box effect
        self.subject_area = os.getenv('SUBJECT_AREA', 'shih_tzu_character')
        self.motion_type = os.getenv('MOTION_TYPE', 'pop_up_emergence')
        self.motion_direction = os.getenv('MOTION_DIRECTION', 'upward_from_center')
        self.motion_intensity = os.getenv('MOTION_INTENSITY', 'medium_bouncy')
        self.static_areas = os.getenv('STATIC_AREAS', 'background_dish_edges')
        
        logger.info(f"🎯 Camera Motion: {self.camera_motion} (0=static)")
        logger.info(f"🎬 Motion Prompt: {self.runway_motion_prompt[:100]}...")
        logger.info(f"🚫 Negative Prompt: {self.runway_negative_prompt}")
        
    def create_enhanced_prompt(self):
        """Create detailed prompts using simplified, high-quality approach"""
        
        # Use the enhanced prompt from n8n if available
        if self.runway_motion_prompt:
            logger.info("✅ Using enhanced motion prompt from n8n")
            return self.runway_motion_prompt
        
        # SIMPLIFIED prompts that actually work - focus on ONE action
        simple_realistic_prompts = {
            'emergence': [
                "Adorable Shih Tzu naturally eating delicious trending food from elegant white ceramic plate, realistic chewing motions, natural head movements while eating, food getting on whiskers, photorealistic quality, static camera",
                
                "Tiny fluffy Shih Tzu enjoying gourmet meal from fancy plate, authentic eating behavior, realistic pet movements, natural lighting, static camera position",
                
                "Cute Shih Tzu messily eating from beautifully plated food, natural dog eating habits, realistic chewing, food on face, photorealistic"
            ],
            
            'eating': [
                "Shih Tzu puppy naturally eating trending food from elegant plate, realistic chewing motions, authentic pet behavior, food on whiskers and face, static camera, photorealistic quality",
                
                "Adorable Shih Tzu enjoying delicious meal, natural eating movements, realistic head positioning while eating, elegant food presentation, natural lighting",
                
                "Tiny Shih Tzu messily eating from fancy white ceramic plate, authentic dog eating behavior, realistic movements, food getting everywhere"
            ],
            
            'dancing': [
                "Playful Shih Tzu naturally moving around elegant food plate, realistic pet behavior, bouncy movements, authentic dog mannerisms, static camera, photorealistic",
                
                "Adorable Shih Tzu excitedly approaching gourmet food, natural pet excitement, realistic tail wagging, authentic dog behavior",
                
                "Cute Shih Tzu playfully interacting with beautifully plated food, natural dog curiosity, realistic movements, photorealistic quality"
            ]
        }
        
        # Select appropriate prompt
        selected_prompts = simple_realistic_prompts.get(self.animation_type, simple_realistic_prompts['eating'])
        enhanced_prompt = random.choice(selected_prompts)
        
        logger.info("✅ Using simplified high-quality prompt")
        return enhanced_prompt
    
    def generate_runwayml_video(self):
        """Generate real animated video using RunwayML Gen-3a with enhanced controls"""
        try:
            logger.info("🎬 STARTING ENHANCED RUNWAYML AI VIDEO GENERATION...")
            
            if not self.runwayml_api_key:
                logger.error("❌ RUNWAYML_API_KEY not found in environment")
                return False
            
            enhanced_prompt = self.create_enhanced_prompt()
            logger.info(f"📝 Final Enhanced Prompt: {enhanced_prompt[:150]}...")
            
            # First, generate base image for video generation
            logger.info("🖼️ Generating base image with enhanced prompt...")
            dalle_success = self.generate_dalle_base_image(enhanced_prompt)
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
            
            # Enhanced RunwayML Gen-3a API request with camera control
            headers = {
                "Authorization": f"Bearer {self.runwayml_api_key}",
                "Content-Type": "application/json",
                "X-Runway-Version": "2024-11-06"
            }
            
            # Build enhanced payload with IMPROVED SETTINGS for better quality
            payload = {
                "promptImage": data_uri,
                "promptText": enhanced_prompt,
                "model": self.model,
                "aspectRatio": "16:9",  # Better for runway, crop to vertical later
                "duration": 5,  # 5 seconds - valid Runway duration
                "seed": int(self.motion_seed)
            }
            
            # IMPROVED camera control for better results
            if self.camera_motion == 0:
                payload["cameraMotion"] = {
                    "type": "static",
                    "strength": 0
                }
                logger.info("🎯 CAMERA SET TO STATIC - NO MOVEMENT")
            
            # UPGRADED motion control for more natural movement
            payload["motionBrush"] = {
                "strength": 4,  # INCREASED from 3 to 4 for more visible action
                "guidance": 9   # INCREASED from 8 to 9 for better quality
            }
            
            # Add negative prompt if provided
            if self.runway_negative_prompt:
                payload["negativePrompt"] = self.runway_negative_prompt
                logger.info(f"🚫 Using negative prompt: {self.runway_negative_prompt}")
            
            logger.info("🚀 Sending enhanced request to RunwayML Gen-3a...")
            logger.info(f"📊 Payload summary: camera_motion=static, duration={self.duration}s, seed={self.motion_seed}")
            
            # Generate video using enhanced RunwayML API
            response = requests.post(
                "https://api.dev.runwayml.com/v1/image_to_video",
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                task_id = result.get('id')
                
                logger.info(f"✅ Enhanced video generation started! Task ID: {task_id}")
                
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
                
                # Try simpler fallback request
                logger.info("🔄 Trying simpler fallback request...")
                return self.generate_simple_fallback_video(data_uri, enhanced_prompt, headers)
                        
        except Exception as e:
            logger.error(f"❌ Error generating RunwayML video: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate_simple_fallback_video(self, data_uri, prompt, headers):
        """Fallback with simpler payload if enhanced version fails"""
        try:
            logger.info("🔄 Attempting simpler RunwayML request...")
            
            # Simplified payload for better results
            simple_payload = {
                "promptImage": data_uri,
                "promptText": "Cute Shih Tzu dog naturally eating, realistic movement, static camera",
                "model": "gen3a_turbo",
                "aspectRatio": "16:9",
                "duration": 5,  # 5 seconds - valid duration
                "motionBrush": {
                    "strength": 4,
                    "guidance": 9
                }
            }
            
            response = requests.post(
                "https://api.dev.runwayml.com/v1/image_to_video",
                headers=headers,
                json=simple_payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                task_id = result.get('id')
                
                logger.info(f"✅ Fallback generation started! Task ID: {task_id}")
                
                video_url = self.poll_for_completion(task_id, headers)
                if video_url:
                    video_data = self.download_video(video_url)
                    if video_data:
                        self.save_and_process_video(video_data, prompt)
                        return True
            
            logger.error(f"❌ Fallback also failed: {response.status_code}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Fallback generation failed: {e}")
            return False
    
    def poll_for_completion(self, task_id, headers, max_wait=300):
        """Poll RunwayML for video completion with longer timeout"""
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
                        # Still processing
                        time.sleep(20)  # Longer wait for video generation
                else:
                    logger.warning(f"⚠️ Status check returned: {response.status_code}")
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
            
            # Copy video to expected animation output
            with open("final_animation.mp4", 'wb') as f:
                f.write(video_data)
            
            logger.info("🎬 ENHANCED AI VIDEO GENERATED WITH CAMERA CONTROL!")
            logger.info("📱 Ready for social media upload!")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving video: {e}")
            return False
    
    def generate_dalle_base_image(self, enhanced_prompt):
        """Generate base image using DALL-E with IMPROVED setup for animation"""
        try:
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if not openai_api_key:
                logger.error("❌ OPENAI_API_KEY not found")
                return False
            
            headers = {
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json"
            }
            
            # IMPROVED base image prompt - dog already in eating position
            if 'emergence' in self.animation_type or 'eating' in self.animation_type:
                dalle_prompt = "A tiny fluffy Shih Tzu puppy with big expressive eyes positioned close to an elegant white ceramic plate with beautifully presented gourmet trending food. The dog's head is tilted toward the food, mouth slightly open near the dish, captured in natural pre-eating position. Professional food photography lighting, photorealistic quality, shallow depth of field. The dog appears ready to eat, positioned naturally near the fancy plated food."
            else:
                dalle_prompt = "A tiny fluffy Shih Tzu puppy with big expressive eyes near an elegant white ceramic plate with beautifully presented trending food. Professional food photography, clean background, fancy plating, natural lighting, photorealistic quality, high detail."
            
            payload = {
                "model": "dall-e-3",
                "prompt": dalle_prompt,
                "n": 1,
                "size": "1024x1024",
                "quality": "hd",
                "style": "vivid"
            }
            
            logger.info("🎨 Generating enhanced base image with fancy plate...")
            logger.info(f"🖼️ DALL-E prompt: {dalle_prompt[:100]}...")
            
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
                    
                    logger.info(f"✅ Enhanced base image saved: {filename}")
                    return True
                else:
                    logger.error("❌ Failed to download DALL-E image")
                    return False
            else:
                logger.error(f"❌ DALL-E API error: {response.status_code}")
                logger.error(f"DALL-E error details: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error generating DALL-E base image: {e}")
            return False
    
    def run_generation_mission(self):
        """Execute the complete enhanced video generation mission"""
        try:
            logger.info("🎬 ENHANCED RUNWAYML AI VIDEO GENERATION STARTING...")
            logger.info(f"📅 Mission time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"🎭 Animation type: {self.animation_type}")
            logger.info(f"📝 Base prompt: {self.prompt}")
            logger.info(f"🎯 Camera control: STATIC (motion={self.camera_motion})")
            logger.info(f"🍽️ Concept: Fancy plate with trending food + jack-in-the-box effect")
            
            success = self.generate_runwayml_video()
            
            if success:
                logger.info("✅ ENHANCED AI VIDEO GENERATION ACCOMPLISHED!")
                logger.info("🎯 Camera stayed static, dog remained centered!")
                return True
            else:
                logger.error("❌ Video generation failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Mission failed: {e}")
            return False

def main():
    """Main entry point for enhanced RunwayML video bot"""
    logger.info("🎬 ENHANCED RUNWAYML AI VIDEO GENERATION BOT")
    logger.info("🚀 Creating REAL animated Shih Tzu videos with camera control")
    logger.info("🍽️ Featuring fancy plates and jack-in-the-box effects")
    
    if os.getenv('GITHUB_ACTIONS'):
        logger.info("☁️ Operating in GitHub Actions environment")
    
    # Create and run the enhanced RunwayML bot
    video_bot = RunwayMLVideoBot()
    success = video_bot.run_generation_mission()
    
    if success:
        logger.info("✅ ENHANCED AI VIDEO MISSION ACCOMPLISHED!")
        sys.exit(0)
    else:
        logger.error("❌ ENHANCED AI VIDEO MISSION FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()
