import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import imageio
import glob
import random

def create_dynamic_shih_tzu_animation(image_path, animation_type="eating", output_path="final_animation.mp4"):
    """
    Create dynamic Shih Tzu animations with simulated movement
    """
    print(f"🐕 Creating DYNAMIC Shih Tzu {animation_type} animation from: {image_path}")
    
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Could not load image: {image_path}")
        return False
        
    height, width = img.shape[:2]
    print(f"📏 Original image size: {width}x{height}")
    
    # Social media format
    target_width = 1080
    target_height = 1920
    
    # Scale and prepare base image
    scale = min(target_width/width, target_height/height) * 0.85
    new_width = int(width * scale)
    new_height = int(height * scale)
    img_resized = cv2.resize(img, (new_width, new_height))
    
    # Animation parameters
    fps = 30
    duration = 8
    total_frames = fps * duration
    frames = []
    
    print(f"🎭 Creating {total_frames} frames with DYNAMIC movement...")
    
    for frame_num in range(total_frames):
        progress = frame_num / total_frames
        
        # Create dynamic background
        background = create_animated_background(target_height, target_width, progress)
        
        # Apply dynamic animation based on type
        if animation_type == 'emergence':
            frame = create_magical_emergence(background, img_resized, progress, target_width, target_height)
        elif animation_type == 'dancing':
            frame = create_bouncy_dance(background, img_resized, progress, target_width, target_height)
        else:  # eating
            frame = create_eating_motion(background, img_resized, progress, target_width, target_height)
        
        # Add floating particles and effects
        frame = add_floating_particles(frame, animation_type, progress)
        
        # Add dynamic text with animation
        frame = add_dynamic_text(frame, animation_type, progress)
        
        # Convert and store
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame_rgb)
        
        if frame_num % 30 == 0:
            print(f"⏳ Frame {frame_num}/{total_frames} - {animation_type} animation")
    
    # Save high-quality video
    print("💾 Saving dynamic animation...")
    imageio.mimsave(output_path, frames, fps=fps, quality=9)
    print(f"✅ Dynamic Shih Tzu animation saved!")
    
    return True

def create_animated_background(height, width, progress):
    """Create animated gradient background that changes over time"""
    background = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Animated color cycling
    time_cycle = progress * 2 * np.pi
    
    for y in range(height):
        ratio = y / height
        
        # Dynamic colors that shift over time
        r_base = 240 + np.sin(time_cycle) * 15
        g_base = 220 + np.sin(time_cycle + np.pi/3) * 20
        b_base = 255 + np.sin(time_cycle + 2*np.pi/3) * 10
        
        r = int(r_base * (1 - ratio * 0.2))
        g = int(g_base * (1 - ratio * 0.1))
        b = int(b_base - ratio * 20)
        
        background[y, :] = [max(0, min(255, b)), max(0, min(255, g)), max(0, min(255, r))]
    
    return background

def create_magical_emergence(background, img, progress, target_width, target_height):
    """Simulate Shih Tzu magically emerging with realistic effects"""
    frame = background.copy()
    
    # Emergence phases
    if progress < 0.3:
        # Phase 1: Just sparkles and anticipation
        alpha = 0
        emergence_scale = 0
    elif progress < 0.6:
        # Phase 2: Gradual emergence
        emergence_progress = (progress - 0.3) / 0.3
        alpha = emergence_progress
        emergence_scale = 0.3 + emergence_progress * 0.7
        
        # Add "popping" effect
        pop_intensity = np.sin(emergence_progress * np.pi) * 0.2
        emergence_scale += pop_intensity
    else:
        # Phase 3: Full visibility with joy bounce
        alpha = 1.0
        joy_bounce = np.sin((progress - 0.6) * 10 * np.pi) * 0.1
        emergence_scale = 1.0 + joy_bounce
    
    if alpha > 0:
        # Apply emergence scaling
        img_height, img_width = img.shape[:2]
        new_height = int(img_height * emergence_scale)
        new_width = int(img_width * emergence_scale)
        
        if new_height > 0 and new_width > 0:
            scaled_img = cv2.resize(img, (new_width, new_height))
            
            # Center positioning with slight upward movement during emergence
            y_offset = (target_height - new_height) // 2
            x_offset = (target_width - new_width) // 2
            
            # Emergence movement - rising effect
            if progress < 0.6:
                y_offset += int((1 - (progress - 0.3) / 0.3) * 50)
            
            # Apply alpha blending
            alpha_img = (scaled_img * alpha).astype(np.uint8)
            
            # Blend onto background
            end_y = min(y_offset + new_height, target_height)
            end_x = min(x_offset + new_width, target_width)
            start_y = max(0, y_offset)
            start_x = max(0, x_offset)
            
            crop_start_y = max(0, -y_offset)
            crop_start_x = max(0, -x_offset)
            crop_end_y = crop_start_y + (end_y - start_y)
            crop_end_x = crop_start_x + (end_x - start_x)
            
            frame[start_y:end_y, start_x:end_x] = alpha_img[crop_start_y:crop_end_y, crop_start_x:crop_end_x]
    
    return frame

def create_bouncy_dance(background, img, progress, target_width, target_height):
    """Simulate energetic dancing with multiple movement layers"""
    frame = background.copy()
    
    # Multiple rhythm layers for complex movement
    main_bounce = np.sin(progress * 8 * np.pi) * 30  # Main vertical bounce
    side_sway = np.sin(progress * 6 * np.pi) * 20    # Side-to-side sway
    micro_bounce = np.sin(progress * 20 * np.pi) * 8  # Quick micro-movements
    
    # Scale pulsing with the beat
    scale_pulse = 1.0 + np.sin(progress * 12 * np.pi) * 0.15
    
    # Rotation for dance spin
    rotation = np.sin(progress * 4 * np.pi) * 8
    
    # Apply transformations
    img_height, img_width = img.shape[:2]
    scaled_height = int(img_height * scale_pulse)
    scaled_width = int(img_width * scale_pulse)
    
    if scaled_height > 0 and scaled_width > 0:
        scaled_img = cv2.resize(img, (scaled_width, scaled_height))
        
        # Calculate dynamic position
        center_y = target_height // 2 + int(main_bounce + micro_bounce)
        center_x = target_width // 2 + int(side_sway)
        
        # Apply rotation
        rotation_matrix = cv2.getRotationMatrix2D((scaled_width//2, scaled_height//2), rotation, 1.0)
        rotated_img = cv2.warpAffine(scaled_img, rotation_matrix, (scaled_width, scaled_height))
        
        # Position on frame
        y_offset = center_y - scaled_height // 2
        x_offset = center_x - scaled_width // 2
        
        # Ensure bounds
        end_y = min(y_offset + scaled_height, target_height)
        end_x = min(x_offset + scaled_width, target_width)
        start_y = max(0, y_offset)
        start_x = max(0, x_offset)
        
        if start_y < end_y and start_x < end_x:
            crop_start_y = max(0, -y_offset)
            crop_start_x = max(0, -x_offset)
            crop_end_y = crop_start_y + (end_y - start_y)
            crop_end_x = crop_start_x + (end_x - start_x)
            
            frame[start_y:end_y, start_x:end_x] = rotated_img[crop_start_y:crop_end_y, crop_start_x:crop_end_x]
    
    return frame

def create_eating_motion(background, img, progress, target_width, target_height):
    """Simulate realistic eating with head movements and satisfaction"""
    frame = background.copy()
    
    # Eating rhythm - multiple bites throughout animation
    bite_cycle = np.sin(progress * 6 * np.pi)
    bite_intensity = (bite_cycle + 1) / 2  # Normalize to 0-1
    
    # Head movement during eating
    head_tilt = np.sin(progress * 8 * np.pi) * 3
    head_forward = bite_intensity * 15  # Lean forward when biting
    
    # Satisfaction scaling - slightly bigger when happy
    satisfaction = 1.0 + bite_intensity * 0.08
    
    # Subtle up-down motion while eating
    eating_bob = np.sin(progress * 10 * np.pi) * 8
    
    # Apply transformations
    img_height, img_width = img.shape[:2]
    scaled_height = int(img_height * satisfaction)
    scaled_width = int(img_width * satisfaction)
    
    if scaled_height > 0 and scaled_width > 0:
        scaled_img = cv2.resize(img, (scaled_width, scaled_height))
        
        # Create eating movement matrix
        center_x = scaled_width // 2
        center_y = scaled_height // 2
        
        # Combine head tilt with forward motion
        M = cv2.getRotationMatrix2D((center_x, center_y), head_tilt, 1.0)
        # Add forward motion (translation)
        M[0, 2] += head_forward * np.cos(np.radians(head_tilt))
        M[1, 2] += head_forward * np.sin(np.radians(head_tilt))
        
        eating_img = cv2.warpAffine(scaled_img, M, (scaled_width, scaled_height))
        
        # Position with eating bob
        center_frame_y = target_height // 2 + int(eating_bob)
        center_frame_x = target_width // 2
        
        y_offset = center_frame_y - scaled_height // 2
        x_offset = center_frame_x - scaled_width // 2
        
        # Blend onto frame
        end_y = min(y_offset + scaled_height, target_height)
        end_x = min(x_offset + scaled_width, target_width)
        start_y = max(0, y_offset)
        start_x = max(0, x_offset)
        
        if start_y < end_y and start_x < end_x:
            crop_start_y = max(0, -y_offset)
            crop_start_x = max(0, -x_offset)
            crop_end_y = crop_start_y + (end_y - start_y)
            crop_end_x = crop_start_x + (end_x - start_x)
            
            frame[start_y:end_y, start_x:end_x] = eating_img[crop_start_y:crop_end_y, crop_start_x:crop_end_x]
    
    return frame

def add_floating_particles(frame, animation_type, progress):
    """Add floating particles and magical effects"""
    height, width = frame.shape[:2]
    
    # Different particle systems for different animations
    if animation_type == 'emergence':
        # Magical sparkles emerging from center
        num_particles = int(30 + progress * 50)
        for i in range(num_particles):
            # Particles emerge from center and float outward
            t = (progress + i * 0.1) % 1.0
            angle = random.uniform(0, 2 * np.pi)
            radius = t * 300
            
            x = int(width // 2 + np.cos(angle) * radius)
            y = int(height // 2 + np.sin(angle) * radius - t * 100)  # Rise up
            
            if 0 <= x < width and 0 <= y < height:
                size = random.randint(2, 6)
                alpha = 1.0 - t  # Fade out as they float away
                
                # Sparkle colors
                colors = [(0, 255, 255), (255, 255, 0), (255, 255, 255)]
                color = random.choice(colors)
                
                # Draw with alpha
                cv2.circle(frame, (x, y), size, color, -1)
                
    elif animation_type == 'dancing':
        # Energy particles bouncing around
        num_particles = 40
        for i in range(num_particles):
            t = (progress * 3 + i * 0.25) % 1.0
            bounce = abs(np.sin(t * np.pi))
            
            x = int((i / num_particles) * width)
            y = int(height * (0.3 + bounce * 0.4))
            
            size = int(3 + bounce * 4)
            colors = [(0, 255, 255), (255, 100, 255), (100, 255, 255)]
            color = colors[i % len(colors)]
            
            cv2.circle(frame, (x, y), size, color, -1)
            
    else:  # eating
        # Gentle floating hearts and satisfaction particles
        num_particles = 15
        for i in range(num_particles):
            t = (progress + i * 0.2) % 1.0
            
            x = int(width * (0.2 + 0.6 * ((i / num_particles))))
            y = int(height * (0.8 - t * 0.6))  # Float upward
            
            if 0 <= x < width and 0 <= y < height:
                size = random.randint(3, 8)
                alpha = 1.0 - t
                
                # Heart-like effect with pink/red colors
                colors = [(255, 182, 193), (255, 105, 180), (255, 20, 147)]  # Light pink to deep pink
                color = random.choice(colors)
                
                cv2.circle(frame, (x, y), size, color, -1)
    
    return frame

def add_dynamic_text(frame, animation_type, progress):
    """Add dynamic animated text"""
    height, width = frame.shape[:2]
    
    # Text content based on animation
    texts = {
        'emergence': ['✨ MAGIC!', '🐕 SURPRISE!', '💫 AMAZING!'],
        'eating': ['😋 YUM YUM!', '🍽️ SO GOOD!', '❤️ HAPPY PUP!'],
        'dancing': ['🎵 DANCING!', '💃 GROOVE!', '🎉 PARTY TIME!']
    }
    
    text_list = texts.get(animation_type, texts['eating'])
    
    # Cycle through texts
    text_phase = int(progress * len(text_list) * 2) % len(text_list)
    text = text_list[text_phase]
    
    # Dynamic text animation
    bounce = np.sin(progress * 15 * np.pi) * 20
    scale_pulse = 1.0 + np.sin(progress * 10 * np.pi) * 0.3
    
    # Position and styling
    font_scale = 1.5 * scale_pulse
    thickness = max(1, int(3 * scale_pulse))
    
    (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
    
    x = (width - text_width) // 2
    y = int(200 + bounce)
    
    # Add shadow
    cv2.putText(frame, text, (x + 4, y + 4), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness + 2)
    
    # Main text with dynamic color
    color_cycle = progress * 2 * np.pi
    r = int(255 * (0.5 + 0.5 * np.sin(color_cycle)))
    g = int(255 * (0.5 + 0.5 * np.sin(color_cycle + 2*np.pi/3)))
    b = int(255 * (0.5 + 0.5 * np.sin(color_cycle + 4*np.pi/3)))
    
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (b, g, r), thickness)
    
    return frame

def main():
    print("🐕 DYNAMIC SHIH TZU ANIMATION GENERATOR STARTING...")
    
    animation_type = os.environ.get('ANIMATION_TYPE', 'eating')
    print(f"🎬 Creating DYNAMIC {animation_type} animation...")
    
    # Find image files
    image_patterns = ["dalle_generation_*.png", "dalle_generation_*.jpg", "*.png", "*.jpg"]
    
    image_files = []
    for pattern in image_patterns:
        found_files = glob.glob(pattern)
        if found_files:
            image_files.extend(found_files)
            break
    
    if not image_files:
        print("❌ No image files found!")
        return False
        
    image_path = image_files[0]
    print(f"🖼️  Using image: {image_path}")
    
    # Create dynamic animation
    success = create_dynamic_shih_tzu_animation(image_path, animation_type)
    
    if success:
        print("🎉 DYNAMIC Shih Tzu animation created!")
        size = os.path.getsize("final_animation.mp4") / (1024*1024)
        print(f"📊 Size: {size:.2f} MB")
        print("🚀 This will be much more engaging!")
    
    return success

if __name__ == "__main__":
    main()
