// swift-tools-version:6.0
import PackageDescription

let package = Package(
    name: "RaioXMac",
    platforms: [.macOS(.v13)],
    targets: [
        .executableTarget(name: "RaioXMac", path: "Sources/VitalsClone", swiftSettings: [.swiftLanguageMode(.v5)])
    ]
)
