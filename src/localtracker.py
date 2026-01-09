"""Local tracking and update orchestration for PaperMC jars."""
import logging
from pathlib import Path
import paperdl, fileops


def update_server(directory: Path) -> bool:
    """Check for updates and apply them. Returns True if updated."""
    
    # 1. Check for staged .new files (interrupted update)
    staged = list(directory.glob("*.new"))
    if staged:
        # Pick the newest one
        new_file = max(staged, key=lambda f: f.stat().st_mtime)
        logging.info("Found staged update: %s", new_file.name)
        _apply_update(new_file, directory)
        return True

    # 2. Check remote
    try:
        r_ver, r_build = paperdl.get_latest_version_info()
    except Exception as e:
        logging.error("Failed to fetch remote info: %s", e)
        return False

    # 3. Check local
    current_jar = fileops.find_jar(directory)
    if current_jar:
        ver_info = fileops.get_jar_version(current_jar)
        if ver_info:
            l_ver, l_build = ver_info
            if l_ver == r_ver and l_build == r_build:
                return False  # Up to date
            logging.info("Update available: %s-%s -> %s-%s", l_ver, l_build, r_ver, r_build)
        else:
            logging.info("Current jar version unknown, forcing update.")
    else:
        logging.info("No local jar found, downloading latest.")

    # 4. Download
    try:
        dl_url, filename = paperdl.get_download_info(r_ver, r_build)
        dest = directory / (filename + ".new")
        logging.info("Downloading %s...", filename)
        paperdl.download_file(dl_url, str(dest))
        _apply_update(dest, directory)
        return True
    except Exception as e:
        logging.error("Update failed: %s", e)
        return False


def _apply_update(new_file: Path, directory: Path) -> None:
    """Promote .new file to .jar, archiving existing .jar."""
    # Target name is the new file without .new
    target_name = new_file.name.replace(".new", "")
    target_path = directory / target_name

    # Find ANY current jar to archive (might be different version/name)
    current = fileops.find_jar(directory)
    if current and current != new_file:
        logging.info("Archiving old server: %s", current.name)
        fileops.backup_file(current)
    
    logging.info("Applying update: %s", target_name)
    new_file.rename(target_path)
