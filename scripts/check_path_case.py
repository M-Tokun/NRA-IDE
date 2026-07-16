"""Check that every Git-tracked path matches the on-disk letter case exactly.

Windows and default macOS filesystems are case-insensitive, so a path with the
wrong case still opens successfully there. Linux CI runners are case-sensitive,
so a mismatch between the case Git recorded and the actual case on disk will
break `open()`, imports, and links only after checkout on Linux. This check
catches that class of bug locally, before it reaches CI.
"""
import subprocess
import sys
import os


def tracked_paths() -> list[str]:
    output = subprocess.run(
        ["git", "ls-files"],
        capture_output=True,
        check=True,
        encoding="utf-8",
    ).stdout
    return [line for line in output.splitlines() if line]


def actual_case(path: str) -> str | None:
    """Return the on-disk path with real casing, or None if it cannot be resolved."""
    parts = path.split("/")
    current = "."
    resolved = []
    for part in parts:
        if not os.path.isdir(current) and current != ".":
            return None
        try:
            entries = os.listdir(current)
        except OSError:
            return None
        match = next((entry for entry in entries if entry.lower() == part.lower()), None)
        if match is None:
            return None
        resolved.append(match)
        current = os.path.join(current, match)
    return "/".join(resolved)


def main() -> int:
    errors = []
    for path in tracked_paths():
        real = actual_case(path)
        if real is None:
            # Deleted-but-still-tracked or submodule-like path; not this check's concern.
            continue
        if real != path:
            errors.append(f"{path}  (on disk: {real})")

    if errors:
        print("FAIL path case mismatch between Git and the filesystem:")
        for e in errors:
            print(f"  {e}")
        print(
            "\nThese paths will fail to open on case-sensitive filesystems "
            "(Linux CI, most macOS setups) even though they work on Windows."
        )
        return 1

    print(f"OK  path case matches for {len(tracked_paths())} tracked files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
