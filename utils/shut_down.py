from utils.logger import log_info


def system_shutdown():
    log_info("Initiating system shutdown...")
    # Insert cleanup code: close databases, disconnect from robots, etc.
    log_info("System shutdown complete.")