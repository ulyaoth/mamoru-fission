<p align="center">
  <img src="https://raw.githubusercontent.com/ulyaoth/mamoru-fission/main/slack-bot-image-512x512.png" />
  <br>
  <h1 align="center">Mamoru: your security assistant and more!</h1>
</p>

<p align="center">
  <a href="https://github.com/ulyaoth/mamoru-fission/blob/main/LICENSE">
    <img alt="Mamoru Licence" src="https://img.shields.io/github/license/ulyaoth/mamoru-fission">
  </a>
  <a href="https://github.com/ulyaoth/mamoru-fission/releases">
    <img alt="Mamoru Releases" src="https://img.shields.io/github/release-pre/ulyaoth/mamoru-fission.svg">
  </a>
  <a href="https://github.com/ulyaoth/mamoru-fission/graphs/contributors">
    <img alt="Fission contributors" src="https://img.shields.io/github/contributors/ulyaoth/mamoru-fission">
  </a>
  <a href="https://github.com/ulyaoth/mamoru-fission/commits/main">
    <img alt="Commit Activity" src="https://img.shields.io/github/commit-activity/m/ulyaoth/mamoru-fission">
  </a>
  <br>
  <a href="https://github.com/ulyaoth/mamoru-fission">
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/ulyaoth/mamoru-fission?style=social">
  </a>
</p>

--------------

Mamoru is an open-source bot written in Python designed to run commands in Slack, with a focus on security. The idea is that it can execute commands targeting tools like Defender, Elastic Stack, and other systems, and provide information in return.

Table of Contents
=================
- [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Slack bot](#slack-bot)
  - [Microsoft Connection](#microsoft-connection)
  - [Slack User Auth](#slack-user-auth)
- [License](#license)

## Prerequisites

- Kubernetes cluster with Fission installed.
- Fission CLI installed
- Git installed

## Slack bot

If you want to use this bot in Slack, you need to create a Slack app and gather the following information:

- Slack App Signing Secret
- Slack App ID
- Slack App Bot User OAuth Token

## Microsoft Connection

Create an app in Microsoft Entra and collect the following information:

- Azure App Client ID
- Azure App Client Secret
- Azure Tenant ID

You need to assign the app permissions based on the tasks you want to perform. Below are some examples:

Microsoft Graph:
* Device.Read.All
* DeviceManagementManagedDevices.Read.All
* ThreatHunting.Read.All

Microsoft Threat Protection:
* Incident.Read.All
* AdvancedHunting.Read.All

Windows Defender ATP:
* AdvancedQuery.Read.All
* Vulnerability.Read.All

Most of the default commands use the permissions listed above. If you want to perform other tasks in Azure, make sure to adjust the permissions accordingly.

# License

Mamoru is licensed under the European Union Public License 1.2 - see the [LICENSE](./LICENSE) file for details