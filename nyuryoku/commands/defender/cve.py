# commands/defender/cve.py

import re
import asyncio
from azure_specific.azure_graph_access import get_azure_graph_access, close_azure_graph_access
from error_handler.errors import error_invalid_cve_format
from msgraph.generated.security.microsoft_graph_security_run_hunting_query.run_hunting_query_post_request_body import RunHuntingQueryPostRequestBody # type: ignore

async def run_hunting_query(cve_id: str):
    graph_client, credential = await get_azure_graph_access()

    try:
        request_body = RunHuntingQueryPostRequestBody(
            query=f"DeviceTvmSoftwareVulnerabilities | where CveId =~ \"{cve_id}\" | summarize DeviceCount = dcount(DeviceName) by CveId | project CveId, DeviceCount",
        )

        result = await graph_client.security.microsoft_graph_security_run_hunting_query.post(request_body)
        return result
    finally:
        await close_azure_graph_access(credential)

def format_response(cve: str, result=None):
    if result and result.results:
        cve_id = result.results[0].additional_data["CveId"]
        device_count = result.results[0].additional_data["DeviceCount"]
        response_message = (
            f"*{cve_id}* was found on *{device_count}* devices.\n\n"
            "To see the specific devices, run the following query:\n"
            f"```DeviceTvmSoftwareVulnerabilities\n| where CveId =~ \"{cve_id}\"\n| summarize Devices = strcat_array(make_list(DeviceName), \", \") by CveId\n| project CveId, Devices```\n\n"
            "Open hunting dashboard in [<https://security.microsoft.com/v2/advanced-hunting|Microsoft 365 Defender>]"
        )
    else:
        response_message = (
            f"*{cve}* was not found on any devices.\n\n"
            "To see this manually, use the below query:\n"
            f"```DeviceTvmSoftwareVulnerabilities\n| where CveId =~ \"{cve}\"```\n\n"
            "Open hunting dashboard in [<https://security.microsoft.com/v2/advanced-hunting|Microsoft 365 Defender>]"
        )
    return response_message

def is_valid_cve_format(cve: str) -> bool:
    pattern = r'^CVE-\d{4}-\d{4,7}$'
    return re.match(pattern, cve, re.IGNORECASE) is not None

def run_cve_command(cve: str) -> str:
    if not is_valid_cve_format(cve):
        return error_invalid_cve_format(cve, "defender")
    
    query_results = asyncio.run(run_hunting_query(cve))
    if not query_results or not query_results.results:
        return format_response(cve)
    else:
        return format_response(cve, query_results)
