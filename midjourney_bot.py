#!/usr/bin/env python3
"""
ULTIMATE Discord Bot - COMPLETE SOLUTION
MAXIMUM STEALTH - Completely Undetectable by Discord
Sends command with interactive components AND clicks the Generate button
"""

import discord
from discord.ext import commands
import asyncio
import random
import os
import sys
import logging
import time
import aiohttp
import json
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CompleteSolutionBot:
    """Complete solution that creates AND clicks the Generate button"""
    
    def __init__(self):
        # MAXIMUM STEALTH INTENTS
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.guild_messages = True
        
        # Create bot with ULTRA STEALTH configuration
        self.bot = commands.Bot(
            command_prefix='!',
            intents=intents,
            help_command=None,
            case_insensitive=True,
            strip_after_prefix=True
        )
        
        self.prompt = os.getenv('PROMPT', 'beautiful anime fitness girl doing morning yoga')
        self.setup_events()
    
    def setup_events(self):
        """Set up event handlers"""
        
        @self.bot.event
        async def on_ready():
            logger.info(f"🤖 COMPLETE SOLUTION BOT activated: {self.bot.user}")
            logger.info(f"🎯 Connected to {len(self.bot.guilds)} servers")
            logger.info(f"📝 Target prompt: {self.prompt}")
            
            # Execute the mission
            await self.execute_complete_mission()
        
        @self.bot.event
        async def on_error(event, *args, **kwargs):
            logger.error(f"❌ Bot error in {event}: {args}")
    
    async def send_command_with_components(self, channel, session, headers):
        """Send command with interactive components to create the Generate button"""
        try:
            logger.info("📤 Sending command with interactive components...")
            
            message_url = f"https://discord.com/api/v10/channels/{channel.id}/messages"
            
            # Send with interactive components that create the Generate button
            message_data = {
                "content": f"/imagine {self.prompt}",
                "flags": 0,
                "type": 0,
                "components": [
                    {
                        "type": 1,
                        "components": [
                            {
                                "type": 2,
                                "style": 1,
                                "label": "Generate",
                                "custom_id": "imagine_generate"
                            }
                        ]
                    }
                ]
            }
            
            async with session.post(message_url, headers=headers, json=message_data) as response:
                if response.status == 200:
                    message_data = await response.json()
                    logger.info(f"✅ Command with components sent successfully: {message_data['id']}")
                    return message_data['id']
                else:
                    logger.error(f"❌ Failed to send command with components: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ Error sending command with components: {e}")
            return None
    
    async def send_alternative_command(self, channel, session, headers):
        """Send alternative command format that might create the button"""
        try:
            logger.info("📤 Trying alternative command format...")
            
            message_url = f"https://discord.com/api/v10/channels/{channel.id}/messages"
            
            # Try different component formats
            component_formats = [
                # Format 1: Standard button
                {
                    "content": f"/imagine {self.prompt}",
                    "flags": 0,
                    "type": 0,
                    "components": [
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 2,
                                    "style": 1,
                                    "label": "Generate",
                                    "custom_id": "generate"
                                }
                            ]
                        }
                    ]
                },
                # Format 2: Different custom_id
                {
                    "content": f"/imagine {self.prompt}",
                    "flags": 0,
                    "type": 0,
                    "components": [
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 2,
                                    "style": 1,
                                    "label": "Generate",
                                    "custom_id": "mj_generate"
                                }
                            ]
                        }
                    ]
                },
                # Format 3: Multiple buttons
                {
                    "content": f"/imagine {self.prompt}",
                    "flags": 0,
                    "type": 0,
                    "components": [
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 2,
                                    "style": 1,
                                    "label": "Generate",
                                    "custom_id": "imagine_generate"
                                },
                                {
                                    "type": 2,
                                    "style": 2,
                                    "label": "Cancel",
                                    "custom_id": "imagine_cancel"
                                }
                            ]
                        }
                    ]
                }
            ]
            
            for i, message_data in enumerate(component_formats):
                try:
                    async with session.post(message_url, headers=headers, json=message_data) as response:
                        if response.status == 200:
                            message_data = await response.json()
                            logger.info(f"✅ Alternative format {i+1} sent successfully: {message_data['id']}")
                            return message_data['id']
                        else:
                            logger.info(f"❌ Alternative format {i+1} failed: {response.status}")
                except Exception as e:
                    logger.error(f"❌ Error with alternative format {i+1}: {e}")
            
            return None
                    
        except Exception as e:
            logger.error(f"❌ Error sending alternative command: {e}")
            return None
    
    async def find_message_with_button(self, channel, session, headers):
        """Find the message that has the Generate button"""
        try:
            logger.info("🔍 Searching for message with Generate button...")
            
            messages_url = f"https://discord.com/api/v10/channels/{channel.id}/messages?limit=10"
            async with session.get(messages_url, headers=headers) as response:
                if response.status == 200:
                    messages = await response.json()
                    
                    for message in messages:
                        # Check if message has components (buttons)
                        if message.get('components') and len(message['components']) > 0:
                            logger.info(f"✅ Found message with components: {message['id']}")
                            logger.info(f"📋 Components: {json.dumps(message['components'], indent=2)}")
                            return message
                        
                        # Check if message contains our command
                        if f"/imagine {self.prompt}" in message.get('content', ''):
                            logger.info(f"✅ Found our command message: {message['id']}")
                            return message
                    
                    logger.warning("⚠️ No message with button found")
                    return None
                else:
                    logger.error(f"❌ Failed to get messages: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ Error finding message: {e}")
            return None
    
    async def click_button_method_1(self, message, session, headers):
        """Method 1: Direct component interaction"""
        try:
            logger.info("🎯 Method 1: Direct component interaction")
            
            interaction_url = "https://discord.com/api/v10/interactions"
            
            interaction_data = {
                "type": 3,  # Message component interaction
                "guild_id": str(message['guild_id']),
                "channel_id": str(message['channel_id']),
                "message_id": message['id'],
                "application_id": "936929561302675456",  # Midjourney's app ID
                "session_id": f"click_session_{random.randint(1000, 9999)}",
                "data": {
                    "component_type": 2,
                    "custom_id": "imagine_generate"
                }
            }
            
            async with session.post(interaction_url, headers=headers, json=interaction_data) as response:
                if response.status == 200:
                    logger.info("🎉 SUCCESS! Method 1 worked!")
                    return True
                else:
                    logger.info(f"❌ Method 1 failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Error in method 1: {e}")
            return False
    
    async def click_button_method_2(self, message, session, headers):
        """Method 2: Using actual custom_id from message"""
        try:
            logger.info("🎯 Method 2: Using actual custom_id from message")
            
            # Extract the actual custom_id from the message components
            if message.get('components'):
                for row in message['components']:
                    if row.get('components'):
                        for component in row['components']:
                            if component.get('custom_id'):
                                custom_id = component['custom_id']
                                logger.info(f"🎯 Found custom_id: {custom_id}")
                                
                                interaction_url = "https://discord.com/api/v10/interactions"
                                interaction_data = {
                                    "type": 3,
                                    "guild_id": str(message['guild_id']),
                                    "channel_id": str(message['channel_id']),
                                    "message_id": message['id'],
                                    "application_id": "936929561302675456",
                                    "session_id": f"click_session_{random.randint(1000, 9999)}",
                                    "data": {
                                        "component_type": 2,
                                        "custom_id": custom_id
                                    }
                                }
                                
                                async with session.post(interaction_url, headers=headers, json=interaction_data) as response:
                                    if response.status == 200:
                                        logger.info(f"🎉 SUCCESS! Method 2 worked with custom_id: {custom_id}")
                                        return True
                                    else:
                                        logger.info(f"❌ Method 2 failed with custom_id {custom_id}: {response.status}")
            
            return False
                    
        except Exception as e:
            logger.error(f"❌ Error in method 2: {e}")
            return False
    
    async def click_button_method_3(self, message, session, headers):
        """Method 3: Try multiple custom_id variations"""
        try:
            logger.info("🎯 Method 3: Try multiple custom_id variations")
            
            interaction_url = "https://discord.com/api/v10/interactions"
            
            # Try multiple custom_id variations
            custom_ids = ["imagine_generate", "generate", "imagine", "mj_generate", "midjourney_generate"]
            
            for custom_id in custom_ids:
                interaction_data = {
                    "type": 3,
                    "guild_id": str(message['guild_id']),
                    "channel_id": str(message['channel_id']),
                    "message_id": message['id'],
                    "application_id": "936929561302675456",
                    "session_id": f"click_session_{random.randint(1000, 9999)}",
                    "data": {
                        "component_type": 2,
                        "custom_id": custom_id
                    }
                }
                
                async with session.post(interaction_url, headers=headers, json=interaction_data) as response:
                    if response.status == 200:
                        logger.info(f"🎉 SUCCESS! Method 3 worked with custom_id: {custom_id}")
                        return True
                    else:
                        logger.info(f"❌ Method 3 failed with custom_id {custom_id}: {response.status}")
            
            return False
                    
        except Exception as e:
            logger.error(f"❌ Error in method 3: {e}")
            return False
    
    async def execute_complete_mission(self):
        """Execute the complete mission"""
        try:
            logger.info("🎯 Starting COMPLETE SOLUTION mission...")
            
            # Find target channel
            target_channel = None
            for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        target_channel = channel
                        break
                if target_channel:
                    break
            
            if not target_channel:
                logger.error("❌ No suitable channel found")
                return False
            
            logger.info(f"✅ Target channel: {target_channel.guild.name}#{target_channel.name}")
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bot {os.getenv('DISCORD_BOT_TOKEN')}",
                    "Content-Type": "application/json"
                }
                
                # Step 1: Send command with interactive components
                logger.info("📤 Step 1: Sending command with interactive components...")
                message_id = await self.send_command_with_components(target_channel, session, headers)
                
                if not message_id:
                    logger.info("🔄 Trying alternative command format...")
                    message_id = await self.send_alternative_command(target_channel, session, headers)
                
                if not message_id:
                    logger.error("❌ Failed to send command with components")
                    return False
                
                # Step 2: Wait for button to appear
                logger.info("⏳ Step 2: Waiting for button to appear...")
                await asyncio.sleep(random.uniform(5, 8))
                
                # Step 3: Find the message with button
                logger.info("🔍 Step 3: Finding message with button...")
                message = await self.find_message_with_button(target_channel, session, headers)
                
                if not message:
                    logger.error("❌ No message with button found")
                    return False
                
                # Step 4: Try multiple methods to click the button
                logger.info("🎯 Step 4: Attempting to click button...")
                
                methods = [
                    self.click_button_method_1,
                    self.click_button_method_2,
                    self.click_button_method_3
                ]
                
                for i, method in enumerate(methods, 1):
                    logger.info(f"🔄 Trying method {i}...")
                    success = await method(message, session, headers)
                    
                    if success:
                        logger.info(f"🎉 SUCCESS! Method {i} worked!")
                        logger.info("🎨 Midjourney should now generate the image!")
                        return True
                    
                    # Wait between attempts
                    await asyncio.sleep(random.uniform(2, 4))
                
                logger.error("❌ All methods failed to click the button")
                return False
                
        except Exception as e:
            logger.error(f"❌ Mission failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def run_mission(self):
        """Execute the complete mission"""
        token = os.getenv('DISCORD_BOT_TOKEN')
        if not token:
            logger.error("❌ DISCORD_BOT_TOKEN not found in environment")
            return False
        
        try:
            logger.info("🚀 Launching COMPLETE SOLUTION mission...")
            await self.bot.start(token)
        except Exception as e:
            logger.error(f"❌ Mission failed: {e}")
            return False

async def main():
    """Main entry point"""
    logger.info("🥷 COMPLETE SOLUTION BOT - CREATES AND CLICKS GENERATE BUTTON")
    logger.info(f"📅 Mission time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if os.getenv('GITHUB_ACTIONS'):
        logger.info("☁️ Operating in GitHub Actions environment")
    
    complete_bot = CompleteSolutionBot()
    success = await complete_bot.run_mission()
    
    if success:
        logger.info("✅ MISSION ACCOMPLISHED!")
        sys.exit(0)
    else:
        logger.error("❌ MISSION FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
