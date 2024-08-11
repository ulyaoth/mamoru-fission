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

def format_ip_checker_response(azure_activity_result, signin_logs_result, device_network_events_result, ip_address):
    found_in_azure_activity = azure_activity_result.results[0].additional_data["FoundInAzureActivityLogs"]
    caller_list = azure_activity_result.results[0].additional_data.get("CallerList", "None")

    found_in_signin_logs = signin_logs_result.results[0].additional_data["FoundInSigninLogs"]
    user_list = signin_logs_result.results[0].additional_data.get("UserList", "None")

    found_in_device_network_events = device_network_events_result.results[0].additional_data["FoundInDeviceNetworkEvents"]
    device_list = device_network_events_result.results[0].additional_data.get("DeviceList", "None")

    response_message = (
        "*IP Checker*\n\n"
        f"See below the results for IP *{ip_address}* based on the last 7 days.\n\n"
        f"*Found In Azure Activity Logs:* {found_in_azure_activity}\n"
        f"*Caller List:* {caller_list}\n\n"
        f"*Found In SignIn Logs:* {found_in_signin_logs}\n"
        f"*User List:* {user_list}\n\n"
        f"*Found In Device Network Events Logs:* {found_in_device_network_events}\n"
        f"*Device List:* {device_list}\n"
    )
    return response_message

def run_ip_checker_command(ip_address: str) -> str:
    # Query to check AzureActivity logs
    azure_activity_query = (
        f"let IPToCheck = \"{ip_address}\";\n"
        "let Found = AzureActivity\n"
        "| where CallerIpAddress == IPToCheck\n"
        "| where TimeGenerated >= ago(7d)\n"
        "| summarize ActivityCount = count(), Callers = make_set(Caller);\n"
        "Found\n"
        "| extend FoundInAzureActivityLogs = iff(ActivityCount > 0, 'Yes', 'No'),\n"
        "         CallerList = strcat_array(Callers, ', ')\n"
        "| project FoundInAzureActivityLogs, CallerList"
    )
    azure_activity_result = asyncio.run(run_hunting_query(azure_activity_query))
    
    # Query to check SignIn logs
    signin_logs_query = (
        f"let IPToCheck = \"{ip_address}\";\n"
        "let Found = SigninLogs\n"
        "| where IPAddress == IPToCheck\n"
        "| where TimeGenerated >= ago(7d)\n"
        "| summarize SigninCount = count(), UserPrincipalNames = make_set(UserPrincipalName);\n"
        "Found\n"
        "| extend FoundInSigninLogs = iff(SigninCount > 0, 'Yes', 'No'),\n"
        "         UserList = strcat_array(UserPrincipalNames, ', ')\n"
        "| project FoundInSigninLogs, UserList"
    )
    signin_logs_result = asyncio.run(run_hunting_query(signin_logs_query))
    
    # Query to check DeviceNetworkEvents logs
    device_network_events_query = (
        f"let IPToCheck = \"{ip_address}\";\n"
        "let Found = DeviceNetworkEvents\n"
        "| where TimeGenerated >= ago(7d)\n"
        "| where LocalIP == IPToCheck or RemoteIP == IPToCheck\n"
        "| summarize EventCount = count(), DeviceNames = make_set(DeviceName);\n"
        "Found\n"
        "| extend FoundInDeviceNetworkEvents = iff(EventCount > 0, 'Yes', 'No'),\n"
        "         DeviceList = strcat_array(DeviceNames, ', ')\n"
        "| project FoundInDeviceNetworkEvents, DeviceList"
    )
    device_network_events_result = asyncio.run(run_hunting_query(device_network_events_query))
    
    # Format the response
    return format_ip_checker_response(azure_activity_result, signin_logs_result, device_network_events_result, ip_address)
