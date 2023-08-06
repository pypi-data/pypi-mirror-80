BLACKLISTED_FILES = {".DS_Store"}

WHITELISTED_FILEEXTS = {
    "ipynb",
}

DEFAULT_SUPPORTED_OPTIONS = {
    "frameworks": {"values": ["pytorch", "tensorflow"]},
    "machine_types": {"values": ["CPU", "K80", "V100"], "default": "CPU"},
}

VERSION_REQUIREMENTS = {"eksctl": "0.19.0"}
