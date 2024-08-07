# commands/common/cve.py

import nvdlib

def run_cve_command(cve: str) -> str:
    # Fetch details for a specific CVE
    cve_id = cve
    results = nvdlib.searchCVE(cveId=cve_id)
    
    # Check if we got results and format the details into a response message
    if results:
        cve_details = results[0]
        response_message = (
            f"CVE ID: {cve_details.id}\n"
            f"Description: {cve_details.descriptions[0].value}\n"
            f"Published Date: {cve_details.published}\n"
            f"Last Modified Date: {cve_details.lastModified}\n"
            f"CVSS v3.1 Score: {cve_details.v31score}\n"
            f"CVSS v3.1 Severity: {cve_details.v31severity}\n"
        )
    else:
        response_message = f"No details found for {cve_id}"

    return response_message
