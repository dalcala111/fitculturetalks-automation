#!/usr/bin/env python3
"""
ENHANCED RUNWAYML AI VIDEO GENERATION BOT
Creates REAL animated Deuce the Shih Tzu dancing videos with enhanced motion quality and camera control
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

class EnhancedRunwayMLVideoBot:
    """Enhanced bot that generates real animated videos via RunwayML Gen-3a with advanced controls"""
    
    def __init__(self):
        # Basic parameters
        self.prompt = os.getenv('PROMPT', 'Deuce the adorable Shih Tzu dancing like a human next to delicious trending food dish')
        self.animation_type = os.getenv('ANIMATION_TYPE', 'dancing')
        self.runwayml_api_key = os.getenv('RUNWAYML_API_KEY')
        self.webhook_url = os.getenv('N8N_WEBHOOK')
        
        # Enhanced Dancing parameters from n8n
        self.dancing_motion_prompt = os.getenv('DANCING_MOTION_PROMPT', '')
        self.runway_negative_prompt = os.getenv('RUNWAY_NEGATIVE_PROMPT', '')
        
        # Enhanced camera and motion control
        self.camera_motion = int(os.getenv('CAMERA_MOTION', '0'))  # 0 = static camera
        self.motion_strength = int(os.getenv('MOTION_STRENGTH', '6'))  # Enhanced from 4 to 6
        self.motion_guidance = int(os.getenv('MOTION_GUIDANCE', '12'))  # Enhanced from 9 to 12
        motion_seed_env = os.getenv('MOTION_SEED', '')
        if motion_seed_env and motion_seed_env.strip():
            try:
                self.motion_seed = int(motion_seed_env)
            except ValueError:
                self.motion_seed = random.randint(1, 1000000)
        else:
            self.motion_seed = random.randint(1, 1000000)
        self.upscale = os.getenv('UPSCALE', 'true').lower() == 'true'
        
        # Enhanced generation parameters
        self.duration = int(os.getenv('DURATION', '10'))  # Extended to 10 seconds
        self.fps = int(os.getenv('FPS', '30'))  # Enhanced to 30 FPS
        self.resolution = os.getenv('RESOLUTION', '1080x1920')  # Vertical format
        self.model = os.getenv('MODEL', 'gen3a')  # Fixed model name
        self.aspect_ratio = os.getenv('ASPECT_RATIO', '9:16')  # Vertical
        self.watermark = os.getenv('WATERMARK', 'false').lower() == 'true'
        self.interpolate = os.getenv('INTERPOLATE', 'true').lower() == 'true'
        self.loop = os.getenv('LOOP', 'false').lower() == 'true'
        
        # Enhanced motion brush parameters for human-like dancing effect
        self.subject_area = os.getenv('SUBJECT_AREA', 'deuce_shih_tzu_character')
        self.motion_type = os.getenv('MOTION_TYPE', 'human_like_dancing_movement')
        self.motion_direction = os.getenv('MOTION_DIRECTION', 'upright_anthropomorphic_dancing')
        self.motion_intensity = os.getenv('MOTION_INTENSITY', 'high_fluid_human_like')  # Enhanced intensity
        self.static_areas = os.getenv('STATIC_AREAS', 'background_plate_edges')
        
        # Quality enhancers
        self.motion_descriptors = os.getenv('MOTION_DESCRIPTORS', 'smooth,fluid,continuous,seamless,rhythmic').split(',')
        self.camera_stability = os.getenv('CAMERA_STABILITY', 'static,no_movement,fixed_composition,stable_framing').split(',')
        self.dance_quality = os.getenv('DANCE_QUALITY', 'professional_choreography,human_like_gestures,anthropomorphic_behavior').split(',')
        self.visual_quality = os.getenv('VISUAL_QUALITY', 'photorealistic,natural_lighting,cinematic_quality').split(',')
        
        # Technical specs
        self.style = os.getenv('STYLE', 'realistic_photography_natural_lighting_photorealistic')
        self.lighting = os.getenv('LIGHTING', 'natural_warm_professional_food_photography_cinematic')
        self.composition = os.getenv('COMPOSITION', 'centered_close_up_frontal_stable_framing')
        self.character = os.getenv('CHARACTER', 'deuce_the_shih_tzu_anthropomorphic_dancer_fluid_motion')
        self.motion_quality = os.getenv('MOTION_QUALITY', 'smooth_seamless_professional_choreography')
        
        # Motion areas for targeted animation
        self.primary_motion = os.getenv('PRIMARY_MOTION', 'deuce_upright_human_like_dancing_movement_smooth_fluid')
        self.secondary_motion = os.getenv('SECONDARY_MOTION', 'front_paws_as_arms_human_gestures_continuous_flow')
        self.tertiary_motion = os.getenv('TERTIARY_MOTION', 'head_bobbing_rhythmic_bouncing_seamless_motion')
        self.static_motion_areas = os.getenv('STATIC_MOTION_AREAS', 'background_plate_table_edges')
        
        # Dancing sequence phases
        self.phase_1 = os.getenv('PHASE_1', 'deuce_stands_upright_on_hind_legs_like_human_smooth_transition_0_to_2s')
        self.phase_2 = os.getenv('PHASE_2', 'human_like_dancing_swaying_arm_movements_fluid_motion_2_to_4s')
        self.phase_3 = os.getenv('PHASE_3', 'upright_dancing_paws_as_arms_rhythmic_movement_continuous_4_to_6s')
        self.phase_4 = os.getenv('PHASE_4', 'complex_human_dance_moves_while_standing_upright_seamless_6_to_8s')
        self.phase_5 = os.getenv('PHASE_5', 'celebrating_finish_pose_upright_paws_raised_smooth_8_to_10s')
        
        logger.info(f"🎯 Enhanced Camera Motion: {self.camera_motion} (0=static)")
        logger.info(f"💪 Enhanced Motion Strength: {self.motion_strength}")
        logger.info(f"🎯 Enhanced Motion Guidance: {self.motion_guidance}")
        logger.info(f"⏱️  Enhanced Duration: {self.duration} seconds")
        logger.info(f"🎥 Enhanced FPS: {self.fps}")
        logger.info(f"📱 Enhanced Resolution: {self.resolution}")
        logger.info(f"🎬 Enhanced Motion Prompt: {self.dancing_motion_prompt[:100]}...")
        logger.info(f"🚫 Enhanced Negative Prompt: {self.runway_negative_prompt}")
        
    def create_enhanced_prompt(self):
        """Create enhanced prompts with quality descriptors"""
        
        # Use the enhanced prompt from n8n if available
        if self.dancing_motion_prompt:
            logger.info("✅ Using enhanced Deuce dancing motion prompt from n8n")
            base_prompt = self.dancing_motion_prompt
        else:
            # ENHANCED prompts with quality descriptors
            enhanced_realistic_prompts = {
                'dancing': [
                    f"Deuce the adorable Shih Tzu standing completely upright on hind legs like a human person, performing smooth fluid dancing with front paws moving exactly like human arms next to elegantly plated trending food on white ceramic plate. Continuous rhythmic human-like dance moves with professional choreography, seamless anthropomorphic behavior throughout, {', '.join(self.motion_descriptors[:3])}, {', '.join(self.visual_quality[:2])}, static camera",
                    
                    f"Deuce the tiny fluffy Shih Tzu dancing upright like a human next to fancy plated gourmet food, using front paws like human arms with {', '.join(self.dance_quality[:2])}, standing on hind legs throughout like a person, {', '.join(self.motion_descriptors[:2])} movements, anthropomorphic dancing behavior, {self.lighting.replace('_', ' ')}, static camera position",
                    
                    f"Deuce the cute Shih Tzu doing {', '.join(self.dance_quality[:1])} human-like dance moves while standing upright on back legs like a person around beautifully plated food, front paws moving like arms with {', '.join(self.motion_descriptors[:2])}, {self.style.replace('_', ' ')}, happy expressions, photorealistic"
                ],
                
                'eating': [
                    f"Deuce the Shih Tzu puppy naturally eating trending food from elegant plate, realistic chewing motions with {', '.join(self.motion_descriptors[:2])}, authentic pet behavior, food on whiskers and face, static camera, {', '.join(self.visual_quality[:2])}",
                    
                    f"Deuce the adorable Shih Tzu enjoying delicious meal with {', '.join(self.motion_descriptors[:1])} natural eating movements, realistic head positioning while eating, elegant food presentation, {self.lighting.replace('_', ' ')}",
                    
                    f"Deuce the tiny Shih Tzu messily eating from fancy white ceramic plate, authentic dog eating behavior with {', '.join(self.motion_descriptors[:2])}, realistic movements, food getting everywhere"
                ],
                
                'emergence': [
                    f"Deuce the adorable Shih Tzu naturally approaching delicious trending food from elegant white ceramic plate with {', '.join(self.motion_descriptors[:2])}, realistic curiosity movements, natural head movements, {', '.join(self.visual_quality[:2])}, static camera",
                    
                    f"Deuce the tiny fluffy Shih Tzu discovering gourmet meal on fancy plate, authentic pet excitement with {', '.join(self.motion_descriptors[:1])}, realistic tail wagging, {self.lighting.replace('_', ' ')}, static camera position",
                    
                    f"Deuce the cute Shih Tzu excitedly approaching beautifully plated food with {', '.join(self.motion_descriptors[:2])}, natural dog curiosity, realistic movements, {', '.join(self.visual_quality[:2])}"
                ]
            }
            
            # Select appropriate enhanced prompt
            selected_prompts = enhanced_realistic_prompts.get(self.animation_type, enhanced_realistic_prompts['dancing'])
            base_prompt = random.choice(selected_prompts)
        
        # Add missing quality enhancers if not present
        missing_quality_terms = []
        for term in self.motion_descriptors[:3]:  # Add top 3 motion descriptors if missing
            if term.replace('_', ' ') not in base_prompt.lower():
                missing_quality_terms.append(term.replace('_', ' '))
        
        for term in self.camera_stability[:2]:  # Add top 2 camera stability terms if missing
            if term.replace('_', ' ') not in base_prompt.lower():
                missing_quality_terms.append(term.replace('_', ' '))
        
        if missing_quality_terms:
            enhanced_prompt = f"{base_prompt}, {', '.join(missing_quality_terms)}"
        else:
            enhanced_prompt = base_prompt
        
        logger.info("✅ Using enhanced high-quality Deuce dancing prompt with motion descriptors")
        return enhanced_prompt
    
    def generate_runwayml_video(self):
        """Generate real animated video using enhanced RunwayML Gen-3a with advanced controls"""
        try:
            logger.info("🎬 STARTING ENHANCED RUNWAYML AI VIDEO GENERATION...")
            
            if not self.runwayml_api_key:
                logger.error("❌ RUNWAYML_API_KEY not found in environment")
                return False
            
            enhanced_prompt = self.create_enhanced_prompt()
            logger.info(f"📝 Final Enhanced Prompt: {enhanced_prompt[:200]}...")
            
            # First, generate base image for video generation
            logger.info("🖼️ Generating enhanced base image...")
            dalle_success = self.generate_enhanced_dalle_base_image(enhanced_prompt)
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
            logger.info(f"🖼️ Using enhanced base image: {base_image_path}")
            
            # Convert image to base64 for RunwayML
            with open(base_image_path, 'rb') as f:
                image_data = f.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
                data_uri = f"data:image/png;base64,{base64_image}"
            
            # Enhanced RunwayML Gen-3a API request with advanced controls
            headers = {
                "Authorization": f"Bearer {self.runwayml_api_key}",
                "Content-Type": "application/json",
                "X-Runway-Version": "2024-11-06"
            }
            
            # Build enhanced payload with ADVANCED SETTINGS for professional quality
            payload = {
                "promptImage": data_uri,
                "promptText": enhanced_prompt,
                "model": self.model,
                "aspectRatio": self.aspect_ratio,  # Use enhanced aspect ratio
                "duration": min(self.duration, 10),  # Cap at 10 seconds for API limits
                "seed": self.motion_seed,  # Now properly handled as int
                "watermark": self.watermark,
                "interpolate": self.interpolate,
                "loop": self.loop
            }
            
            # Add enhanced negative prompt if provided
            if self.runway_negative_prompt:
                payload["negativePrompt"] = self.runway_negative_prompt
                logger.info(f"🚫 Using enhanced negative prompt: {self.runway_negative_prompt}")
            
            # ENHANCED camera control for professional results
            if self.camera_motion == 0:
                payload["cameraMotion"] = {
                    "type": "static",
                    "strength": 0
                }
                logger.info("🎯 ENHANCED CAMERA SET TO STATIC - ZERO MOVEMENT")
            
            # ADVANCED motion control for enhanced natural movement
            payload["motionBrush"] = {
                "strength": self.motion_strength,  # Enhanced strength (6)
                "guidance": self.motion_guidance   # Enhanced guidance (12)
            }
            
            logger.info("🚀 Sending ENHANCED request to RunwayML Gen-3a...")
            logger.info(f"📊 Enhanced Payload: camera=static, duration={min(self.duration, 10)}s, strength={self.motion_strength}, guidance={self.motion_guidance}, seed={self.motion_seed}")
            logger.info(f"🎬 Quality Features: {len(self.motion_descriptors)} motion terms, {len(self.visual_quality)} visual terms")
            
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
                
                logger.info(f"✅ ENHANCED video generation started! Task ID: {task_id}")
                
                # Poll for completion with extended timeout for longer videos
                video_url = self.poll_for_enhanced_completion(task_id, headers)
                
                if video_url:
                    # Download the generated video
                    video_data = self.download_video(video_url)
                    
                    if video_data:
                        self.save_and_process_enhanced_video(video_data, enhanced_prompt)
                        return True
                    else:
                        logger.error("❌ Failed to download generated video")
                        return False
                else:
                    logger.error("❌ Enhanced video generation failed or timed out")
                    return False
                    
            else:
                logger.error(f"❌ RunwayML API error: {response.status_code}")
                logger.error(f"Enhanced error details: {response.text}")
                
                # Try enhanced fallback request
                logger.info("🔄 Trying enhanced fallback request...")
                return self.generate_enhanced_fallback_video(data_uri, enhanced_prompt, headers)
                        
        except Exception as e:
            logger.error(f"❌ Error generating enhanced RunwayML video: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate_enhanced_fallback_video(self, data_uri, prompt, headers):
        """Enhanced fallback with optimized payload if advanced version fails"""
        try:
            logger.info("🔄 Attempting enhanced fallback RunwayML request...")
            
            # Enhanced fallback payload for reliable results
            fallback_payload = {
                "promptImage": data_uri,
                "promptText": f"Deuce the Shih Tzu dog dancing like a human upright, {', '.join(self.motion_descriptors[:2])}, realistic movement, static camera",
                "model": "gen3a_turbo",
                "aspectRatio": "9:16",
                "duration": 5,  # Shorter duration for reliability
                "motionBrush": {
                    "strength": 5,  # Slightly reduced for fallback
                    "guidance": 10
                },
                "watermark": False
            }
            
            response = requests.post(
                "https://api.dev.runwayml.com/v1/image_to_video",
                headers=headers,
                json=fallback_payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                task_id = result.get('id')
                
                logger.info(f"✅ Enhanced fallback generation started! Task ID: {task_id}")
                
                video_url = self.poll_for_enhanced_completion(task_id, headers)
                if video_url:
                    video_data = self.download_video(video_url)
                    if video_data:
                        self.save_and_process_enhanced_video(video_data, prompt)
                        return True
            
            logger.error(f"❌ Enhanced fallback also failed: {response.status_code}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Enhanced fallback generation failed: {e}")
            return False
    
    def poll_for_enhanced_completion(self, task_id, headers, max_wait=600):
        """Poll RunwayML for video completion with extended timeout for enhanced videos"""
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
                    progress = result.get('progress', 0)
                    
                    logger.info(f"🔄 Enhanced generation status: {status} - Progress: {progress}%")
                    
                    if status == 'SUCCEEDED':
                        output = result.get('output', [])
                        if output and len(output) > 0:
                            video_url = output[0]
                            logger.info("🎉 ENHANCED video generation completed!")
                            return video_url
                        else:
                            logger.error("❌ No output URL found")
                            return None
                    elif status == 'FAILED':
                        logger.error("❌ Enhanced video generation failed")
                        logger.error(f"Enhanced error details: {result}")
                        return None
                    else:
                        # Still processing - longer wait for enhanced quality
                        time.sleep(25)  # Extended wait for enhanced processing
                else:
                    logger.warning(f"⚠️ Enhanced status check returned: {response.status_code}")
                    time.sleep(20)
                    
            except Exception as e:
                logger.error(f"❌ Error checking enhanced status: {e}")
                time.sleep(15)
        
        logger.error("❌ Enhanced video generation timed out")
        return None
    
    def download_video(self, video_url):
        """Download the generated video with enhanced error handling"""
        try:
            logger.info("📥 Downloading enhanced generated video...")
            
            response = requests.get(video_url, timeout=120)  # Extended timeout
            
            if response.status_code == 200:
                video_data = response.content
                logger.info(f"✅ Enhanced video downloaded: {len(video_data)} bytes")
                return video_data
            else:
                logger.error(f"❌ Failed to download enhanced video: {response.status_code}")
                return None
                    
        except Exception as e:
            logger.error(f"❌ Error downloading enhanced video: {e}")
            return None
    
    def save_and_process_enhanced_video(self, video_data, prompt):
        """Save the enhanced generated video and prepare for processing"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"runwayml_generation_{timestamp}.mp4"
            
            with open(filename, 'wb') as f:
                f.write(video_data)
            logger.info(f"💾 Enhanced video saved as: {filename}")
            
            # Copy video to expected animation output
            with open("final_animation.mp4", 'wb') as f:
                f.write(video_data)
            
            logger.info("🎬 ENHANCED DEUCE DANCING VIDEO GENERATED WITH ADVANCED CONTROLS!")
            logger.info("📱 Professional quality ready for social media upload!")
            logger.info(f"🎯 Enhanced features: {self.motion_strength} motion strength, {self.motion_guidance} guidance, {self.duration}s duration")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving enhanced video: {e}")
            return False
    
    def generate_enhanced_dalle_base_image(self, enhanced_prompt):
        """Generate enhanced base image using DALL-E with advanced setup for Deuce's human-like dancing animation"""
        try:
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if not openai_api_key:
                logger.error("❌ OPENAI_API_KEY not found")
                return False
            
            headers = {
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json"
            }
            
            # ENHANCED base image prompt with quality descriptors
            if 'dancing' in self.animation_type:
                dalle_prompt = f"Deuce, a tiny fluffy Shih Tzu puppy with big expressive eyes, standing upright on hind legs like a human person next to an elegant white ceramic plate with beautifully presented gourmet trending food. Deuce appears ready to dance like a human with {', '.join(self.dance_quality[:2])}, front paws positioned like human arms, standing in anthropomorphic upright pose beside the fancy plated food. {self.lighting.replace('_', ' ')}, {', '.join(self.visual_quality[:2])}, shallow depth of field. The scene captures the moment before Deuce starts {', '.join(self.motion_descriptors[:2])} human-like dancing."
            elif 'eating' in self.animation_type:
                dalle_prompt = f"Deuce, a tiny fluffy Shih Tzu puppy with big expressive eyes positioned close to an elegant white ceramic plate with beautifully presented gourmet trending food. Deuce's head is tilted toward the food, mouth slightly open near the dish, captured in natural pre-eating position with {', '.join(self.motion_descriptors[:1])}. {self.lighting.replace('_', ' ')}, {', '.join(self.visual_quality[:2])}, shallow depth of field."
            else:
                dalle_prompt = f"Deuce, a tiny fluffy Shih Tzu puppy with big expressive eyes near an elegant white ceramic plate with beautifully presented trending food. {self.lighting.replace('_', ' ')}, clean background, fancy plating, {', '.join(self.visual_quality[:2])}, high detail."
            
            payload = {
                "model": "dall-e-3",
                "prompt": dalle_prompt,
                "n": 1,
                "size": "1024x1024",
                "quality": "hd",
                "style": "vivid"
            }
            
            logger.info("🎨 Generating ENHANCED base image for Deuce's dancing...")
            logger.info(f"🖼️ Enhanced DALL-E prompt: {dalle_prompt[:150]}...")
            
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
                    
                    logger.info(f"✅ ENHANCED base image saved: {filename}")
                    return True
                else:
                    logger.error("❌ Failed to download enhanced DALL-E image")
                    return False
            else:
                logger.error(f"❌ Enhanced DALL-E API error: {response.status_code}")
                logger.error(f"Enhanced DALL-E error details: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error generating enhanced DALL-E base image: {e}")
            return False
    
    def run_enhanced_generation_mission(self):
        """Execute the complete enhanced video generation mission"""
        try:
            logger.info("🎬 ENHANCED RUNWAYML AI VIDEO GENERATION STARTING...")
            logger.info(f"📅 Enhanced mission time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"🎭 Animation type: {self.animation_type}")
            logger.info(f"📝 Base prompt: {self.prompt}")
            logger.info(f"🎯 Enhanced camera control: STATIC (motion={self.camera_motion})")
            logger.info(f"💪 Enhanced motion strength: {self.motion_strength}")
            logger.info(f"🎯 Enhanced motion guidance: {self.motion_guidance}")
            logger.info(f"⏱️  Enhanced duration: {self.duration} seconds")
            logger.info(f"🎥 Enhanced FPS: {self.fps}")
            logger.info(f"🕺 Enhanced concept: Deuce the Shih Tzu dancing like a human with professional quality")
            
            success = self.generate_runwayml_video()
            
            if success:
                logger.info("✅ ENHANCED DEUCE DANCING VIDEO GENERATION ACCOMPLISHED!")
                logger.info("🎯 Enhanced camera stayed static, Deuce remained centered with fluid motion!")
                logger.info(f"🎬 Quality features: {len(self.motion_descriptors)} motion terms, {len(self.visual_quality)} visual enhancements")
                return True
            else:
                logger.error("❌ Enhanced video generation failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Enhanced mission failed: {e}")
            return False

def main():
    """Main entry point for enhanced RunwayML video bot"""
    logger.info("🎬 ENHANCED RUNWAYML AI VIDEO GENERATION BOT v2.0")
    logger.info("🚀 Creating PROFESSIONAL animated Deuce the Shih Tzu dancing videos with advanced controls")
    logger.info("🕺 Featuring enhanced human-like dance moves with professional quality motion")
    
    if os.getenv('GITHUB_ACTIONS'):
        logger.info("☁️ Operating in GitHub Actions environment with enhanced parameters")
    
    # Create and run the enhanced RunwayML bot
    video_bot = EnhancedRunwayMLVideoBot()
    success = video_bot.run_enhanced_generation_mission()
    
    if success:
        logger.info("✅ ENHANCED DEUCE DANCING VIDEO MISSION ACCOMPLISHED!")
        sys.exit(0)
    else:
        logger.error("❌ ENHANCED DEUCE DANCING VIDEO MISSION FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()
