"""File operations helpers for managing PaperMC server jars."""
from pathlib import Path
from typing import Optional


def find_jar(directory: Path) -> Optional[Path]:
    """Find the current server jar (excludes .old and .new files)."""
    # Returns the first jar found that isn't a backup or staged file
    return next(directory.glob("*.jar"), None)


def get_jar_version(path: Path) -> Optional[tuple[str, int]]:
    """Extract version and build from filename (e.g. paper-1.20.1-123.jar)."""
    try:
        # Expecting format: name-version-build.jar
        parts = path.stem.split("-")
        if len(parts) >= 3:
            return parts[-2], int(parts[-1])
    except ValueError:
        pass
    return None


def backup_file(path: Path) -> Path:
    """Rename file to file.old (incrementing if needed)."""
    base = path.name + ".old"
    target = path.with_name(base)
    i = 1
    while target.exists():
        target = path.with_name(f"{base}.{i}")
        i += 1
    path.rename(target)
    return target


def restore_backup(directory: Path) -> Optional[Path]:
    """Restore the most recent .old file to .jar, backing up current."""
    # Find .old files (looking for .jar.old pattern)
    backups = list(directory.glob("*.jar.old*"))
    if not backups:
        return None
    
    # Sort by modification time
    latest_backup = max(backups, key=lambda f: f.stat().st_mtime)
    
    # Determine original name (everything before .old)
    new_name = latest_backup.name.split(".old")[0]
    target_path = directory / new_name

    # Archive current jar if it exists
    current = find_jar(directory)
    if current:
        backup_file(current)
    
    latest_backup.rename(target_path)
    return target_path
