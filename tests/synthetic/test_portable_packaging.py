from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


class PortablePackagingTests(unittest.TestCase):
    def _run_installer(self, target: str, destination: Path) -> None:
        subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "install_skills.py"),
                "--target",
                target,
                "--destination",
                str(destination),
            ],
            check=True,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )

    def test_generic_bundle_contains_runnable_engine_and_all_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            bundle = Path(temp) / "bundle"
            self._run_installer("generic", bundle)
            required = (
                bundle / "bin" / "application-pack",
                bundle / "pyproject.toml",
                bundle / "src" / "application_pack" / "cli.py",
                bundle / "schemas" / "run-manifest.schema.json",
                bundle / "BOOTSTRAP.md",
            )
            for path in required:
                self.assertTrue(path.is_file(), path)
            self.assertTrue(os.access(bundle / "bin" / "application-pack", os.X_OK))
            self.assertEqual(
                sorted(path.name for path in (bundle / "skills").iterdir() if path.is_dir()),
                sorted(
                    (
                        "application-package",
                        "career-evidence",
                        "opportunity-auditor",
                        "application-positioner",
                        "resume-author",
                        "speaker-pitch-author",
                        "document-compositor",
                        "artifact-change-controller",
                        "submission-release-auditor",
                    )
                ),
            )
            result = subprocess.run(
                [sys.executable, str(bundle / "bin" / "application-pack"), "--help"],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("run", result.stdout)
            self.assertIn("validate", result.stdout)

    def test_chatgpt_front_door_skill_contains_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "chatgpt"
            self._run_installer("chatgpt", output)
            front_door = output / "application-package.skill"
            self.assertTrue(front_door.is_file())
            with zipfile.ZipFile(front_door) as archive:
                names = set(archive.namelist())
            for name in (
                "application-package/SKILL.md",
                "application-package/runtime/bin/application-pack",
                "application-package/runtime/pyproject.toml",
                "application-package/runtime/src/application_pack/cli.py",
                "application-package/runtime/schemas/run-manifest.schema.json",
            ):
                self.assertIn(name, names)


if __name__ == "__main__":
    unittest.main()
