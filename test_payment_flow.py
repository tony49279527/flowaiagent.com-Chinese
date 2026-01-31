
import os
import time
from playwright.sync_api import sync_playwright

def run_payment_test():
    print("Starting Payment Flow Test...")
    
    # Create videos directory
    video_dir = os.path.abspath("test_media")
    os.makedirs(video_dir, exist_ok=True)
    
    with sync_playwright() as p:
        # Launch browser (headless=False so user can see it working!)
        # Using slow_mo to make it easier to follow in a video/observation
        print("Launching Browser...")
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        
        # Create context with video recording
        context = browser.new_context(
            record_video_dir=video_dir,
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720}
        )
        
        page = context.new_page()
        
        try:
            # 1. Open Payment Page
            print("Step 1: Navigating to payment page (http://localhost:8000/payment.html)...")
            page.goto("http://localhost:8000/payment.html")
            page.wait_for_load_state("networkidle")
            page.screenshot(path=os.path.join(video_dir, "1_payment_page.png"))
            
            # Check for key elements
            if page.is_visible("text=解锁完整报告"):
                print("[OK] Report preview visible")
            if page.is_visible("text=订单概览"):
                print("[OK] Payment panel visible")
                
            # 2. Switch Payment Methods
            print("Step 2: Switching to Alipay...")
            page.click("#alipayBtn")
            time.sleep(1) # Visual pause
            page.screenshot(path=os.path.join(video_dir, "2_alipay_switched.png"))
            
            # Verify image change (simple check of src)
            img_src = page.get_attribute("#qrImage", "src")
            if "alipay" in img_src:
                print(f"[OK] QR switched to Alipay ({img_src})")
                
            print("Step 3: Switching back to WeChat...")
            page.click("#wechatBtn")
            time.sleep(1)
            page.screenshot(path=os.path.join(video_dir, "3_wechat_switched.png"))
            
            img_src = page.get_attribute("#qrImage", "src")
            if "wechat" in img_src:
                print(f"[OK] QR switched back to WeChat ({img_src})")
            
            # 3. Confirm Payment
            print("Step 4: Clicking 'Payment Completed'...")
            
            # Handle the confirm dialog
            page.once("dialog", lambda dialog: dialog.accept())
            page.click("button:has-text('我已完成支付')")
            
            # 4. Success Page
            print("Step 5: Waiting for success redirection...")
            page.wait_for_url("**/payment_success.html*", timeout=10000)
            print("[OK] Redirected to success page")
            page.screenshot(path=os.path.join(video_dir, "4_success_page.png"))
            
            # Wait for confetti
            time.sleep(2)
            if page.is_visible(".confetti"):
                print("[OK] Confetti animation detected")
                
            print("Test Completed Successfully!")
            print(f"Screenshots and Video saved in: {video_dir}")
            
        except Exception as e:
            print(f"[FAIL] Test Failed: {e}")
            page.screenshot(path=os.path.join(video_dir, "error.png"))
            
        finally:
            # Close context to save video
            context.close()
            browser.close()
            
if __name__ == "__main__":
    run_payment_test()
