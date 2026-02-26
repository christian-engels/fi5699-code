import os
import subprocess
import sys
import platform


def is_codespaces():
    return os.environ.get("CODESPACES") == "true" or "CODESPACE_NAME" in os.environ


def main():
    utilities_dir = os.path.dirname(os.path.abspath(__file__))

    # Build commit message
    message = "Saved from GitHub Codespaces" if is_codespaces(
    ) else "Saved from local computer"

    system = platform.system().lower()
    try:
        if system in ("linux", "darwin"):
            script = os.path.join(utilities_dir, "commit_push.sh")
            # Ensure executable bit (best-effort)
            try:
                os.chmod(script, 0o755)
            except Exception:
                pass
            subprocess.run([script, message], check=True)
        elif system == "windows":
            script = os.path.join(utilities_dir, "commit_push.ps1")
            # Use PowerShell to run the script
            subprocess.run([
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-File", script,
                message,
            ], check=True)
        else:
            # Fallback to direct git calls with change detection
            status = subprocess.run(
                ["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
            if not status.stdout.strip():
                print("No changes to commit.")
                return
            subprocess.run(["git", "add", "-A"], check=True)
            # Ensure something is staged
            # returncode 0 means no diff
            staged_check = subprocess.run(
                ["git", "diff", "--cached", "--quiet"])
            if staged_check.returncode == 0:
                print("No staged changes to commit.")
                return
            subprocess.run(["git", "commit", "-m", message], check=True)
            # Push, setting upstream if needed
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
            has_upstream = subprocess.run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name",
                                          "@{u}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if has_upstream.returncode == 0:
                subprocess.run(["git", "push"], check=True)
            else:
                subprocess.run(
                    ["git", "push", "-u", "origin", branch], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")
        sys.exit(e.returncode if hasattr(e, 'returncode') else 1)


if __name__ == "__main__":
    main()
