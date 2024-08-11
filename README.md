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
  - [Teams bot](#teams-bot)
  - [Microsoft Connection](#microsoft-connection)
  - [Microsoft Entra Auth](#microsoft-entra-auth)
  - [Slack User Auth](#slack-user-auth)
  - [User Role](#user-roles)
  - [How to Install](#how-to-install)
  - [Create a DEMO Environment](#create-a-demo-environment)
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

Look at the secrets [example](./config/mamoru-secrets-example.yaml).

## Teams bot

If you want to use this bot in Team, you need to have a Teams app, connected to a teams bot, this bot should post to your functions endpoint, you also need a managed identity configured and have the following permissions minimal:

Microsoft Graph:
* Chat.ReadWrite
* User.Read
* Directory.Read.All
* Team.ReadBasic.All
* ChannelMessage.Send
* Channel.ReadBasic.All

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
* Application.Read.All

Microsoft Threat Protection:
* Incident.Read.All
* AdvancedHunting.Read.All

Windows Defender ATP:
* AdvancedQuery.Read.All
* Vulnerability.Read.All

Most of the default commands use the permissions listed above. If you want to perform other tasks in Azure, make sure to adjust the permissions accordingly.

Make sure you update your secret with the required information.
Secrets [example](./config/mamoru-secrets-example.yaml).


## Microsoft Entra Auth

In order to use Microsoft Entra Authentication, ensure that you add the necessary permissions to your application in Entra.

Required permissions under 'Microsoft Graph':
* User.Read.All
* Directory.Read.All
* Group.Read.All

Create the following groups in Microsoft Entra:
- mamoru-access-user-sg
- mamoru-access-guest-sg
- mamoru-access-admin-sg

Then, add the appropriate individuals to those groups as needed.

Next, refer to the configmap [example](./config/mamoru-configmap-microsoft_entra_example.yaml)

Ensure that you update the configmap accordingly.

Explanation on Authentication:
Please note that if you use Slack with Microsoft Entra Authentication, it only works if your Slack users have the same email address as the one used in Microsoft Entra.

Here's how it works: The process retrieves the user's Slack user ID, queries the Slack API, and then retrieves the associated email address. Once it has the email, it will attempt to find the user in Entra and verify if they belong to the appropriate Mamoru group (user, admin, or guest)."

## Slack User Auth

This authentication method can only be used if your bot is exclusively used in Slack. Unfortunately, it is a very manual implementation, so you'll need to keep things up to date yourself.

Open the following configmap [example](./config/mamoru-configmap-slack_user_verification_example.yaml)

Make sure you use: AUTH_METHOD: "slack_user_verification"

And then create the following:

  AUTHORIZED_SLACK_USERS: |
    [
      {"name": "Example User", "userid": "U0IB44ZER", "permission": "admin"},
      {"name": "XXX", "userid": "XXX", "permission": "user"},
      {"name": "XXX", "userid": "XXX", "permission": "guest"}
    ]

As you can see, it's manual work to keep this up to date, you'll need to manually enter the name of each person and their Slack user ID.

## User Roles

The app is mostly dynamic, allowing you to create your own user roles. However, these custom roles might not fully integrate with the help files.

Currently supported roles: guest, user, and admin.

The admin role has default access and should never need to be included in the roles configmap.

Refer to the roles configmap [example](./config/mamoru-roles-configmap-example.yaml)

As you can see, it's fairly straightforward—decide for yourself which roles should have access to specific commands.

## How to Install

Example for an already existing kubernetes environment with fission and their cli installed:

```bash
# Download the mamoru code
git clone git@github.com:ulyaoth/mamoru-fission.git
```

Inside "mamoru-fission/config":
Now alter the config files for your needs and apply them you should end up with 2 configmaps and 1 secret.

You can apply a configmap or secret as below.
```bash
kubectl apply -f example.yaml
```

Once you applied all three files with your correct info then go to the main folder "mamoru-fission" and run:

```bash
fission spec apply --wait
```

## Create a DEMO Environment

Start a fresh install server and run the following commands:

Make sure to check for the latest fission version first.

```bash
curl -sfL https://get.k3s.io | sh -
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
export FISSION_NAMESPACE="fission"
kubectl create namespace $FISSION_NAMESPACE
kubectl create -k "github.com/fission/fission/crds/v1?ref=v1.20.3"
helm repo add fission-charts https://fission.github.io/fission-charts/
helm repo update
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
helm install --version v1.20.3 --namespace $FISSION_NAMESPACE fission fission-charts/fission-all
curl -Lo fission https://github.com/fission/fission/releases/download/v1.20.3/fission-v1.20.3-linux-amd64 && chmod +x fission && sudo mv fission /usr/local/bin/
git clone git@github.com:ulyaoth/mamoru-fission.git
```

Inside "mamoru-fission/config":
Now alter the config files for your needs and apply them you should end up with 2 configmaps and 1 secret.

You can apply a configmap or secret as below.
```bash
kubectl apply -f example.yaml
```

Once you applied all three files with your correct info then go to the main folder "mamoru-fission" and run:

```bash
fission spec apply --wait
```

# License

Mamoru is licensed under the European Union Public License 1.2 - see the [LICENSE](./LICENSE) file for details