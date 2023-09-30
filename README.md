# Extensions
On top of the basic functionality, the proxy includes the following features:
## Image Substitution
Performs image substitution if the second argument is set to 1. For all the requested images, the proxy substitutes the requested image with the image with URL http://ocna0.d2.comp.nus.edu.sg:50000/change.jpg
## Attacker
Proxy should run in the attacker mode if the third argument is set to 1. For any http request, it will reply with an HTML page with the string “You are being attacked”.

# Configuration of Firefox
You should use Firefox version 92.0 [URL](https://www.mozilla.org/en-US/firefox/92.0/releasenotes/).
## Proxy Setup
To configure your browser for the proxy server, follow the below steps:
1. Open Settings
2. Search “Network Settings”
3. Check Manual Proxy Configuration. Enter the IP address and (listening) port number of
your proxy server in HTTPS Proxy. For example, if you run proxy locally, put
“localhost” as IP address.
4. (Optional) If the setup does not work, try to check “Proxy DNS when using SOCKS
v5”.
Disabling Caching
To properly test your proxy’s performance such as fetching speed, you need to disable caching. Here are the steps:
1. Enter about:config at the first page
2. Press the “Accept the Risk and Continue” button.
3. Search browser.cache.disk.enable and browser.cache.memory.enable, then make them
False.
To erase currently saved cookies and caches,
1. Open Settings
2. Search browser.cache.disk.enable
3. Push the “Clear Data” button and clear.
Flexibility of Default HTTP Version
To change the default HTTP version, follow the steps:
1. Enter about:config at the first page
2. Press the “Accept the Risk and Continue” button.
3. Search network.http.version and network.http.proxy.version, then type HTTP version either
1.0 or 1.1.

# Running the proxy
The only file needed is proxy.py
To run this proxy, enter the following command in your terminal:

`python3 proxy.py <port> <image-flag> <attack-flag>`
