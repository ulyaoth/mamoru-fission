import asyncio
from azure_specific.azure_graph_access import get_azure_graph_access, close_azure_graph_access
from msgraph.generated.security.microsoft_graph_security_run_hunting_query.run_hunting_query_post_request_body import RunHuntingQueryPostRequestBody # type: ignore

async def run_hunting_query(query: str):
    graph_client, credential = await get_azure_graph_access()

    try:
        request_body = RunHuntingQueryPostRequestBody(
            query=query
        )
        result = await graph_client.security.microsoft_graph_security_run_hunting_query.post(request_body)
        return result
    finally:
        await close_azure_graph_access(credential)

def format_most_vulnerable_response(result, last_login_result):
    device_name = result.results[0].additional_data["DeviceName"]
    high_count = result.results[0].additional_data["HighSeverityCount"]
    medium_count = result.results[0].additional_data["MediumSeverityCount"]
    low_count = result.results[0].additional_data["LowSeverityCount"]
    last_login = last_login_result.results[0].additional_data["UserName"]

    response_message = (
        "*Most Vulnerable Endpoint*\n\n"
        f"On endpoint *{device_name}* the following amount of vulnerabilities were found:\n\n"
        f"*High:* {high_count}\n"
        f"*Medium:* {medium_count}\n"
        f"*Low:* {low_count}\n"
        f"Last login by: *{last_login}*\n\n"
        "To see the full details of the device in question, run the following query:\n"
        f"```DeviceTvmSoftwareVulnerabilities\n| where DeviceName == \"{device_name}\"\n| summarize CVE_List = make_list(CveId) by SoftwareName\n| extend CVE_List = strcat_array(CVE_List, \", \")\n| project SoftwareName, CVE_List```\n\n"
        "Open hunting dashboard in [<https://security.microsoft.com/v2/advanced-hunting|Microsoft 365 Defender>]"
    )
    return response_message

def format_specific_device_response(device_name, result):
    high_count = result.results[0].additional_data["HighCount"]
    medium_count = result.results[0].additional_data["MediumCount"]
    low_count = result.results[0].additional_data["LowCount"]

    response_message = (
        "*Specific Endpoint Vulnerability Summary*\n\n"
        f"On endpoint *{device_name}* the following amount of vulnerabilities were found:\n\n"
        f"*High:* {high_count}\n"
        f"*Medium:* {medium_count}\n"
        f"*Low:* {low_count}\n\n"
        "To see the full details of the device in question, run the following query:\n"
        f"```DeviceTvmSoftwareVulnerabilities\n| where DeviceName == \"{device_name}\"```\n\n"
        "Open hunting dashboard in [<https://security.microsoft.com/v2/advanced-hunting|Microsoft 365 Defender>]"
    )
    return response_message

def run_endpoint_command(input: str) -> str:
    if input.lower() == "mostvln":
        # Query to find the most vulnerable endpoint
        query = (
            "DeviceTvmSoftwareVulnerabilities\n"
            "| summarize HighSeverityCount = countif(VulnerabilitySeverityLevel == \"High\"), "
            "MediumSeverityCount = countif(VulnerabilitySeverityLevel == \"Medium\"), "
            "LowSeverityCount = countif(VulnerabilitySeverityLevel == \"Low\") "
            "by DeviceName, DeviceId\n"
            "| extend TotalVulnerabilities = HighSeverityCount + MediumSeverityCount + LowSeverityCount\n"
            "| top 1 by TotalVulnerabilities desc"
        )
        result = asyncio.run(run_hunting_query(query))
        
        if not result or not result.results:
            return "No results found for most vulnerable endpoint."

        # Query to find the last login user for the most vulnerable endpoint
        device_name = result.results[0].additional_data["DeviceName"]
        last_login_query = (
            f"DeviceInfo\n"
            f"| where DeviceName == \"{device_name}\"\n"
            "| extend LoggedOnUsersArray = parse_json(LoggedOnUsers)\n"
            "| mv-expand LoggedOnUsersArray\n"
            "| project Timestamp, UserName = LoggedOnUsersArray.UserName\n"
            "| sort by Timestamp desc\n"
            "| project UserName\n"
            "| limit 1"
        )
        last_login_result = asyncio.run(run_hunting_query(last_login_query))
        
        if not last_login_result or not last_login_result.results:
            return f"Found most vulnerable endpoint {device_name}, but no login information available."

        return format_most_vulnerable_response(result, last_login_result)

    else:
        # Assume input is a device name
        device_name = input.strip()
        # Query to check if the device exists
        existence_query = (
            f"DeviceTvmSoftwareVulnerabilities\n"
            f"| where DeviceName =~ \"{device_name}\"\n"
            "| summarize recordCount = count()\n"
            "| extend checkExistence = (recordCount > 0)\n"
            "| project checkExistence"
        )
        existence_result = asyncio.run(run_hunting_query(existence_query))

        if not existence_result or not existence_result.results or not existence_result.results[0].additional_data["checkExistence"]:
            return f"The device '{device_name}' does not exist or has no recorded vulnerabilities."

        # Query to get vulnerabilities summary for the specific device
        summary_query = (
            f"DeviceTvmSoftwareVulnerabilities\n"
            f"| where DeviceName =~ \"{device_name}\"\n"
            "| summarize LowCount = countif(tolower(VulnerabilitySeverityLevel) == \"low\"),"
            " MediumCount = countif(tolower(VulnerabilitySeverityLevel) == \"medium\"),"
            " HighCount = countif(tolower(VulnerabilitySeverityLevel) == \"high\")"
        )
        summary_result = asyncio.run(run_hunting_query(summary_query))

        if not summary_result or not summary_result.results:
            return f"No vulnerability data found for the device '{device_name}'."

        return format_specific_device_response(device_name, summary_result)
