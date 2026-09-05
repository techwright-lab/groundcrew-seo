#!/usr/bin/env python3
"""Exercise the actual stdin installer against a local release with divergent main."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = (ROOT / "install.sh").read_text()


def run(command, **kwargs):
    return subprocess.run(command, text=True, capture_output=True, check=True, **kwargs)


with tempfile.TemporaryDirectory(prefix="groundcrew-installer-") as temporary:
    root = Path(temporary)
    repo = root / "remote"
    repo.mkdir()
    for name in ("skills", "shared", "scripts"):
        shutil.copytree(ROOT / name, repo / name)
    shutil.copy2(ROOT / "install.sh", repo / "install.sh")
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_CONFIG_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=str(root / "gitconfig"), GIT_ALLOW_PROTOCOL="file")
    (root / "gitconfig").write_text(f'[url "{repo.as_uri()}"]\n\tinsteadOf = https://github.com/techwright-lab/groundcrew-seo\n')
    run(["git", "init", "-q", "-b", "main", str(repo)], env=env)
    run(["git", "-C", str(repo), "add", "."], env=env)
    run(["git", "-C", str(repo), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.test", "commit", "-qm", "reviewed release"], env=env)
    candidate = run(["git", "-C", str(repo), "rev-parse", "HEAD"], env=env).stdout.strip()
    run(["git", "-C", str(repo), "tag", "v1.1.0"], env=env)
    skill = "fix-my-site/SKILL.md"
    expected = (repo / "skills" / skill).read_bytes()
    (repo / "skills" / skill).write_bytes(expected + b"\nUnreviewed default-main content\n")
    run(["git", "-C", str(repo), "add", "."], env=env)
    run(["git", "-C", str(repo), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.test", "commit", "-qm", "divergent main"], env=env)

    for scenario, unrelated, ref in (("outside", False, []), ("unrelated-cwd", True, []), ("exact-sha", True, ["--ref", candidate])):
        cwd = root / scenario
        cwd.mkdir()
        if unrelated:
            (cwd / "skills/foreign").mkdir(parents=True)
            (cwd / "skills/foreign/SKILL.md").write_text("unrelated local skill")
            (cwd / "shared").mkdir()
        destination = root / f"{scenario}-installed"
        result = run(["bash", "-s", "--", "--skills-dir", str(destination), *ref], input=INSTALLER, cwd=cwd, env=env)
        assert (destination / skill).read_bytes() == expected, (scenario, "installed default main instead of release", result.stdout)
        assert not (destination / "foreign").exists(), scenario
        print(f"PASS actual stdin installer {scenario}: reviewed tag bytes, divergent main excluded")

    missing = subprocess.run(["bash", "-s", "--", "--skills-dir", str(root / "missing"), "--ref", "missing-ref"], input=INSTALLER, text=True, capture_output=True, cwd=root / "outside", env=env)
    assert missing.returncode != 0 and not (root / "missing").exists(), missing
    print("PASS unavailable ref fails before installation")

print("actual installer tests passed (local Git only; network protocols disabled)")
