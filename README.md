# 💥 BARON v5.2 - Automated XSS Checker

**BARON v5.2** (implemented in **`algeria.py`**) is a dedicated, automated Cross-Site Scripting (XSS) vulnerability checker that utilizes **Selenium WebDriver** to actively test web application parameters. 

By executing payloads in a real, headless browser environment, it is highly effective at detecting reflected XSS vulnerabilities, including those that require user interaction (like clicking a link or a button).

---

### **1. 🎯 Features**

* **Active Browser Testing:** Uses **headless Chrome** (via Selenium) to execute payloads and confirm XSS by detecting live JavaScript `alert()`, `confirm()`, or `prompt()` pop-ups.
* **Comprehensive Encoding:** Automatically generates and tests multiple encoded variations (URL, Double/Triple URL, Hex/HTML Entity, Mixed Case) to bypass common filters.
* **Interaction Emulation:** Attempts to click interactive elements (links with "CLICK" or submit buttons) if the payload requires it.
* **File Input Support:** Can load a custom list of payloads from a file or use its integrated defaults.
* **Parameterized Testing:** Automatically identifies and iterates through every query parameter found in the input URL.

---

### **2. 💻 Requirements & Installation**

#### **A. Python Dependencies**

Install the required Python packages using `pip`:

```bash
pip install selenium colorama urllib3
