#!/bin/zsh
# Builds the RaioX Mac menu-bar application bundle.
set -euo pipefail
cd "$(dirname "$0")"

export DEVELOPER_DIR="${DEVELOPER_DIR:-$(xcode-select -p)}"
export SDKROOT="${SDKROOT:-$(xcrun --sdk macosx --show-sdk-path)}"

swift build -c release
APP="build/RaioX Mac.app"
EXECUTABLE="RaioXMac"
rm -rf "$APP"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
cp ".build/release/$EXECUTABLE" "$APP/Contents/MacOS/$EXECUTABLE"
cat > "$APP/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>CFBundleName</key><string>RaioX Mac</string>
  <key>CFBundleDisplayName</key><string>RaioX Mac</string>
  <key>CFBundleIdentifier</key><string>us.lucianocorrea.raioxmac</string>
  <key>CFBundleExecutable</key><string>RaioXMac</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleShortVersionString</key><string>0.1</string>
  <key>CFBundleVersion</key><string>1</string>
  <key>LSMinimumSystemVersion</key><string>15.0</string>
  <key>LSUIElement</key><true/>
  <key>NSDesktopFolderUsageDescription</key><string>Checks for a project marker to group developer processes.</string>
  <key>NSDocumentsFolderUsageDescription</key><string>Checks for a project marker to group developer processes.</string>
  <key>NSDownloadsFolderUsageDescription</key><string>Checks for a project marker to group developer processes.</string>
</dict></plist>
PLIST
codesign --force --sign - "$APP"
echo "Built $PWD/$APP"
