import time
from playwright.sync_api import sync_playwright

print("Connecting to payment page to complete the flow...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # Navigate to payment page
    page.goto("http://localhost:8000/payment.html")
    print("Payment page loaded. Waiting 2 seconds for you to verify...")
    time.sleep(2)
    
    # Click "I have completed payment" button
    print("Clicking 'I have completed payment' button...")
    page.once("dialog", lambda dialog: dialog.accept())
    page.click("button:has-text('我已完成支付')")
    
    # Wait for success page
    print("Waiting for redirect to success page...")
    page.wait_for_url("**/payment_success.html*")
    print("[SUCCESS] Redirected to payment success page!")
    
    # Check confetti
    if page.is_visible(".confetti"):
        print("[SUCCESS] Confetti animation is active!")
    
    print("\nTest completed! Browser will stay open for 10 seconds for you to review...")
    time.sleep(10)
    
    browser.close()
    print("Done!")
