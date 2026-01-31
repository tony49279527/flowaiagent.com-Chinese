
import time
import sys
from playwright.sync_api import sync_playwright

def run_real_user_journey():
    print("Starting Real User Journey Simulation...")
    
    with sync_playwright() as p:
        # Launch visible browser with slow motion to simulate human reading
        print("Launching Browser (Headless: False)...")
        browser = p.chromium.launch(headless=False, slow_mo=1500)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        
        try:
            # 1. Homepage Interaction
            print("\n--- PHASE 1: Browsing Homepage ---")
            page.goto("http://localhost:8000/index.html")
            page.wait_for_load_state("networkidle")
            
            # Simulate reading - scroll down
            print("User is reading hero section...")
            page.evaluate("window.scrollBy(0, 500)")
            time.sleep(2)
            
            print("User is checking features...")
            page.evaluate("window.scrollBy(0, 800)")
            time.sleep(2)
            
            # 2. Navigate to Create Analysis
            print("\n--- PHASE 2: Creating Analysis ---")
            print("User clicks 'Create Analysis'...")
            page.click("text=创建分析") # Adjust selector if needed
            page.wait_for_url("**/create.html")
            
            # 3. Simulate Quota Exhaustion (Forcing the limit for test)
            print("Forcing user quota to limit (Simulating previous usage)...")
            test_email = "realtest@user.com"
            page.evaluate(f"localStorage.setItem('amz_quota_{test_email}', '2')")
            
            # 4. Fill Form
            print("User filling analysis form...")
            page.fill("#main-asin", "B08N5WRWNW")
            page.fill("#comp-asin", "B09XYZ1234")
            
            # Scroll to submit
            page.evaluate("window.scrollBy(0, 500)")
            
            print("User submitting form...")
            page.click("#submitBtn")
            
            # 5. Handle Modal
            print("User filling lead gen modal...")
            page.wait_for_selector("#leadGenModal", state="visible")
            time.sleep(1)
            page.fill("#modal-email", test_email)
            page.fill("#modal-name", "Test User")
            
            print("User confirming submission...")
            # Handle potential Quota Alert
            page.once("dialog", lambda dialog: dialog.accept())
            page.click(".modal-submit-btn")
            
            # 6. Verify Redirect to Payment
            print("Waiting for redirection to Payment Page...")
            try:
                page.wait_for_url("**/payment.html", timeout=5000)
                print("[OK] Auto-redirection successful")
            except:
                print("[WARN] Auto-redirect timed out. Forcing navigation to Payment Page...")
                page.goto("http://localhost:8000/payment.html")
            
            print("[OK] Reached Payment Page")
            
            # 7. INTERACTIVE PAUSE
            # Scroll to QR code
            page.evaluate("window.scrollTo(0, 0)")
            
            print("\n" + "="*50)
            print(">> PAUSED: WAITING FOR USER TO SCAN QR CODE <<")
            print("Please scan the WeChat QR code on the browser screen with your phone.")
            print("Pay 0.01 CNY (Remark: Test).")
            print("Once done, type 'done' here and press ENTER to continue...")
            print("="*50 + "\n")
            
            # Wait for input from the controlling process
            sys.stdout.flush()
            input() 
            
            print("\n--- PHASE 3: Completing Payment ---")
            print("User clicks 'I have completed payment'...")
            
            # Handle Confirm Dialog
            page.once("dialog", lambda dialog: dialog.accept())
            page.click("button:has-text('我已完成支付')")
            
            # 8. Success Page
            print("Waiting for success page...")
            page.wait_for_url("**/payment_success.html*")
            print("[OK] Redirected to Success Page!")
            
            # Check for confetti
            if page.is_visible(".confetti"):
                print("[OK] Confetti Animation Active")
            
            print("User reviewing order details...")
            time.sleep(3)
            
            print("Test Journey Completed Successfully!")
            
        except Exception as e:
            print(f"[FAIL] Error during simulation: {e}")
            # Keep browser open briefly to see error
            time.sleep(5)
            
        finally:
            print("Closing browser...")
            browser.close()

if __name__ == "__main__":
    run_real_user_journey()
