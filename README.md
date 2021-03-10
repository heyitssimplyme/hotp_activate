# hotp_activate

A small script to activate Duo's HOTP code

## Steps
1. Register a new device
    -  Select Tablet
    - Select Android
    - Select "I have Duo Mobile installed"
2. Right click the QR code, copy the image url, and then run this program with the QR code url.
    ```sh
    # example
    python main.py "https://api-xxxxxxxx.duosecurity.com/frame/qr?value=....-...."
    ```

3. You'll get your HOTP secret with a counter, which starts from 0.

### Notes:
- You can use a cli tool like `oathtool` to generate the passcode.
    ```sh
    # example
    oathtool --hotp -b 'base32' -c 0
   ```
- You cannot use some managers like 1Password since they do not support HOTP.
- Ensure that the counter is incremented _every time_ you login.
- Other details: SHA1, 6 digits
