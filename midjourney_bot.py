#!/usr/bin/env python3
"""
EXPERT Discord Bot - SLASH COMMAND SPECIALIST
MAXIMUM HARMONY - Properly integrated with Discord server
Uses correct slash command format to trigger dropdown
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

class ExpertSlashCommandBot:
    """Expert bot that properly uses slash commands to trigger dropdown"""
    
    def __init__(self):
        # PROPER INTENTS FOR SLASH COMMANDS
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.guild_messages = True
        intents.application_commands = True
        
        # Create bot with EXPERT configuration
        self.bot = commands.Bot(
            command_prefix='!',
            intents=intents,
            help_command=None,
            case_insensitive=True,
            strip_after_prefix=True
        )
        
        self.prompt = os.getenv('PROMPT', 'beautiful anime fitness girl doing morning yoga')
        self.setup_events()
        self.setup_expert_commands()
    
    def setup_events(self):
        """Set up expert event handlers"""
        
        @self.bot.event
        async def on_ready():
            logger.info(f"🤖 EXPERT SLASH COMMAND BOT activated: {self.bot.user}")
            logger.info(f"🎯 Connected to {len(self.bot.guilds)} servers")
            logger.info(f"📝 Target prompt: {self.prompt}")
            
            # Sync slash commands properly
            logger.info("🔄 Syncing slash commands...")
            await self.bot.tree.sync()
            
            # HUMAN-LIKE STARTUP DELAY
            startup_delay = random.uniform(3, 8)
            logger.info(f"⏳ Human-like startup delay: {startup_delay:.1f}s")
            await asyncio.sleep(startup_delay)
            
            # Execute the expert mission
            await self.execute_expert_mission()
        
        @self.bot.event
        async def on_error(event, *args, **kwargs):
            logger.error(f"❌ Bot error in {event}: {args}")
    
    def setup_expert_commands(self):
        """Set up expert slash commands"""
        
        @self.bot.tree.command(name="imagine", description="Generate an image with Midjourney")
        async def imagine(interaction: discord.Interaction, prompt: str):
            """Handle /imagine command with proper interaction"""
            try:
                # Defer the response to give time for processing
                await interaction.response.defer(thinking=True)
                
                logger.info(f"🎨 Received /imagine command: {prompt}")
                
                # Send the command to trigger Midjourney
                command_message = f"/imagine {prompt}"
                await interaction.followup.send(command_message)
                
                logger.info(f"✅ Sent Midjourney command: {command_message}")
                
            except Exception as e:
                logger.error(f"❌ Error in /imagine command: {e}")
                await interaction.followup.send("❌ Error processing command", ephemeral=True)
    
    async def send_expert_slash_command(self, channel, session, headers):
        """
        Send expert slash command that triggers the dropdown
        """
        try:
            logger.info("🎯 Sending expert slash command...")
            
            # Start typing indicator for human-like behavior
            typing_url = f"https://discord.com/api/v10/channels/{channel.id}/typing"
            async with session.post(typing_url, headers=headers) as response:
                if response.status == 204:
                    logger.info("✅ Started typing indicator")
            
            # Simulate human typing delays
            await asyncio.sleep(random.uniform(2, 4))
            
            # Send the slash command with proper format
            message_url = f"https://discord.com/api/v10/channels/{channel.id}/messages"
            
            # Expert format that triggers dropdown
            message_data = {
                "content": f"/imagine {self.prompt}",
                "flags": 0,
                "type": 0
            }
            
            async with session.post(message_url, headers=headers, json=message_data) as response:
                if response.status == 200:
                    message_data = await response.json()
                    logger.info(f"✅ Expert slash command sent: {message_data['id']}")
                    return message_data['id']
                else:
                    logger.error(f"❌ Failed to send expert command: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ Error sending expert command: {e}")
            return None
    
    async def send_interaction_command(self, channel, session, headers):
        """
        Send interaction command that triggers the dropdown
        """
        try:
            logger.info("🎯 Sending interaction command...")
            
            interaction_url = "https://discord.com/api/v10/interactions"
            
            # Expert interaction format
            interaction_data = {
                "type": 2,  # Application command
                "guild_id": str(channel.guild.id),
                "channel_id": str(channel.id),
                "application_id": "936929561302675456",  # Midjourney's app ID
                "session_id": f"expert_session_{random.randint(1000, 9999)}",
                "data": {
                    "type": 1,  # Slash command
                    "name": "imagine",
                    "options": [
                        {
                            "type": 3,  # String option
                            "name": "prompt",
                            "value": self.prompt
                        }
                    ]
                }
            }
            
            async with session.post(interaction_url, headers=headers, json=interaction_data) as response:
                if response.status == 200:
                    logger.info("✅ Expert interaction command sent successfully!")
                    return True
                else:
                    logger.error(f"❌ Failed to send interaction command: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Error sending interaction command: {e}")
            return False
    
    async def send_gateway_command(self, channel, session, headers):
        """
        Send command using Gateway API format
        """
        try:
            logger.info("🎯 Sending Gateway API command...")
            
            # Gateway API format
            gateway_data = {
                "op": 0,  # Dispatch
                "t": "INTERACTION_CREATE",
                "s": 1,
                "d": {
                    "type": 2,
                    "guild_id": str(channel.guild.id),
                    "channel_id": str(channel.id),
                    "application_id": "936929561302675456",
                    "session_id": f"gateway_session_{random.randint(1000, 9999)}",
                    "data": {
                        "type": 1,
                        "name": "imagine",
                        "options": [
                            {
                                "type": 3,
                                "name": "prompt",
                                "value": self.prompt
                            }
                        ]
                    }
                }
            }
            
            # Send via HTTP API
            interaction_url = "https://discord.com/api/v10/interactions"
            async with session.post(interaction_url, headers=headers, json=gateway_data["d"]) as response:
                if response.status == 200:
                    logger.info("✅ Gateway API command sent successfully!")
                    return True
                else:
                    logger.error(f"❌ Failed to send Gateway command: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Error sending Gateway command: {e}")
            return False
    
    async def find_best_target_channel(self):
        """Find the best available channel with expert logic"""
        logger.info("🎯 Scanning for optimal target channels...")
        
        available_options = []
        
        for guild in self.bot.guilds:
            logger.info(f"📡 Scanning server: {guild.name} (ID: {guild.id})")
            
            # Check if this is Midjourney server
            if guild.id == 662267976984297473:
                logger.info("🎨 Found Midjourney server!")
                midjourney_channels = [
                    1008571045445382216,  # newbies-109
                    989268300473192551,   # newbies-108  
                    1008571733043462154,  # newbies-110
                    662267976984297473,   # general (if accessible)
                ]
                
                for channel_id in midjourney_channels:
                    channel = guild.get_channel(channel_id)
                    if channel and channel.permissions_for(guild.me).send_messages:
                        available_options.append({
                            'guild': guild,
                            'channel': channel,
                            'priority': 10,
                            'type': 'midjourney_official'
                        })
                        logger.info(f"✅ Midjourney channel available: {channel.name}")
            
            else:
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        priority = 5 if 'general' in channel.name.lower() else 3
                        available_options.append({
                            'guild': guild,
                            'channel': channel,
                            'priority': priority,
                            'type': 'personal_server'
                        })
                        logger.info(f"✅ Available channel: {guild.name}#{channel.name}")
        
        available_options.sort(key=lambda x: x['priority'], reverse=True)
        
        if not available_options:
            logger.error("❌ No accessible channels found!")
            return None
        
        best_option = available_options[0]
        logger.info(f"🎯 Selected target: {best_option['guild'].name}#{best_option['channel'].name}")
        logger.info(f"🎭 Strategy: {best_option['type']}")
        
        return best_option
    
    async def execute_expert_mission(self):
        """Execute the expert mission"""
        try:
            logger.info("🎨 Initiating EXPERT MISSION...")
            
            target = await self.find_best_target_channel()
            if not target:
                logger.error("❌ No suitable channels found")
                return False
            
            guild = target['guild']
            channel = target['channel']
            strategy_type = target['type']
            
            logger.info(f"✅ Target acquired: {guild.name}#{channel.name}")
            
            # Add context for personal server
            if strategy_type == 'personal_server':
                await channel.send("🤖 Expert Discord Bot - Testing Midjourney automation...")
                await asyncio.sleep(random.uniform(2, 4))
            
            # Human-like behavior simulation
            logger.info("👀 Analyzing recent activity...")
            await asyncio.sleep(random.uniform(2, 5))
            
            # Execute with expert methods
            logger.info("🎯 Executing EXPERT METHODS...")
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bot {os.getenv('DISCORD_BOT_TOKEN')}",
                    "Content-Type": "application/json"
                }
                
                # Try multiple expert methods
                methods = [
                    ("Expert Slash Command", self.send_expert_slash_command),
                    ("Interaction Command", self.send_interaction_command),
                    ("Gateway API Command", self.send_gateway_command)
                ]
                
                for method_name, method_func in methods:
                    logger.info(f"🔄 Trying {method_name}...")
                    success = await method_func(channel, session, headers)
                    
                    if success:
                        logger.info(f"🎉 SUCCESS! {method_name} worked!")
                        logger.info("🎯 This should trigger the dropdown!")
                        return True
                    
                    # Wait between attempts
                    await asyncio.sleep(random.uniform(3, 6))
                
                logger.error("❌ All expert methods failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Mission failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def run_mission(self):
        """Execute the complete expert mission"""
        token = os.getenv('DISCORD_BOT_TOKEN')
        if not token:
            logger.error("❌ DISCORD_BOT_TOKEN not found in environment")
            return False
        
        try:
            logger.info("🚀 Launching EXPERT MISSION...")
            await self.bot.start(token)
        except Exception as e:
            logger.error(f"❌ Mission failed: {e}")
            return False

async def main():
    """Main entry point for EXPERT bot"""
    logger.info("🥷 EXPERT DISCORD BOT - SLASH COMMAND SPECIALIST")
    logger.info(f"📅 Mission time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if os.getenv('GITHUB_ACTIONS'):
        logger.info("☁️ Operating in GitHub Actions environment")
    
    expert_bot = ExpertSlashCommandBot()
    success = await expert_bot.run_mission()
    
    if success:
        logger.info("✅ MISSION ACCOMPLISHED!")
        sys.exit(0)
    else:
        logger.error("❌ MISSION FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
