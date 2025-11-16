BARON v5.2 - Automated XSS Checker

BARON v5.2 (implemented in algeria.py) is a dedicated, automated Cross-Site Scripting (XSS) vulnerability checker that utilizes Selenium WebDriver to actively test web application parameters.

By executing payloads in a real, headless browser environment, it is highly effective at detecting reflected XSS vulnerabilities, including those that require user interaction (like clicking a link or a button).

---

1. Features

* Active Browser Testing: Uses headless Chrome (via Selenium) to execute payloads and confirm XSS by detecting live JavaScript alert(), confirm(), or prompt() pop-ups.
* Comprehensive Encoding: Automatically generates and tests multiple encoded variations (URL, Double/Triple URL, Hex/HTML Entity, Mixed Case) to bypass common filters.
* Interaction Emulation: Attempts to click interactive elements (links with "CLICK" or submit buttons) if the payload requires it.
* File Input Support: Can load a custom list of payloads from a file or use its integrated defaults.
* Parameterized Testing: Automatically identifies and iterates through every query parameter found in the input URL.

---

2. Requirements & Installation

A. Python Dependencies

Install the required Python packages using pip:

pip install selenium colorama urllib3

B. Chrome Driver

The tool requires the Chromium/Chrome web driver (chromedriver):

1. Install Google Chrome or Chromium.
2. Install chromedriver: Ensure the chromedriver executable matches your browser version and is accessible on your system path.
3. Update Configuration: You must verify and potentially update the CHROME_DRIVER_PATH variable inside the algeria.py script to the correct location for your system.

# In algeria.py
CHROME_DRIVER_PATH = "/usr/bin/chromedriver" # << UPDATE THIS PATH IF NEEDED

---

3. Detailed Usage Guide

To start the scan, execute the script from your terminal:

python algeria.py

The tool will display its logo and then guide you through three input steps.

Step 1: Enter Base URL
Enter the full URL you want to test. It must contain query parameters for the tool to identify injection points.

* Example Input: https://target.com/page?id=10&name=

Step 2: Payloads File Name
Provide the path to a custom file of XSS payloads, or leave it blank to use the built-in defaults.

* Example Input (Custom): my_payloads.txt
* Example Input (Default): (Just press Enter)

Step 3: Select Mode
Choose how the payloads should be handled and encoded.

Mode | Option | Description
:--- | :--- | :---
A | All (Base + Encoded) | Tests the raw payload and all its encoded variations (recommended for full coverage).
B | Base Only | Tests only the raw payloads as they are defined in the file/defaults.
E | Encoded Only | Tests only the encoded variations, skipping the raw payloads.

Example Scan Output

The tool will display a running log for each parameter and payload combination. Successful XSS detections are highlighted in green.

[i] Using 6 integrated base payloads.
[*] Found 2 parameters: id, name

*** Testing Parameter: id ***
[+] id Test 1/18 (Base): <script>alert(document.domain)... 
[VV] id TEST 1 (Base): POP-UP CONFIRMED (Alert: target.com) -> <script>alert(document.domain)</script>...
[+] id Test 2/18 (URL Encoded): %3cscript%3ealert(document.domain)... 
...
*** Testing Parameter: name ***
[+] name Test 7/18 (Double Encoded): %2522%253cimg%2520src%253d...

--- BARON: Test Summary ---
[*] Testing Mode: A
[*] Total Parameters Tested: 2
[*] Total Tests Run: 36
[VV] Confirmed XSS (Pop-up Detected): 1
----------------------------

Confirmed XSS Payloads:
[VV] PARAM: id | [Base] (Alert: target.com) -> <script>alert(document.domain)</script>

---

4. Integrated Default Payloads

If you choose not to provide a file, BARON uses the following common list of pop-up payloads:

* <script>alert(document.domain)</script>
* "><img src=x onerror=alert(1)>
* "><svg onload=alert(1)>
* javascript:alert(1)
* "></a><a href="javascript:alert(1)">CLICK</a>
* <iframe srcdoc='<script>alert(1)</script>'>

---

5. Screenshot

(Insert your high-quality screenshot of the tool running here.)
