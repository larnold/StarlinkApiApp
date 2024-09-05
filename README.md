# Starlink Account API

## About

This python code will access the Starlink Account API "api.starlink.com" to retrieve information programatically such as Account, Billing, Orders, Users, Hardware, Subscriptions. Also provides the ability to pause and resume Starlink subscriptions and reboot terminals. The application supports retrieving information from user logins that have multiple  associated starlink accounts.

## Getting Started

Access to the Starlink API is via Access/Refresh tokens which is first obtained by using [mitmproxy](https://mitmproxy.org/) to observe logging into your Starlink account via the mobile app and observing requests submitted to "https://api.starlink.com/auth/connect/token"

### Prerequisites

This app is designed to run as an Azure Function and can be modified to run elsewhere as required. 