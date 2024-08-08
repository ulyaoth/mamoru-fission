import asyncio
from azure_specific.azure_graph_access import get_azure_graph_access, close_azure_graph_access
from error_handler.errors import error_invalid_vulnerabilities_input
from msgraph.generated.security.microsoft_graph_security_run_hunting_query.run_hunting_query_post_request_body import RunHuntingQueryPostRequestBody # type: ignore

async def run_hunting_query(query: str):
    graph_client, credential = await get_azure_graph_access()

    try:
        request_body = RunHuntingQueryPostRequestBody(query=query)
        result = await graph_client.security.microsoft_graph_security_run_hunting_query.post(request_body)
        return result
    finally:
        await close_azure_graph_access(credential)

def format_response_for_total(result, top_result):
    vulnerability_count = result.results[0].additional_data["VulnerabilityCount"]
    device_count = result.results[0].additional_data["DeviceCount"]
    top_cve_id = top_result.results[0].additional_data["CveId"]
    top_device_count = top_result.results[0].additional_data["DeviceCount"]
    software_names = ", ".join(top_result.results[0].additional_data["SoftwareNames"])

    response_message = (
        "*Total Amount of Vulnerabilities Finder*\n\n"
        f"A total of *{vulnerability_count}* vulnerabilities were found spread out over *{device_count}* devices.\n\n"
        "*Most Found Vulnerability:*\n"
        f"*CVE:* {top_cve_id}\n*Devices:* {top_device_count}\n*Software Names:* {software_names}\n\n"
        "To see the specific devices, run the following query:\n"
        "```DeviceTvmSoftwareVulnerabilities\n| summarize Devices = make_set(DeviceName) by CveId\n| project CveId, Devices```\n\n"
        "Open hunting dashboard in [<https://security.microsoft.com/v2/advanced-hunting|Microsoft 365 Defender>]"
    )
    return response_message

def format_response_for_severity(level: str, result, top_result):
    severity = level.capitalize()
    vulnerability_count = result.results[0].additional_data["VulnerabilityCount"]
    device_count = result.results[0].additional_data["DeviceCount"]
    top_cve_id = top_result.results[0].additional_data["CveId"]
    top_device_count = top_result.results[0].additional_data["DeviceCount"]
    software_names = ", ".join(top_result.results[0].additional_data["SoftwareNames"])

    response_message = (
        f"*{severity} Vulnerability Finder*\n\n"
        f"A total of *{vulnerability_count}* {severity} vulnerabilities were found spread out over *{device_count}* devices.\n\n"
        f"*Most Found {severity} Vulnerability:*\n"
        f"*CVE:* {top_cve_id}\n*Devices:* {top_device_count}\n*Software Names:* {software_names}\n\n"
        "To see the specific devices, run the following query:\n"
        f"```DeviceTvmSoftwareVulnerabilities\n| where VulnerabilitySeverityLevel =~ \"{level}\"\n| summarize Devices = make_set(DeviceName) by CveId\n| project CveId, Devices```\n\n"
        "Open hunting dashboard in [<https://security.microsoft.com/v2/advanced-hunting|Microsoft 365 Defender>]"
    )
    return response_message

def run_vulnerabilities_command(input: str) -> str:
    if input.lower() in ['low', 'medium', 'high']:
        query = f"DeviceTvmSoftwareVulnerabilities | where VulnerabilitySeverityLevel =~ \"{input}\" | summarize VulnerabilityCount = dcount(CveId), DeviceCount = dcount(DeviceName) | project VulnerabilityCount, DeviceCount"
        top_query = f"DeviceTvmSoftwareVulnerabilities | where VulnerabilitySeverityLevel =~ \"{input}\" | summarize DeviceCount = dcount(DeviceName), SoftwareNames = make_set(SoftwareName) by CveId | top 1 by DeviceCount desc | project CveId, DeviceCount, SoftwareNames"
        query_results = asyncio.run(run_hunting_query(query))
        top_results = asyncio.run(run_hunting_query(top_query))
        if not query_results or not query_results.results or not top_results or not top_results.results:
            return f"No results found for {input} severity."
        return format_response_for_severity(input, query_results, top_results)
    elif input.lower() == 'total':
        query = "DeviceTvmSoftwareVulnerabilities | summarize VulnerabilityCount = dcount(CveId), DeviceCount = dcount(DeviceName) | project VulnerabilityCount, DeviceCount"
        top_query = "DeviceTvmSoftwareVulnerabilities | summarize DeviceCount = dcount(DeviceName), SoftwareNames = make_set(SoftwareName) by CveId | top 1 by DeviceCount desc | project CveId, DeviceCount, SoftwareNames"
        query_results = asyncio.run(run_hunting_query(query))
        top_results = asyncio.run(run_hunting_query(top_query))
        if not query_results or not query_results.results or not top_results or not top_results.results:
            return "No results found for total vulnerabilities."
        return format_response_for_total(query_results, top_results)
    else:
        return error_invalid_vulnerabilities_input(input, "defender")
