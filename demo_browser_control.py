
import time
from playwright.sync_api import sync_playwright

def demo_browser_control():
    print("Starting Browser Control Demo...")
    
    with sync_playwright() as p:
        # Launch visible browser
        print("Launching Chrome...")
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context()
        page = context.new_page()
        
        # Navigate
        print("Navigating to Homepage...")
        page.goto("http://localhost:8000/index.html")
        
        # Demonstrate control: Highlight elements
        print("Highlighting Hero Section...")
        heading = page.locator("h1")
        heading.evaluate("element => element.style.border = '5px solid red'")
        heading.evaluate("element => element.style.backgroundColor = 'yellow'")
        
        time.sleep(2)
        
        print("Clicking 'Create Analysis'...")
        page.click("text=创建分析")
        
        print("Waiting for page load...")
        page.wait_for_url("**/create-analysis.html")
        
        print("Taking a screenshot...")
        page.screenshot(path="demo_screenshot.png")
        
        print("Browser Control Test Passed!")
        print("Closing in 5 seconds...")
        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    demo_browser_control()
