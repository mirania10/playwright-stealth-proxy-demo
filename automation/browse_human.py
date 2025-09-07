#!/usr/bin/env python3
"""
Human-like browsing automation script using Playwright with stealth capabilities.
Designed for production use with comprehensive proxy support and anti-detection.

Author: Playwright Stealth Demo
Date: September 2025
"""

import os
import sys
import time
import random
import logging
import json
from datetime import datetime
from pathlib import Path
import asyncio
from typing import Optional, Dict, Any

# Core Playwright imports
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, ProxySettings
from playwright_stealth import stealth_async

# Additional stealth and utilities
from fake_useragent import UserAgent
import numpy as np

# Setup logging
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f'browse_human_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class HumanBrowserSimulator:
    """Production-ready human browsing simulator with comprehensive stealth capabilities."""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.ua = UserAgent()
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables with sensible defaults."""
        return {
            'target_url': os.getenv('TARGET_URL', 'https://creditBPO.com'),
            'duration_minutes': int(os.getenv('DURATION_MINUTES', '5')),
            'proxy_host': os.getenv('PROXY_HOST'),
            'proxy_port': os.getenv('PROXY_PORT'),
            'proxy_username': os.getenv('PROXY_USERNAME'),
            'proxy_password': os.getenv('PROXY_PASSWORD'),
            'timezone': os.getenv('TIMEZONE', 'America/New_York'),
            'user_agent': os.getenv('USER_AGENT', self.ua.random),
            'viewport_width': int(os.getenv('VIEWPORT_WIDTH', '1920')),
            'viewport_height': int(os.getenv('VIEWPORT_HEIGHT', '1080')),
            'locale': os.getenv('LOCALE', 'en-US'),
        }
    
    def _create_proxy_settings(self) -> Optional[ProxySettings]:
        """Create proxy settings if proxy credentials are provided."""
        if not all([self.config['proxy_host'], self.config['proxy_port']]):
            logger.info("No proxy configuration found, proceeding without proxy")
            return None
            
        proxy_settings = {
            'server': f"http://{self.config['proxy_host']}:{self.config['proxy_port']}"
        }
        
        if self.config['proxy_username'] and self.config['proxy_password']:
            proxy_settings.update({
                'username': self.config['proxy_username'],
                'password': self.config['proxy_password']
            })
            
        logger.info(f"Using proxy: {self.config['proxy_host']}:{self.config['proxy_port']}")
        return proxy_settings
    
    async def _setup_browser(self, playwright) -> None:
        """Setup browser with stealth configuration and anti-detection measures."""
        proxy_settings = self._create_proxy_settings()
        
        # Launch browser with comprehensive stealth settings
        browser_args = [
            '--no-sandbox',
            '--disable-blink-features=AutomationControlled',
            '--disable-features=VizDisplayCompositor',
            '--disable-web-security',
            '--disable-features=TranslateUI',
            '--disable-ipc-flooding-protection',
            '--disable-renderer-backgrounding',
            '--disable-backgrounding-occluded-windows',
            '--disable-client-side-phishing-detection',
            '--disable-component-extensions-with-background-pages',
            '--disable-default-apps',
            '--disable-dev-shm-usage',
            '--disable-extensions',
            '--disable-features=TranslateUI',
            '--disable-hang-monitor',
            '--disable-sync',
            '--metrics-recording-only',
            '--no-first-run',
            '--safebrowsing-disable-auto-update',
            '--enable-automation',
            '--password-store=basic',
            '--use-mock-keychain'
        ]
        
        self.browser = await playwright.chromium.launch(
            headless=False,  # Non-headless for human simulation
            args=browser_args,
            proxy=proxy_settings
        )
        
        # Create context with human-like settings
        context_options = {
            'viewport': {
                'width': self.config['viewport_width'],
                'height': self.config['viewport_height']
            },
            'user_agent': self.config['user_agent'],
            'locale': self.config['locale'],
            'timezone_id': self.config['timezone'],
            'permissions': ['geolocation', 'notifications'],
            'color_scheme': 'light',
            'extra_http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0'
            }
        }
        
        self.context = await self.browser.new_context(**context_options)
        
        # Add additional stealth scripts
        await self.context.add_init_script("""
            // Override the `plugins` property to use a custom getter.
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // Override the `languages` property to use a custom getter.
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            // Override the `webdriver` property to remove it.
            delete navigator.__proto__.webdriver;
        """)
        
        self.page = await self.context.new_page()
        
        # Apply playwright-stealth
        await stealth_async(self.page)
        
        logger.info("Browser setup completed with stealth configuration")
    
    async def _human_delay(self, min_seconds: float = 0.5, max_seconds: float = 3.0) -> None:
        """Simulate human-like delays with realistic timing patterns."""
        # Use a more realistic delay distribution
        delay = np.random.gamma(2, 0.5) + min_seconds
        delay = min(delay, max_seconds)
        await asyncio.sleep(delay)
    
    async def _human_scroll(self) -> None:
        """Simulate human-like scrolling behavior."""
        # Random scroll patterns
        scroll_patterns = [
            {'direction': 'down', 'amount': random.randint(200, 800)},
            {'direction': 'up', 'amount': random.randint(100, 400)},
            {'direction': 'down', 'amount': random.randint(300, 600)}
        ]
        
        pattern = random.choice(scroll_patterns)
        
        if pattern['direction'] == 'down':
            await self.page.evaluate(f'window.scrollBy(0, {pattern["amount"]})')
        else:
            await self.page.evaluate(f'window.scrollBy(0, -{pattern["amount"]})')
        
        await self._human_delay(0.8, 2.5)
    
    async def _simulate_mouse_movement(self) -> None:
        """Simulate realistic mouse movements and interactions."""
        viewport = self.page.viewport_size
        
        # Generate random coordinates within viewport
        x = random.randint(100, viewport['width'] - 100)
        y = random.randint(100, viewport['height'] - 100)
        
        # Move mouse with human-like curve
        await self.page.mouse.move(x, y)
        await self._human_delay(0.3, 1.0)
        
        # Occasionally click on safe areas
        if random.random() < 0.3:
            await self.page.mouse.click(x, y)
            await self._human_delay(0.5, 1.5)
    
    async def _random_interactions(self) -> None:
        """Perform various random human-like interactions."""
        interactions = [
            self._human_scroll,
            self._simulate_mouse_movement,
            lambda: self._human_delay(1.0, 4.0)  # Just pause and observe
        ]
        
        # Choose 1-3 random interactions
        num_interactions = random.randint(1, 3)
        chosen_interactions = random.sample(interactions, num_interactions)
        
        for interaction in chosen_interactions:
            try:
                await interaction()
            except Exception as e:
                logger.warning(f"Interaction failed: {e}")
    
    async def browse_like_human(self) -> None:
        """Main browsing simulation with human-like behavior patterns."""
        try:
            logger.info(f"Starting human browsing simulation for {self.config['duration_minutes']} minutes")
            logger.info(f"Target URL: {self.config['target_url']}")
            
            # Navigate to target URL
            await self.page.goto(self.config['target_url'], wait_until='networkidle')
            await self._human_delay(2.0, 5.0)
            
            # Log successful navigation
            logger.info(f"Successfully navigated to {self.config['target_url']}")
            
            # Calculate end time
            start_time = time.time()
            end_time = start_time + (self.config['duration_minutes'] * 60)
            
            interaction_count = 0
            
            # Main browsing loop
            while time.time() < end_time:
                try:
                    await self._random_interactions()
                    interaction_count += 1
                    
                    # Log progress every 10 interactions
                    if interaction_count % 10 == 0:
                        elapsed = (time.time() - start_time) / 60
                        remaining = (end_time - time.time()) / 60
                        logger.info(f"Progress: {elapsed:.1f}min elapsed, {remaining:.1f}min remaining, {interaction_count} interactions")
                    
                    # Longer pause occasionally to simulate reading
                    if random.random() < 0.2:
                        await self._human_delay(5.0, 15.0)
                        
                except Exception as e:
                    logger.error(f"Error during interaction {interaction_count}: {e}")
                    await self._human_delay(1.0, 3.0)
            
            logger.info(f"Browsing simulation completed. Total interactions: {interaction_count}")
            
        except Exception as e:
            logger.error(f"Critical error during browsing simulation: {e}")
            raise
    
    async def cleanup(self) -> None:
        """Clean up browser resources."""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            logger.info("Browser cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    async def run(self) -> None:
        """Main execution method."""
        async with async_playwright() as playwright:
            try:
                await self._setup_browser(playwright)
                await self.browse_like_human()
            finally:
                await self.cleanup()

async def main():
    """Main entry point."""
    simulator = HumanBrowserSimulator()
    
    try:
        await simulator.run()
        logger.info("Human browsing simulation completed successfully")
    except KeyboardInterrupt:
        logger.info("Simulation interrupted by user")
    except Exception as e:
        logger.error(f"Simulation failed: {e}")
        sys.exit(1)
    finally:
        logger.info("Exiting human browsing simulator")

if __name__ == "__main__":
    asyncio.run(main())
