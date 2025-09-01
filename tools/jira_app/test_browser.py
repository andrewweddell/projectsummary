#!/usr/bin/env python3
"""
Simple browser automation script to test the Jira app sync functionality
and capture any warnings that appear.
"""

import time
import json
from selenium import webdriver
from selenium import __version__ as selenium_version
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_sync_warnings():
    """Test the sync functionality and capture any warnings."""
    print("🚀 Testing Jira app sync functionality for warnings...")
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Enable logging
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--log-level=0")
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    driver = None
    try:
        # Initialize the driver
        print(f"Using Selenium version: {selenium_version}")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Navigate to the app
        print("📱 Navigating to http://localhost:5001...")
        driver.get("http://localhost:5001")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        print("✅ Page loaded successfully")
        
        # Take initial screenshot
        driver.save_screenshot("/tmp/jira_app_initial.png")
        print("📸 Initial screenshot saved to /tmp/jira_app_initial.png")
        
        # Look for sync button using different methods
        sync_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Sync')]")
        
        if not sync_buttons:
            # Try finding by partial text match
            sync_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'from Jira')]")
            
        if not sync_buttons:
            # Try finding by onclick attribute
            sync_buttons = driver.find_elements(By.XPATH, "//button[@onclick='syncTickets()']")
            
        if not sync_buttons:
            # Try finding in sidebar
            sync_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'Sync Tickets')]")
            
        if not sync_buttons:
            print("❌ No sync buttons found on page")
            print("🔍 Let's examine the page content...")
            
            # Print page source snippet for debugging
            page_source = driver.page_source
            if 'syncTickets' in page_source:
                print("✅ Found 'syncTickets' function in page")
            else:
                print("❌ No 'syncTickets' function found")
                
            # Find all buttons on page
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            print(f"🔍 Found {len(all_buttons)} buttons on page:")
            for i, btn in enumerate(all_buttons[:5]):  # Show first 5 buttons
                try:
                    print(f"  {i+1}. Text: '{btn.text}', Class: '{btn.get_attribute('class')}'")
                except:
                    print(f"  {i+1}. Unable to read button properties")
            return
            
        sync_button = sync_buttons[0]
        print(f"🔍 Found sync button: {sync_button.text}")
        
        # Clear console logs
        driver.get_log('browser')
        
        # Click the sync button
        print("🖱️  Clicking sync button...")
        driver.execute_script("arguments[0].click();", sync_button)
        
        # Wait for confirmation dialog and accept it
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(f"⚠️  Alert detected: {alert.text}")
            alert.accept()
            print("✅ Alert accepted")
        except:
            print("ℹ️  No alert detected")
        
        # Wait for progress modal to appear
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "progressModal"))
            )
            print("📊 Progress modal appeared")
            
            # Take screenshot of progress modal
            driver.save_screenshot("/tmp/jira_app_progress.png")
            print("📸 Progress modal screenshot saved to /tmp/jira_app_progress.png")
            
        except:
            print("⚠️  Progress modal not detected")
        
        # Monitor for warnings in console logs and on page
        print("👁️  Monitoring for warnings...")
        
        max_wait = 30  # Wait up to 30 seconds
        start_time = time.time()
        warnings_found = []
        
        while time.time() - start_time < max_wait:
            # Check browser console logs
            logs = driver.get_log('browser')
            for log in logs:
                if 'warning' in log['message'].lower() or log['level'] == 'WARNING':
                    warning_msg = f"Console Warning: {log['level']} - {log['message']}"
                    if warning_msg not in warnings_found:
                        warnings_found.append(warning_msg)
                        print(f"⚠️  {warning_msg}")
            
            # Check for alert warnings on page
            alert_warnings = driver.find_elements(By.CSS_SELECTOR, ".alert-warning")
            for warning in alert_warnings:
                if warning.is_displayed():
                    warning_text = warning.text.strip()
                    if warning_text and warning_text not in warnings_found:
                        warnings_found.append(f"UI Warning: {warning_text}")
                        print(f"⚠️  UI Warning: {warning_text}")
            
            # Check progress modal for warnings
            try:
                progress_details = driver.find_element(By.ID, "progressDetailsContent")
                if progress_details.is_displayed():
                    details_text = progress_details.text
                    if 'warning' in details_text.lower() or 'warn' in details_text.lower():
                        if details_text not in warnings_found:
                            warnings_found.append(f"Progress Warning: {details_text}")
                            print(f"⚠️  Progress Warning: {details_text}")
            except:
                pass
            
            # Check if operation completed
            try:
                close_btn = driver.find_element(By.ID, "progressCloseBtn")
                if close_btn.is_displayed():
                    print("✅ Operation completed")
                    break
            except:
                pass
                
            time.sleep(1)
        
        # Take final screenshot
        driver.save_screenshot("/tmp/jira_app_final.png")
        print("📸 Final screenshot saved to /tmp/jira_app_final.png")
        
        # Print summary
        print("\n📋 SUMMARY:")
        print("="*50)
        if warnings_found:
            print(f"⚠️  Found {len(warnings_found)} warning(s):")
            for i, warning in enumerate(warnings_found, 1):
                print(f"  {i}. {warning}")
        else:
            print("✅ No warnings detected during sync process")
        
        return warnings_found
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return []
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    warnings = test_sync_warnings()
    if warnings:
        print(f"\n🎯 RESULT: {len(warnings)} warning(s) found during sync")
        exit(1)
    else:
        print("\n🎯 RESULT: No warnings detected")
        exit(0)