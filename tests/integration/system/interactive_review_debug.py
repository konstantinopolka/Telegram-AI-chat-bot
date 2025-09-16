#!/usr/bin/env python3
"""
Interactive Single Review Debug Script
=====================================
Interactive version of the single review debugger with user prompts.
"""

import asyncio
import json
import os
import re
from pathlib import Path
import sys
from datetime import datetime

# Add src to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from test_single_review_debug import SingleReviewDebugger


class InteractiveReviewDebugger:
    """Interactive wrapper for SingleReviewDebugger with user prompts."""
    
    def __init__(self):
        self.debugger = None
        self.selected_url = None
        self.selected_mode = None
    
    def _show_banner(self):
        """Show interactive debug banner."""
        print("🔍 Interactive Single Review Debug Script")
        print("=" * 50)
        print("This tool helps debug single review processing step by step.")
        print("You can select from recent URLs or provide a custom one.")
        print()
    
    def _get_recent_urls(self, limit=10):
        """Get recent URLs from generated_jsons."""
        json_files = [
            "platypus_all_issue_urls.json",
            "platypus_review_links.json"
        ]
        
        available_urls = []
        base_path = Path(__file__).parent.parent.parent.parent / "generated_jsons"
        
        for file in json_files:
            filepath = base_path / file
            if filepath.exists():
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            available_urls.extend(data)
                except Exception as e:
                    print(f"⚠️  Error reading {file}: {e}")
        
        # Remove duplicates and get most recent
        unique_urls = list(dict.fromkeys(available_urls))  # Preserves order
        return unique_urls[-limit:] if len(unique_urls) > limit else unique_urls
    
    def _get_review_url(self):
        """Interactive URL selection."""
        print("🎯 Select Review to Debug:")
        print("1. Default review (issue-178)")
        print("2. Choose from recent URLs")
        print("3. Enter custom URL")
        print()
        
        while True:
            choice = input("Select option (1/2/3): ").strip()
            
            if choice == "1":
                self.selected_url = "https://platypus1917.org/category/pr/issue-178/"
                print(f"✅ Selected: {self.selected_url}")
                break
            
            elif choice == "2":
                recent_urls = self._get_recent_urls()
                if not recent_urls:
                    print("❌ No recent URLs found. Using default.")
                    self.selected_url = "https://platypus1917.org/category/pr/issue-178/"
                    break
                
                print("\n📋 Recent URLs:")
                for i, url in enumerate(recent_urls, 1):
                    # Extract issue number for display
                    match = re.search(r'issue-(\d+)', url)
                    issue_id = match.group(1) if match else "unknown"
                    print(f"   {i}. Issue {issue_id}: {url}")
                
                while True:
                    url_choice = input(f"\nSelect number (1-{len(recent_urls)}): ").strip()
                    if url_choice.isdigit() and 1 <= int(url_choice) <= len(recent_urls):
                        self.selected_url = recent_urls[int(url_choice) - 1]
                        print(f"✅ Selected: {self.selected_url}")
                        break
                    else:
                        print("❌ Invalid selection. Please try again.")
                break
            
            elif choice == "3":
                while True:
                    custom_url = input("Enter review URL: ").strip()
                    if custom_url and "platypus1917.org" in custom_url:
                        self.selected_url = custom_url
                        print(f"✅ Selected: {self.selected_url}")
                        break
                    else:
                        print("❌ Please enter a valid platypus1917.org review URL.")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    def _get_debug_mode(self):
        """Interactive mode selection."""
        print("\n🔧 Select Debugging Mode:")
        print("1. Full workflow (complete processing like production)")
        print("2. Step-by-step (detailed debugging with pauses)")
        print()
        
        while True:
            choice = input("Select mode (1/2): ").strip()
            
            if choice == "1":
                self.selected_mode = "full"
                print("✅ Selected: Full workflow mode")
                break
            elif choice == "2":
                self.selected_mode = "step"
                print("✅ Selected: Step-by-step mode")
                break
            else:
                print("❌ Invalid choice. Please enter 1 or 2.")
    
    def _show_setup_summary(self):
        """Show selected configuration before starting."""
        print(f"\n🔧 Setting up components for review: {self.selected_url}")
        print("   📡 Using real Telegraph API")
        
        # Initialize debugger with selected URL
        self.debugger = SingleReviewDebugger(self.selected_url)
        
        print("✅ Component setup complete")
    
    async def _run_debug_session(self):
        """Run the selected debugging mode."""
        if self.selected_mode == "full":
            print(f"\n🚀 Running Full Workflow Debug...")
            results = await self.debugger.debug_full_workflow()
        else:
            print(f"\n🔍 Running Step-by-step Debug...")
            print("(Press Enter after each step to continue)")
            results = await self.debugger.debug_step_by_step()
        
        return results
    
    def _show_completion_summary(self, results):
        """Show completion summary."""
        print("\n" + "=" * 50)
        print("✅ Debug session complete!")
        if results and hasattr(results, 'debug_info') and results.debug_info:
            debug_info = results.debug_info
            print(f"🔍 [DEBUG POINT] Review: {debug_info.get('review_url', 'N/A')}")
            print(f"📊 Articles found: {debug_info.get('articles_found', 0)}")
            print(f"📊 Articles processed: {debug_info.get('articles_processed', 0)}")
            print(f"⏱️  Processing time: {debug_info.get('processing_time', 'N/A')}")
        
        # Show results location
        results_file = Path(__file__).parent.parent.parent.parent / "tests" / "single_review_debug_results.json"
        if results_file.exists():
            print(f"💾 Results saved to: {results_file}")
    
    async def run(self):
        """Run interactive debugging session."""
        self._show_banner()
        self._get_review_url()
        self._get_debug_mode()
        self._show_setup_summary()
        
        try:
            results = await self._run_debug_session()
            self._show_completion_summary(results)
            return results
        except Exception as e:
            print(f"❌ Debug session failed: {e}")
            import traceback
            traceback.print_exc()
            return None


async def main():
    """Main entry point."""
    debugger = InteractiveReviewDebugger()
    await debugger.run()


if __name__ == "__main__":
    asyncio.run(main())
