from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import sys

def setup_termux_environment():
    """Setup Termux environment for headless browser"""
    os.system("pkg update && pkg upgrade -y")
    os.system("pkg install python chromium -y")
    os.system("pip install selenium")
    
def init_driver():
    """Initialize Chrome driver with Termux-specific options"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 10; SM-G960F)")
    options.add_argument("--window-size=1920,1080")
    
    # Path to Chromium in Termux
    options.binary_location = "/data/data/com.termux/files/usr/bin/chromium"
    
    return webdriver.Chrome(options=options)

def ban_instagram_accounts(accounts_to_ban):
    """Ban Instagram accounts using Selenium"""
    try:
        driver = init_driver()
        driver.get("https://www.instagram.com/accounts/login/")
        
        # Login credentials
        username = os.getenv("INSTAGRAM_USER")
        password = os.getenv("INSTAGRAM_PASS")
        
        if not username or not password:
            print("Error: Missing Instagram credentials")
            return
        
        # Login process
        driver.find_element("name", "username").send_keys(username)
        driver.find_element("name", "password").send_keys(password)
        driver.find_element("xpath", "//button[@type='submit']").click()
        time.sleep(5)
        
        # Ban accounts
        results = []
        for account in accounts_to_ban:
            try:
                driver.get(f"https://www.instagram.com/{account}/")
                time.sleep(2)
                
                # Handle follow button
                try:
                    driver.find_element("xpath", "//button[contains(text(), 'Following')]").click()
                    time.sleep(1)
                except:
                    pass
                
                # Block account
                driver.find_element("xpath", "//button[contains(text(), 'Block') or contains(text(), 'Block user')]").click()
                time.sleep(1)
                results.append(f"Successfully banned {account}")
            except Exception as e:
                results.append(f"Failed to ban {account}: {str(e)}")
        
        driver.quit()
        return results
        
    except Exception as e:
        print(f"Script error: {str(e)}")
        return [f"Error: {str(e)}"]

def main():
    # Setup Termux environment if needed
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        setup_termux_environment()
        print("Termux environment ready!")
        return
    
    # Get target accounts
    accounts_to_ban = ["account1", "account2"]  # Replace with actual accounts
    results = ban_instagram_accounts(accounts_to_ban)
    
    # Print results
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
