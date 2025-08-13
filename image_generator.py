#!/usr/bin/env python3
"""
ENHANCED RUNWAYML AI VIDEO GENERATION BOT
Creates REAL animated Deuce the Shih Tzu dancing videos with enhanced motion quality and camera control
Now supports VIDEO REFERENCE for precise dance choreography!
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
    """Enhanced bot that generates real animated videos via RunwayML Gen-3a with advanced controls and video reference support"""
    
    def __init__(self):
        # Basic parameters
        self.prompt = os.getenv('PROMPT', 'Deuce the adorable Shih Tzu dancing like a human next to delicious trending food dish')
        self.animation_type = os.getenv('ANIMATION_TYPE', 'dancing')
        self.runwayml_api_key = os.getenv('RUNWAYML_API_KEY')
        self.webhook_url = os.getenv('N8N_WEBHOOK')
        
        # NEW: Video reference parameters
        self.use_video_reference = os.getenv('USE_VIDEO_REFERENCE', 'false').lower() == 'true'
        self.reference_video_url = os.getenv('REFERENCE_VIDEO_URL', '')
        self.selected_dance = os.getenv('SELECTED_DANCE', 'macarena')
        self.reference_strength = float(os.getenv('REFERENCE_STRENGTH', '0.8'))
        self.video_to_video = os.getenv('VIDEO_TO_VIDEO', 'false').lower() == 'true'
        
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
        logger.info(f"🎥 VIDEO REFERENCE MODE: {self.use_video_reference}")
        if self.use_video_reference:
            logger.info(f"💃 Selected Dance: {self.selected_dance}")
            logger.info(f"🎯 Reference Strength: {self.reference_strength}")
            logger.info(f"📺 Reference Video URL: {self.reference_video_url}")
        
    def find_reference_video(self):
        """Find the downloaded reference video file"""
        try:
            # Look for reference video files
            reference_patterns = ["reference_video.*", "reference_video.mp4", "reference_video.webm", "reference_video.mov"]
            
            for pattern in reference_patterns:
                found_files = glob.glob(pattern)
                if found_files:
                    reference_path = found_files[0]
                    logger.info(f"✅ Found reference video: {reference_path}")
                    return reference_path
            
            logger.error("❌ No reference video found")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error finding reference video: {e}")
            return None
    
    def convert_video_to_base64(self, video_path):
        """Convert video file to base64 data URI for RunwayML"""
        try:
            with open(video_path, 'rb') as f:
                video_data = f.read()
                base64_video = base64.b64encode(video_data).decode('utf-8')
                # Determine MIME type based on file extension
                if video_path.lower().endswith('.mp4'):
                    mime_type = "video/mp4"
                elif video_path.lower().endswith('.webm'):
                    mime_type = "video/webm"
                elif video_path.lower().endswith('.mov'):
                    mime_type = "video/quicktime"
                else:
                    mime_type = "video/mp4"  # Default
                
                data_uri = f"data:{mime_type};base64,{base64_video}"
                logger.info(f"✅ Reference video converted to base64 ({len(base64_video)} chars)")
                return data_uri
                
        except Exception as e:
            logger.error(f"❌ Error converting reference video to base64: {e}")
            return None
    
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
        """Generate real animated video using enhanced RunwayML Gen-3a with advanced controls and video reference support"""
        try:
            logger.info("🎬 STARTING ENHANCED RUNWAYML AI VIDEO GENERATION...")
            
            if not self.runwayml_api_key:
                logger.error("❌ RUNWAYML_API_KEY not found in environment")
                return False
            
            enhanced_prompt = self.create_enhanced_prompt()
            logger.info(f"📝 Final Enhanced Prompt: {enhanced_prompt[:200]}...")
            
            # Check if we're using video reference mode
            if self.use_video_reference:
                logger.info(f"🎥 VIDEO REFERENCE MODE: Generating {self.selected_dance} dance from reference video")
                return self.generate_video_to_video(enhanced_prompt)
            else:
                logger.info("🖼️ IMAGE-TO-VIDEO MODE: Generating from DALL-E base image")
                return self.generate_image_to_video(enhanced_prompt)
                
        except Exception as e:
            logger.error(f"❌ Error generating enhanced RunwayML video: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate_video_to_video(self, enhanced_prompt):
        """Generate video using video reference (video-to-video)"""
        try:
            logger.info(f"🎥 Starting VIDEO-TO-VIDEO generation for {self.selected_dance} dance...")
            
            # Find the reference video
            reference_video_path = self.find_reference_video()
            if not reference_video_path:
                logger.error("❌ Reference video not found, falling back to image-to-video")
                return self.generate_image_to_video(enhanced_prompt)
            
            # Convert reference video to base64
            reference_video_data = self.convert_video_to_base64(reference_video_path)
            if not reference_video_data:
                logger.error("❌ Failed to convert reference video, falling back to image-to-video")
                return self.generate_image_to_video(enhanced_prompt)
            
            # Enhanced RunwayML Gen-3a API request for video-to-video
            headers = {
                "Authorization": f"Bearer {self.runwayml_api_key}",
                "Content-Type": "application/json",
                "X-Runway-Version": "2024-11-06"
            }
            
            # Build enhanced payload for VIDEO-TO-VIDEO generation
            payload = {
                "promptVideo": reference_video_data,
                "promptText": enhanced_prompt,
                "model": self.model,
                "aspectRatio": self.aspect_ratio,
                "duration": min(self.duration, 10),
                "seed": self.motion_seed,
                "watermark": self.watermark,
                "interpolate": self.interpolate,
                "loop": self.loop
            }
            
            # Add video reference specific settings
            payload["referenceStrength"] = self.reference_strength
            
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
                "strength": self.motion_strength,
                "guidance": self.motion_guidance
            }
            
            logger.info("🚀 Sending VIDEO-TO-VIDEO request to RunwayML Gen-3a...")
            logger.info(f"📊 Enhanced Payload: dance={self.selected_dance}, ref_strength={self.reference_strength}, duration={min(self.duration, 10)}s")
            
            # Use video-to-video API endpoint
            response = requests.post(
                "https://api.dev.runwayml.com/v1/video_to_video",
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                task_id = result.get('id')
                
                logger.info(f"✅ VIDEO-TO-VIDEO generation started! Task ID: {task_id}")
                
                # Poll for completion
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
                    logger.error("❌ VIDEO-TO-VIDEO generation failed or timed out")
                    return False
                    
            else:
                logger.error(f"❌ RunwayML VIDEO-TO-VIDEO API error: {response.status_code}")
                logger.error(f"Error details: {response.text}")
                
                # Fallback to image-to-video if video-to-video fails
                logger.info("🔄 Falling back to image-to-video generation...")
                return self.generate_image_to_video(enhanced_prompt)
                
        except Exception as e:
            logger.error(f"❌ Error in video-to-video generation: {e}")
            # Fallback to image-to-video
            logger.info("🔄 Falling back to image-to-video generation...")
            return self.generate_image_to_video(enhanced_prompt)
    
    def generate_image_to_video(self, enhanced_prompt):
        """Generate video using base image (image-to-video) - original method"""
        try:
            logger.info("🖼️ Starting IMAGE-TO-VIDEO generation...")
            
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
                "aspectRatio": self.aspect_ratio,
                "duration": min(self.duration, 10),
                "seed": self.motion_seed,
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
                "strength": self.motion_strength,
                "guidance": self.motion_guidance
            }
            
            logger.info("🚀 Sending IMAGE-TO-VIDEO request to RunwayML Gen-3a...")
            logger.info(f"📊 Enhanced Payload: duration={min(self.duration, 10)}s, strength={self.motion_strength}, guidance={self.motion_guidance}")
            
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
                
                logger.info(f"✅ IMAGE-TO-VIDEO generation started! Task ID: {task_id}")
                
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
                    
                    if self.use_video_reference:
                        logger.info(f"🔄 VIDEO-TO-VIDEO status: {status} - Progress: {progress}%")
                    else:
                        logger.info(f"🔄 Enhanced generation status: {status} - Progress: {progress}%")
                    
                    if status == 'SUCCEEDED':
                        output = result.get('output', [])
                        if output and len(output) > 0:
                            video_url = output[0]
                            if self.use_video_reference:
                                logger.info("🎉 VIDEO-TO-VIDEO generation completed!")
                            else:
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
            if self.use_video_reference:
                filename = f"runwayml_video_ref_{self.selected_dance}_{timestamp}.mp4"
            else:
                filename = f"runwayml_generation_{timestamp}.mp4"
