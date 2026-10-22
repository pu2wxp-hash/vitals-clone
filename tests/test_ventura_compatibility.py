from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "Sources" / "VitalsClone"


class VenturaCompatibilityTests(unittest.TestCase):
    def test_package_deployment_target_is_macos_13(self):
        package = (ROOT / "Package.swift").read_text()
        self.assertRegex(package, r"platforms:\s*\[\.macOS\(\.v13\)\]", "Package.swift must target macOS 13")

    def test_app_bundle_declares_ventura_minimum(self):
        build_script = (ROOT / "build-app.sh").read_text()
        self.assertIn("<key>LSMinimumSystemVersion</key><string>13.0</string>", build_script, "The app bundle must declare macOS 13.0")

    def test_monitor_store_uses_legacy_observable_object(self):
        source = (SOURCES / "MonitorStore.swift").read_text()
        self.assertRegex(source, r"final class MonitorStore:\s*ObservableObject", "MonitorStore must use ObservableObject")
        self.assertRegex(source, r"@Published\s+var system\s*=", "UI-observed state must be published")
        self.assertNotIn("import Observation", source, "Observation framework is unavailable on Ventura")
        self.assertNotIn("@Observable", source, "@Observable is unavailable on Ventura")

    def test_swiftui_environment_uses_ventura_compatible_api(self):
        swift_files = list(SOURCES.glob("*.swift"))
        all_source = "\n".join(path.read_text() for path in swift_files)
        self.assertNotIn("@Bindable", all_source, "@Bindable is unavailable on Ventura")
        self.assertNotIn("@Environment(MonitorStore.self)", all_source, "Typed Observable environment is unavailable on Ventura")
        self.assertNotIn(".environment(store)", all_source, "Typed Observable environment injection is unavailable on Ventura")
        self.assertGreaterEqual(all_source.count("@EnvironmentObject var store: MonitorStore"), 13, "All store-consuming views must use EnvironmentObject")

    def test_workflow_artifact_names_mark_macos_13(self):
        workflow = (ROOT / ".github" / "workflows" / "build-macos.yml").read_text()
        self.assertGreaterEqual(workflow.count("RaioX-Mac-macOS13-universal"), 3, "Installer names must identify the macOS 13 build")
        self.assertNotIn("RaioX-Mac-macOS15-universal", workflow, "Workflow must not label the Ventura build as macOS 15")

    def test_readme_states_ventura_requirement(self):
        readme = (ROOT / "README.md").read_text()
        self.assertIn("macOS 13 ou posterior", readme)
        self.assertNotIn("macOS 15 ou posterior", readme)

    def test_app_injects_shared_store_into_both_scenes(self):
        app = (SOURCES / "App.swift").read_text()
        self.assertEqual(app.count(".environmentObject(store)"), 2, "Both app scenes must receive the shared model")
        self.assertIn("@StateObject private var store", app)


if __name__ == "__main__":
    unittest.main()
