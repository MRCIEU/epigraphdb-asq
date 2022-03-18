from pathlib import Path

from loguru import logger


def find_project_root(anchor_file: str = "environment.yml") -> Path:
    cwd = Path.cwd()
    test_dir = cwd
    prev_dir = None
    while prev_dir != test_dir:
        if (test_dir / anchor_file).exists():
            return test_dir
        prev_dir = test_dir
        test_dir = test_dir.parent
    return cwd


def find_data_root() -> Path:
    proj_root = find_project_root()
    # NOTE: atm analysis is the sub directory of repo root
    repo_root = (proj_root / "..").resolve()
    path = repo_root / "data"
    if not path.exists():
        logger.info(f"Path {path} does not exists")
    return path


def find_analysis_artifacts_dir() -> Path:
    data_root = find_data_root()
    path = data_root / "analysis-artifacts"
    if not path.exists():
        logger.info(f"Path {path} does not exists")
    return path
