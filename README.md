# BARON v5.2 - Automated XSS Checker

**BARON v5.2** (implemented in **algeria.py**) is a dedicated, automated Cross-Site Scripting (XSS) vulnerability checker that uses **Selenium WebDriver** to actively test web application parameters. It executes payloads in a real, headless browser environment to detect reflected XSS, including those requiring user interaction.

---

## 1. Features

* Active Browser Testing: Uses headless Chrome to confirm XSS by detecting live JavaScript alerts.
* Comprehensive Encoding: Tests multiple encoded variations (URL, Hex, Mixed Case) to bypass filters.
* Interaction Emulation: Attempts to click interactive elements (links, submit buttons).
* File Input Support: Uses custom payload files or integrated defaults.
* Parameterized Testing: Automatically iterates through every query parameter in the input URL.

---

## 2. Requirements & Installation

### A. Python Dependencies

Install the required Python packages using pip:

`pip install selenium colorama urllib3`

### B. Chrome Driver

The tool requires the Chromium/Chrome web driver (chromedriver).

1. Install Google Chrome or Chromium.
2. Install **chromedriver** (ensure it matches your browser version).
3. **Configuration:** You must verify and update the `CHROME_DRIVER_PATH` variable inside the **algeria.py** script to the correct location for your system.

`# Example in algeria.py: CHROME_DRIVER_PATH = "/usr/bin/chromedriver"`

---

## 3. Detailed Usage Guide

To start the scan, execute the script:

`python algeria.py`

The tool prompts for three inputs:

### Step 1: Enter Base URL
Enter the full URL. **Must contain query parameters** (e.g., `https://target.com/page?id=10&name=`).

### Step 2: Payloads File Name
Provide the path to a custom file, or leave blank to use defaults.

### Step 3: Select Mode
Choose: **(A)ll** (Base + Encoded), **(B)ase Only**, or **(E)ncoded Only**.

### Example Scan Output (Summary)

The tool logs all tests and provides a final summary. Successful XSS detections are confirmed with details:

`[VV] Confirmed XSS (Pop-up Detected): 1`
`[VV] PARAM: id | [Base] (Alert: target.com) -> <script>alert(document.domain)</script>`

---

## 4. Integrated Default Payloads

If no file is provided, the tool uses:

* `<script>alert(document.domain)</script>`
* `"><img src=x onerror=alert(1)>`
* `"><svg onload=alert(1)>`
* `javascript:alert(1)`
* `"></a><a href="javascript:alert(1)">CLICK</a>`
* `<iframe srcdoc='<script>alert(1)</script>'>`

---

## BBA.34000
