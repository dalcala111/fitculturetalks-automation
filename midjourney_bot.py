#!/usr/bin/env python3
"""
ULTIMATE HYBRID DISCORD BOT - MAXIMUM POWER
Combines ULTRA STEALTH human behavior + EXPERT slash command methods
The most sophisticated Discord automation ever created
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

class UltimateHybridBot:
    """ULTIMATE bot combining stealth behavior with expert API methods"""
    
    def __init__(self):
        # HYBRID INTENTS - Best of both worlds
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.guild_messages = True
        
        # Create bot with ULTIMATE configuration
        self.bot = commands.Bot(
            command_prefix='!',
            intents=intents,
            help_command=None,
            case_insensitive=True,
            strip_after_prefix=True
        )
        
        self.prompt = os.getenv('PROMPT', 'beautiful anime fitness girl doing morning yoga')
        
        # ULTRA REALISTIC DELAYS (from our stealth version)
        self.human_delays = {
            'think_time': (2, 5),
            'typing_speed': (0.05, 0.15),
            'pause_chance': 0.08,
            'pause_duration': (0.3, 1.2),
            'post_command_wait': (3, 7)
        }
        
        self.setup_events()
        self.setup_hybrid_commands()
    
    def setup_events(self):
        """Set up ULTIMATE hybrid event handlers"""
        
        @self.bot.event
        async def on_ready():
            logger.info(f"🚀 ULTIMATE HYBRID BOT activated: {self.bot.user}")
            logger.info(f"🎯 Connected to {len(self.bot.guilds)} servers")
            logger.info(f"📝 Target prompt: {self.prompt}")
            
            # Sync slash commands like expert version
            try:
                logger.info("🔄 Syncing slash commands...")
                await self.bot.tree.sync()
                logger.info("✅ Slash commands synced successfully")
            except Exception as e:
                logger.warning(f"⚠️ Could not sync slash commands: {e}")
            
            # ULTRA REALISTIC startup delay (from stealth version)
            startup_delay = random.uniform(3, 8)
            logger.info(f"⏳ Human-like startup delay: {startup_delay:.1f}s")
            await asyncio.sleep(startup_delay)
            
            # Execute the ULTIMATE mission
            await self.execute_ultimate_mission()
        
        @self.bot.event
        async def on_error(event, *args, **kwargs):
            logger.error(f"❌ Bot error in {event}: {args}")
    
    def setup_hybrid_commands(self):
        """Set up hybrid slash commands"""
        
        @self.bot.tree.command(name="imagine", description="Generate an image with Midjourney")
        async def imagine(interaction: discord.Interaction, prompt: str):
            """Handle /imagine command with hybrid approach"""
            try:
                await interaction.response.defer(thinking=True)
                logger.info(f"🎨 Received /imagine command: {prompt}")
                
                # Use expert API method for response
                await self.send_expert_api_command(interaction.channel, prompt)
                await interaction.followup.send(f"🎯 Midjourney command sent: {prompt}")
                
            except Exception as e:
                logger.error(f"❌ Error in /imagine command: {e}")
                await interaction.followup.send("❌ Error processing command", ephemeral=True)
    
    async def human_type_simulation(self, content):
        """ULTRA REALISTIC typing simulation (from stealth version)"""
        typing_pattern = []
        
        for i, char in enumerate(content):
            typing_pattern.append(char)
            
            if i == 0:
                delay = random.uniform(0.2, 0.5)
            elif char == ' ':
                delay = random.uniform(0.1, 0.3)
            elif char in '.,!?':
                delay = random.uniform(0.2, 0.4)
            else:
                base_delay = random.uniform(*self.human_delays['typing_speed'])
                if random.random() < self.human_delays['pause_chance']:
                    hesitation = random.uniform(*self.human_delays['pause_duration'])
                    base_delay += hesitation
                    logger.info(f"💭 Human hesitation: {hesitation:.2f}s")
                delay = base_delay
            
            typing_pattern.append(delay)
        
        return typing_pattern
    
    async def send_expert_api_command(self, channel, prompt_text):
        """EXPERT API method from Cursor code"""
        try:
            logger.info("🎯 Using EXPERT API method...")
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bot {os.getenv('DISCORD_BOT_TOKEN')}",
                    "Content-Type": "application/json",
                    "User-Agent": "DiscordBot (https://github.com/discord/discord-api-docs, 1.0)"
                }
                
                # Expert interaction format (from Cursor code)
                interaction_url = "https://discord.com/api/v10/interactions"
                
                interaction_data = {
                    "type": 2,  # Application command
                    "guild_id": str(channel.guild.id),
                    "channel_id": str(channel.id),
                    "application_id": "936929561302675456",  # Midjourney's app ID
                    "session_id": f"hybrid_session_{random.randint(1000, 9999)}",
                    "data": {
                        "type": 1,  # Slash command
                        "name": "imagine",
                        "options": [
                            {
                                "type": 3,  # String option
                                "name": "prompt",
                                "value": prompt_text
                            }
                        ]
                    }
                }
                
                async with session.post(interaction_url, headers=headers, json=interaction_data) as response:
                    if response.status == 200:
                        logger.info("🎉 EXPERT API command sent successfully!")
                        return True
                    else:
                        logger.error(f"❌ API command failed: {response.status}")
                        response_text = await response.text()
                        logger.error(f"Response: {response_text}")
                        return False
                        
        except Exception as e:
            logger.error(f"❌ Error in expert API method: {e}")
            return False
    
    async def send_stealth_message_command(self, channel):
        """ULTRA STEALTH message method (our original approach)"""
        try:
            logger.info("🥷 Using ULTRA STEALTH message method...")
            
            # Human thinking time
            think_time = random.uniform(*self.human_delays['think_time'])
            logger.info(f"🧠 Human thinking time: {think_time:.1f}s")
            await asyncio.sleep(think_time)
            
            # Start typing with human behavior
            async with channel.typing():
                typing_pattern = await self.human_type_simulation(f"/imagine {self.prompt}")
                
                total_typing_time = 0
                for i in range(0, len(typing_pattern), 2):
                    if i + 1 < len(typing_pattern):
                        delay = typing_pattern[i + 1]
                        total_typing_time += delay
                        await asyncio.sleep(delay)
                
                logger.info(f"⌨️ Typed command over {total_typing_time:.2f}s")
                
                # Final pause before sending
                final_pause = random.uniform(0.5, 1.5)
                await asyncio.sleep(final_pause)
            
            # Send the message
            message = await channel.send(f"/imagine {self.prompt}")
            logger.info(f"✅ STEALTH message sent: {message.content}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error in stealth message method: {e}")
            return False
    
    async def find_best_target_channel(self):
        """Enhanced channel detection (hybrid approach)"""
        logger.info("🎯 Scanning for optimal target channels...")
        
        available_options = []
        
        for guild in self.bot.guilds:
            logger.info(f"📡 Scanning server: {guild.name} (ID: {guild.id})")
            
            # Enhanced Midjourney server detection
            if guild.id == 662267976984297473:
                logger.info("🎨 Found Midjourney server!")
                # More channels to try (from both versions)
                midjourney_channels = [
                    (1008571045445382216, "newbies-109"),
                    (989268300473192551, "newbies-108"),
                    (1008571733043462154, "newbies-110"),
                    (1033144674709467156, "newbies-111"),
                    (1033144740417437716, "newbies-112"),
                    (1008571878793289808, "general-1"),
                    (1008571936079798282, "general-2"),
                    (662267976984297473, "general"),
                ]
                
                for channel_id, channel_name in midjourney_channels:
                    channel = guild.get_channel(channel_id)
                    if channel:
                        permissions = channel.permissions_for(guild.me)
                        if permissions.send_messages:
                            available_options.append({
                                'guild': guild,
                                'channel': channel,
                                'priority': 10,
                                'type': 'midjourney_official'
                            })
                            logger.info(f"✅ Midjourney channel available: {channel_name}")
                        else:
                            logger.info(f"❌ No permission for {channel_name}")
            
            else:
                # Personal servers
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        priority = 5 if 'general' in channel.name.lower() else 3
                        available_options.append({
                            'guild': guild,
                            'channel': channel,
                            'priority': priority,
                            'type': 'personal_server'
                        })
        
        available_options.sort(key=lambda x: x['priority'], reverse=True)
        
        if not available_options:
            logger.error("❌ No accessible channels found!")
            return None
        
        best_option = available_options[0]
        logger.info(f"🎯 Selected target: {best_option['guild'].name}#{best_option['channel'].name}")
        logger.info(f"🎭 Strategy: {best_option['type']}")
        
        return best_option
    
    async def execute_ultimate_mission(self):
        """Execute the ULTIMATE HYBRID mission"""
        try:
            logger.info("🚀 Initiating ULTIMATE HYBRID MISSION...")
            
            target = await self.find_best_target_channel()
            if not target:
                logger.error("❌ No suitable channels found")
                return False
            
            guild = target['guild']
            channel = target['channel']
            strategy_type = target['type']
            
            logger.info(f"✅ Target acquired: {guild.name}#{channel.name}")
            
            # Context for personal servers
            if strategy_type == 'personal_server':
                await channel.send("🚀 ULTIMATE HYBRID BOT - Testing advanced Midjourney methods...")
                await asyncio.sleep(random.uniform(2, 4))
            
            # Human behavior analysis
            logger.info("👀 Analyzing recent activity (human behavior)...")
            recent_count = 0
            async for message in channel.history(limit=5):
                recent_count += 1
                logger.info(f"📝 Recent: {message.author.name}: {message.content[:50]}...")
            
            await asyncio.sleep(random.uniform(2, 5))
            
            # ULTIMATE APPROACH: Try BOTH methods
            logger.info("🎯 Executing ULTIMATE HYBRID METHODS...")
            
            methods = [
                ("EXPERT API Command", self.send_expert_api_command),
                ("ULTRA STEALTH Message", self.send_stealth_message_command)
            ]
            
            for method_name, method_func in methods:
                logger.info(f"🔄 Trying {method_name}...")
                
                if method_name == "EXPERT API Command":
                    success = await method_func(channel, self.prompt)
                else:
                    success = await method_func(channel)
                
                if success:
                    logger.info(f"🎉 SUCCESS! {method_name} executed!")
                    
                    # Post-command monitoring
                    post_wait = random.uniform(*self.human_delays['post_command_wait'])
                    logger.info(f"⏳ Post-command monitoring: {post_wait:.1f}s")
                    await asyncio.sleep(post_wait)
                    
                    # Check for Midjourney response
                    if strategy_type == 'midjourney_official':
                        async for msg in channel.history(limit=15):
                            if msg.author.name == "Midjourney Bot":
                                if any(word in msg.content.lower() for word in ['processing', '%', 'queued']):
                                    logger.info("🎉 MIDJOURNEY BOT RESPONDED!")
                                    logger.info(f"📋 Response: {msg.content[:100]}...")
                                    return True
                    
                    logger.info("✅ Command executed successfully!")
                    return True
                else:
                    logger.warning(f"⚠️ {method_name} failed, trying next method...")
                    await asyncio.sleep(random.uniform(2, 4))
            
            logger.error("❌ All methods failed")
            return False
            
        except Exception as e:
            logger.error(f"❌ Ultimate mission failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def run_mission(self):
        """Execute the complete ultimate mission"""
        token = os.getenv('DISCORD_BOT_TOKEN')
        if not token:
            logger.error("❌ DISCORD_BOT_TOKEN not found in environment")
            return False
        
        try:
            logger.info("🚀 Launching ULTIMATE HYBRID MISSION...")
            await self.bot.start(token)
        except Exception as e:
            logger.error(f"❌ Mission failed: {e}")
            return False

async def main():
    """Main entry point for ULTIMATE HYBRID bot"""
    logger.info("🚀 ULTIMATE HYBRID DISCORD BOT - MAXIMUM POWER")
    logger.info(f"📅 Mission time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if os.getenv('GITHUB_ACTIONS'):
        logger.info("☁️ Operating in GitHub Actions environment")
    
    ultimate_bot = UltimateHybridBot()
    success = await ultimate_bot.run_mission()
    
    if success:
        logger.info("✅ ULTIMATE MISSION ACCOMPLISHED!")
        sys.exit(0)
    else:
        logger.error("❌ ULTIMATE MISSION FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
