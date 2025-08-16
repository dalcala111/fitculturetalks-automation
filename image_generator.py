#!/usr/bin/env python3
"""
OPTIMIZED RUNWAYML REFERENCE VIDEO GENERATOR
Streamlined for reference video-to-video generation with Deuce the Shih Tzu
Focused on using your manual prompt format that works!
"""

import time
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

class OptimizedReferenceVideoGenerator:
    """Streamlined generator focused on reference video-to-video generation"""
    
    def __init__(self):
        # Core parameters from your working setup
        self.runway_prompt = os.getenv('RUNWAY_PROMPT', '')
        self.selected_dance = os.getenv('SELECTED_DANCE', 'reference_dance')
        self.runwayml_api_key = os.getenv('RUNWAYML_API_KEY')
        
        # Essential video reference parameters only
        self.reference_strength = float(os.getenv('REFERENCE_STRENGTH', '0.8'))
        self.motion_score = int(os.getenv('MOTION_SCORE', '7'))  # Your manual setting
        
        # Basic generation settings
        self.duration = 10
        self.aspect_ratio = "9:16"
        self.watermark = False
        
        logger.info(f"🎯 Using prompt: {self.runway_prompt[:100]}...")
        logger.info(f"💃 Dance type: {self.selected_dance}")
        logger.info(f"🎯 Reference strength: {self.reference_strength}")
        logger.info(f"🎬 Motion score: {self.motion_score}")
        
    def find_reference_video(self):
        """Find the downloaded reference video file"""
        try:
            reference_patterns = ["reference_video.*", "reference_video.mp4"]
            
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
        """Convert video file to base64 for RunwayML"""
        try:
            with open(video_path, 'rb') as f:
                video_data = f.read()
                base64_video = base64.b64encode(video_data).decode('utf-8')
                
            logger.info(f"✅ Reference video converted to base64 ({len(base64_video)} chars)")
            return base64_video
                
        except Exception as e:
            logger.error(f"❌ Error converting reference video: {e}")
            return None
    
    def generate_video_with_reference(self):
        """Generate video using reference video - simplified version"""
        try:
            logger.info("🎥 Starting reference video generation...")
            
            if not self.runwayml_api_key:
                logger.error("❌ RUNWAYML_API_KEY not found")
                return False
            
            if not self.runway_prompt:
                logger.error("❌ No runway prompt provided")
                return False
            
            # Find and convert reference video
            reference_video_path = self.find_reference_video()
            if not reference_video_path:
                return False
            
            reference_video_b64 = self.convert_video_to_base64(reference_video_path)
            if not reference_video_b64:
                return False
            
            # Simple RunwayML API call matching your manual success
            headers = {
                "Authorization": f"Bearer {self.runwayml_api_key}",
                "Content-Type": "application/json"
            }
            
            # Use exact same parameters that worked manually
            payload = {
                "promptText": self.runway_prompt,
                "init_video": reference_video_b64,
                "duration": self.duration,
                "ratio": self.aspect_ratio,
                "watermark": self.watermark,
                "motionScore": self.motion_score
            }
            
            logger.info("🚀 Sending request to RunwayML...")
            logger.info(f"📝 Prompt: {self.runway_prompt[:100]}...")
            
            # Use the correct RunwayML API endpoint
            response = requests.post(
                "https://api.dev.runwayml.com/v1/image_to_video",
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                task_id = result.get('id')
                
                logger.info(f"✅ Generation started! Task ID: {task_id}")
                
                # Wait for completion
                video_url = self.wait_for_completion(task_id, headers)
                
                if video_url:
                    # Download and save video
                    video_data = self.download_video(video_url)
                    if video_data:
                        self.save_video(video_data)
                        return True
                        
                return False
                    
            else:
                logger.error(f"❌ RunwayML API error: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error generating video: {e}")
            return False
    
    def wait_for_completion(self, task_id, headers, max_wait=600):
        """Wait for RunwayML to complete video generation"""
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
                    
                    logger.info(f"🔄 Status: {status} - Progress: {progress}%")
                    
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
                        time.sleep(20)
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
            
            response = requests.get(video_url, timeout=120)
            
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
    
    def save_video(self, video_data):
        """Save the generated video"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"runwayml_generation_{timestamp}.mp4"
            
            # Save with timestamp
            with open(filename, 'wb') as f:
                f.write(video_data)
            logger.info(f"💾 Video saved as: {filename}")
            
            # Save as expected output file
            with open("final_animation.mp4", 'wb') as f:
                f.write(video_data)
            
            logger.info("🎬 REFERENCE VIDEO GENERATION COMPLETED!")
            logger.info(f"💃 Dance: {self.selected_dance}")
            logger.info("📱 Ready for processing!")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving video: {e}")
            return False
    
    def run(self):
        """Main execution"""
        try:
            logger.info("🎬 OPTIMIZED REFERENCE VIDEO GENERATOR STARTING...")
            logger.info(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"💃 Dance: {self.selected_dance}")
            logger.info(f"📝 Using your successful manual prompt format")
            
            success = self.generate_video_with_reference()
            
            if success:
                logger.info("✅ REFERENCE VIDEO GENERATION SUCCESSFUL!")
                return True
            else:
                logger.error("❌ Reference video generation failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Generation failed: {e}")
            return False

def main():
    """Main entry point"""
    logger.info("🎬 OPTIMIZED RUNWAYML REFERENCE VIDEO GENERATOR")
    logger.info("🎯 Focused on your working manual prompt format")
    logger.info("💃 Streamlined for reference video success")
    
    if os.getenv('GITHUB_ACTIONS'):
        logger.info("☁️ Running in GitHub Actions")
    
    # Create and run generator
    generator = OptimizedReferenceVideoGenerator()
    success = generator.run()
    
    if success:
        logger.info("✅ MISSION ACCOMPLISHED!")
        sys.exit(0)
    else:
        logger.error("❌ MISSION FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()
