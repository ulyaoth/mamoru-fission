# commands/sentinel/incidents.py

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

def format_sentinel_incidents_response(result, incident_type: str) -> str:
    if incident_type == "open":
        return (
            "*Open Incidents in Sentinel*\n\n"
            f"In the last 30 days, *{result.results[0].additional_data['TotalOpenIncidents']}* Sentinel incidents are open.\n\n"
            f"*High:* {result.results[0].additional_data['HighSeverityCount']}\n"
            f"*Medium:* {result.results[0].additional_data['MediumSeverityCount']}\n"
            f"*Low:* {result.results[0].additional_data['LowSeverityCount']}\n"
            f"*Informational:* {result.results[0].additional_data['InformationalSeverityCount']}\n\n"
            "To see all open incidents in the interface, please visit the Microsoft Sentinel dashboard."
        )
    elif incident_type == "closed":
        return (
            "*Closed Incidents in Sentinel*\n\n"
            f"In the last 30 days, *{result.results[0].additional_data['TotalClosedIncidents']}* Sentinel incidents were closed.\n\n"
            f"*High:* {result.results[0].additional_data['HighSeverityCount']}\n"
            f"*Medium:* {result.results[0].additional_data['MediumSeverityCount']}\n"
            f"*Low:* {result.results[0].additional_data['LowSeverityCount']}\n"
            f"*Informational:* {result.results[0].additional_data['InformationalSeverityCount']}\n\n"
            "To see all closed incidents in the interface, please visit the Microsoft Sentinel dashboard."
        )
    elif incident_type == "summary":
        return (
            "*Sentinel Incidents Summary*\n\n"
            "In the last 30 days:\n"
            f"- Open incidents: *{result.results[0].additional_data['TotalOpenIncidents']}*\n"
            f"- Closed incidents: *{result.results[0].additional_data['TotalClosedIncidents']}*\n"
            "To see more details, please visit the Microsoft Sentinel dashboard."
        )
    elif incident_type == "trending":
        trending_summary = "*Incident Trends Over the Past 4 Weeks*\n\n"
        for week in result.results:
            trending_summary += (
                f"*@{week.additional_data['WeekNumber']}*:\n"
                f"High: *{week.additional_data['HighSeverityCount']}*, "
                f"Medium: *{week.additional_data['MediumSeverityCount']}*, "
                f"Low: *{week.additional_data['LowSeverityCount']}*, "
                f"Informational: *{week.additional_data['InformationalSeverityCount']}*\n\n"
            )
        return trending_summary.strip()  # Remove any trailing newline

def run_sentinel_incidents_command(incident_type: str) -> str:
    if incident_type == "open":
        query = (
            "let last30DaysIncidents = SecurityIncident\n"
            "| where TimeGenerated >= ago(30d);\n"
            "let latestIncidents = last30DaysIncidents\n"
            "| summarize arg_max(TimeGenerated, *) by ProviderIncidentId;\n"
            "let openIncidents = latestIncidents\n"
            "| where Status in ('New', 'Active');\n"
            "openIncidents\n"
            "| summarize HighSeverityCount = countif(Severity == 'High'), "
            "MediumSeverityCount = countif(Severity == 'Medium'), "
            "LowSeverityCount = countif(Severity == 'Low'), "
            "InformationalSeverityCount = countif(Severity == 'Informational')\n"
            "| extend TotalOpenIncidents = HighSeverityCount + MediumSeverityCount + LowSeverityCount + InformationalSeverityCount"
        )
    elif incident_type == "closed":
        query = (
            "let last30DaysIncidents = SecurityIncident\n"
            "| where TimeGenerated >= ago(30d);\n"
            "let latestIncidents = last30DaysIncidents\n"
            "| summarize arg_max(TimeGenerated, *) by ProviderIncidentId;\n"
            "let closedIncidents = latestIncidents\n"
            "| where Status == 'Closed';\n"
            "closedIncidents\n"
            "| summarize HighSeverityCount = countif(Severity == 'High'), "
            "MediumSeverityCount = countif(Severity == 'Medium'), "
            "LowSeverityCount = countif(Severity == 'Low'), "
            "InformationalSeverityCount = countif(Severity == 'Informational')\n"
            "| extend TotalClosedIncidents = HighSeverityCount + MediumSeverityCount + LowSeverityCount + InformationalSeverityCount"
        )
    elif incident_type == "summary":
        query = (
            "let last30DaysIncidents = SecurityIncident\n"
            "| where TimeGenerated >= ago(30d);\n"
            "let latestIncidents = last30DaysIncidents\n"
            "| summarize arg_max(TimeGenerated, *) by ProviderIncidentId;\n"
            "let summary = latestIncidents\n"
            "| summarize TotalClosedIncidents = countif(Status == 'Closed'), "
            "TotalOpenIncidents = countif(Status in ('New', 'Active'));\n"
            "summary"
        )
    elif incident_type == "trending":
        query = (
            "let last30DaysIncidents = SecurityIncident\n"
            "| where TimeGenerated >= ago(30d);\n"
            "let latestIncidents = last30DaysIncidents\n"
            "| summarize arg_max(TimeGenerated, *) by ProviderIncidentId;\n"
            "latestIncidents\n"
            "| extend WeekNumber = strcat('Week ', tostring(datepart('WeekOfYear', TimeGenerated)), ', ', tostring(datepart('Year', TimeGenerated)))\n"
            "| summarize HighSeverityCount = countif(Severity == 'High'), "
            "MediumSeverityCount = countif(Severity == 'Medium'), "
            "LowSeverityCount = countif(Severity == 'Low'), "
            "InformationalSeverityCount = countif(Severity == 'Informational') by WeekNumber\n"
            "| sort by WeekNumber asc"
        )
    else:
        return "Invalid incident type. Please use 'open', 'closed', 'summary', or 'trending'."

    result = asyncio.run(run_hunting_query(query))
    return format_sentinel_incidents_response(result, incident_type)
