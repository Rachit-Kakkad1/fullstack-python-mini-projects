import qrcode

# Ask user for WiFi details
ssid = input("📶 Enter WiFi Name (SSID): ").strip()
password = input("🔐 Enter WiFi Password (leave blank if open network): ").strip()

# Decide security type
if password == "":
    security = "nopass"
    wifi_config = f"WIFI:T:{security};S:{ssid};;"
else:
    security = "WPA"
    wifi_config = f"WIFI:T:{security};S:{ssid};P:{password};;"

# Show what’s going into the QR
print("\n📄 QR Content:")
print(wifi_config)

# Generate and save QR code
qr = qrcode.make(wifi_config)
qr.save("wifi_qr.png")
print("✅ WiFi QR Code saved as 'wifi_qr.png'")
qr.show()

print("\n🎉 Done! See you next time!")
print("👋 Bye-bye!")