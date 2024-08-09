# command_handlers/common.py

import re
from commands.common.help import get_slack_help_menu
from commands.common.cve import run_cve_command
from commands.common.version import get_version
from error_handler.errors import error_unknown_command, error_permission_denied
from role_handlers.role_registry import check_permission

def run_common_command(command: str, myaccess: str) -> str:
    if command == "help":
        if check_permission("common:help", myaccess):
            return get_slack_help_menu(myaccess)
        else:
            return error_permission_denied(command)
    
    elif command == "version":
        if check_permission("common:version", myaccess):
            return get_version()
        else:
            return error_permission_denied(command)
    
    elif re.match(r'^cve-\d{4}-\d{4,7}$', command):
        if check_permission("common:cve", myaccess):
            return run_cve_command(command)
        else:
            return error_permission_denied(command)
    
    else:
        return error_unknown_command(command, "common")
