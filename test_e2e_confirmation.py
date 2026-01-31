
import time
from playwright.sync_api import sync_playwright

def run_simulation():
    print("Starting End-to-End Simulation: User Payment + Admin Confirmation")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Headless=False so you can watch!
        
        # --- Context 1: The USER ---
        print("\n[USER] Opening Website...")
        user_context = browser.new_context(viewport={"width": 600, "height": 800})
        user_page = user_context.new_page()
        
        # User goes to payment page (simulating they hit the quota)
        user_page.goto("http://localhost:8000/payment.html")
        print("[USER] I am on the Payment Page. Waiting for payment confirmation...")
        
        # Check current URL
        print(f"[USER] Current URL: {user_page.url}")
        
        # --- Context 2: The ADMIN (You) ---
        print("\n[ADMIN] Opening Trigger Dashboard...")
        admin_context = browser.new_context(viewport={"width": 400, "height": 600})
        admin_page = admin_context.new_page()
        admin_page.goto("http://localhost:5000")
        
        print("[ADMIN] I see the dashboard. Simulating 'Payment Received'...")
        time.sleep(2) # Wait a bit for dramatic effect
        
        # Admin clicks "Success"
        print("[ADMIN] Clicking 'Payment Success' button...")
        admin_page.click("button:has-text('✅ Payment Received')")
        
        # --- Validation ---
        print("\n[SYSTEM] Checking if User page reacts...")
        
        # Wait for User Page to redirect
        try:
            user_page.wait_for_url("**/payment_success.html*", timeout=10000)
            print("[SUCCESS] User was automatically redirected to Success Page!")
            print(f"[USER] New URL: {user_page.url}")
            
            if user_page.is_visible(".confetti"):
                print("[USER] I see confetti animation!")
                
        except Exception as e:
            print(f"[FAIL] User page did not redirect. Error: {e}")
            
        print("\nSimulation Finished. Keeping browser open for 5 seconds...")
        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    try:
        run_simulation()
    except Exception as e:
        print(f"Script Error: {e}")
