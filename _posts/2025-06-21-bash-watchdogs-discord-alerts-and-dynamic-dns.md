---
tags: [scratchpad]
info: aberto.
date: 2025-06-21
type: post
layout: post
published: true
slug: bash-watchdogs-discord-alerts-and-dynamic-dns
title: 'Bash Watchdogs, Discord Alerts, and Dynamic DNS'
---
## SSH Watcher

Make sure your server is set up to allow SSH logins with public keys and, **at the server console or shell, as `root`, login to your local server (yes, recursively):**

```bash
ssh <ipaddress you want to be monitored>
```

The first time you do this, you should get a message about remembering the fingerprint – say “yes”.

You will be logged into the server in an SSH shell from your current SSH shell. You can exit.  
Next time you log in like this:

```bash
ssh <ipaddress you want to be monitored>
```

there should be **no prompt**.

Create a file `/opt/watchdog/watchdog-ssh.sh`

```bash
#!/bin/bash
SSH_USER="root"
SSH_HOST="<ipaddress you want to be monitored>"
SSH_PORT="<port of ssh>"

attempt_ssh_login() {
    local user="$1"
    local host="$2"
    local port="$3"
    echo "Attempting SSH login to $user@$host:$port..."
    ssh -o BatchMode=yes \
        -o ConnectTimeout=10 \
        -o StrictHostKeyChecking=no \
        -o PasswordAuthentication=no \
        -p "$port" "$user@$host" "exit" &> /dev/null
    return $?   # Return the exit status of the ssh command
}

# Perform the SSH login attempt
attempt_ssh_login "$SSH_USER" "$SSH_HOST" "$SSH_PORT"

# Check the exit status
SSH_STATUS=$?

if [ "$SSH_STATUS" -eq 0 ]; then
    # --- Actions on SUCCESS ---
    echo "SSH login to $SSH_USER@$SSH_HOST:$SSH_PORT successful!"
    echo "Nothing to do, exiting."
    # You can put a script here but consider this runs every 5 minutes.
    exit 0

elif [ "$SSH_STATUS" -ne 0 ]; then
    # --- Actions on FAILURE ---
    echo "SSH login to $SSH_USER@$SSH_HOST:$SSH_PORT FAILED (Exit Code: $SSH_STATUS)."
    echo "Restarting sshd..."
    systemctl restart ssh.service   # Restart the SSH service; your distro might vary.
    # /path/scriptToRun.sh  # you can run a script here; make sure it is +x and on PATH.
    exit 1

else
    # This block should not be reached if SSH_STATUS is always 0 or non-zero, but for completeness:
    echo "An unexpected error occurred."
    exit 2
fi
```

Make the file executable:

```bash
chmod +x /opt/watchdog/watchdog-ssh.sh
```

Open crontab and put the line there to run every 5 minutes:

```bash
crontab -e
```

Add this on a new line:

```bash
*/5 * * * * /opt/watchdog/watchdog-ssh.sh
```

You can manually run the script (be aware it restarts sshd) or wait a few minutes and check the crontab logs (may vary with distro):

```bash
grep CRON /var/log/syslog
```

Or you can use the script logic to write something meaningful or send a Discord notification.

> **Note:** Some distros don’t like `*/5` in a cron job. If you have that trouble, try <http://crontab.guru> for tips.

Also, you don’t have to use `root` for this. You can use any user with permissions and a valid public key.

---

## Port Watcher

Similarly, a port can be checked with `nc` (netcat). In this case, create a file `/opt/watcher/watcher-minecraft.sh`

```bash
#!/bin/bash
TARGET_HOST="172.16.30.212"   # The IP address or hostname of the target server
TARGET_PORT="25565"           # The port number to check

check_port_status() {
    local host="$1"
    local port="$2"
    echo "Checking if port $port on $host is open..."
    if nc -z -w 1 "$host" "$port" &> /dev/null; then
        return 0   # Port is open
    else
        return 1   # Port is not open
    fi
}

# Perform the port check
check_port_status "$TARGET_HOST" "$TARGET_PORT"

# Check the exit status of the port check
PORT_STATUS=$?

if [ "$PORT_STATUS" -eq 0 ]; then
    # --- Actions on SUCCESS (Port is Open) ---
    echo "Port $TARGET_PORT on $TARGET_HOST is open. Nothing to do, exiting."
    exit 0

elif [ "$PORT_STATUS" -ne 0 ]; then
    # --- Actions on FAILURE (Port is NOT Open) ---
    echo "Port $TARGET_PORT on $TARGET_HOST is NOT open (Exit Code: $PORT_STATUS)."
    echo "Attempting to restart Minecraft, watch Discord for updates..."
    cd /opt/docker
    docker compose restart minecraft   # Restart the service or run a script

    if [ $? -eq 0 ]; then
        echo "Service restarted successfully."
    else
        echo "Failed to restart service. Check Discord for updates."
    fi
    exit 1

else
    # This block should not theoretically be reached
    echo "An unexpected error occurred during port check."
    exit 2
fi
```

---

## Discord Notifications

This is the easiest way, I think, to keep track of things as the app is nice and the service is reliable.  
*I find sometimes messages might be 1–2 minutes after the fact, so this is not a real-time messaging solution.*

1. Create a Discord account, server, and webhook.

You should have a string that looks like this:

```
https://discordapp.com/api/webhooks/115954877264954...
```

2. Make a file `/opt/discord/discord.conf` and put the string in, like this:

```bash
webhook="https://discordapp.com/api/webhooks/115954877264954..."
```

3. Lock the file down:

```bash
chmod 400 /opt/discord/discord.conf
```

4. Make a file `/opt/discord/discord.sh`:

```bash
#!/bin/bash
. /opt/discord/discord.conf
curl -H "Content-Type:application/json" \
     -d "{\"username\": \"$1\", \"content\": \"$2\"}" $webhook
```

5. Make this file executable:

```bash
chmod 775 /opt/discord/discord.sh
```

Now, if you want to send a notification to your Discord channel from the command line:

```bash
root@server12:~# /opt/discord/discord.sh "username" "message"
```

This will send a message with the fields to the Discord channel on the server.  
Make sure the server is private.

Similarly, you can add that line to one of the actions above:

```bash
elif [ "$PORT_STATUS" -ne 0 ]; then
    # --- Actions on FAILURE (Port is NOT Open) ---
    echo "Port $TARGET_PORT on $TARGET_HOST is NOT open (Exit Code: $PORT_STATUS)."
    echo "Attempting to restart Minecraft, watch Discord for updates..."
    /opt/discord/discord.sh "server12" "Attempting to restart the Minecraft container..."
    cd /opt/docker
    docker compose restart minecraft
```

---

## Reboot Notifications

A little-known key of `crontab` is `@reboot`, and it can be used like this:

```bash
crontab -e
```

Add this on its own line:

```bash
@reboot /opt/discord/discord.sh "$(hostname)" "$(hostname) starting up..."
```

Now, whenever your Linux server starts up, you get a short message; this is good to get confirmation of a restart or a warning the power may have gone off.

## DDNS Updater

Often when self-hosting the problem is related to the ever-changing IP address at home. To get around this, I created a Cloudflare account, then set up the free DNS services and hosted a domain I own there. I then created a record called `home.<mydomain>` with IP address `1.2.3.4`.

Make sure with `nslookup` the IP address is visible and resolves:

```bash
nslookup home.<mydomain>
```

Should return the IP `1.2.3.4`.

In Cloudflare, click on your profile picture, then *Preferences*, then *API Tokens* and make a token that has **EDIT** rights to `<mydomain>` domain.

Install `jq` (varies by distro):

```bash
apt install jq
```

Get your zone ID from Cloudflare’s API:

```bash
curl -X GET "https://api.cloudflare.com/client/v4/zones?name=<mydomain>" \
     -H "Authorization: Bearer <cloudflare token>" \
     -H "Content-Type: application/json"
```

The output is 30- or 40-character alphanumerics; that is the `<zoneid>` for `<mydomain>`.

Create a script `/opt/ddns/ddns.sh`:

```bash
#!/bin/bash
# Don't forget to install the jq package

## keep these private
cloudflare_auth_key=<cloudflare token>

# Cloudflare zone is the zone which holds the record
dnsrecord=home.<mydomain>
zoneid=<zone id>

# Get the current external IP address
ip=$(curl -4 icanhazip.com)

#echo "Current IP is $ip"

if host $dnsrecord 1.1.1.1 | grep "has address" | grep "$ip"; then
  echo "$dnsrecord is currently set to $ip; no changes needed"
else
  /opt/discord/discord.sh "$(hostname)" "Cloudflare address for $dnsrecord should be $ip, I'll update the address..."

  # get the dns record id
  dnsrecordid=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$zoneid/dns_records?type=A&name=$dnsrecord" \
    -H "Authorization: Bearer $cloudflare_auth_key" \
    -H "Content-Type: application/json" | jq -r  '{"result"}[] | .[0] | .id')

  # update the record
  curl -s -X PUT "https://api.cloudflare.com/client/v4/zones/$zoneid/dns_records/$dnsrecordid" \
    -H "Authorization: Bearer $cloudflare_auth_key" \
    -H "Content-Type: application/json" \
    --data "{\"type\":\"A\",\"name\":\"$dnsrecord\",\"content\":\"$ip\",\"ttl\":1,\"proxied\":false}" | jq
fi
```

Make the file executable:

```bash
chmod 775 /opt/ddns/ddns.sh
```

The script checks the IPv4 address of the public interface against what is in Cloudflare and makes a change if needed. It also sends a Discord notice if a change was required.

I know my ISP resets the IP address every morning at 03:00 and I get a new one if the modem reboots for any reason, so this script can be added to `crontab` to run every 20 minutes:

```bash
crontab -e
```

Put this on a new line:

```bash
*/20 * * * * /opt/ddns/ddns.sh
```

You can test this by restarting your modem to get a new IP, then manually running the script. You should see `nslookup` returning your public IP after a few minutes and, of course, a Discord notification. You can also use the logic of the script to run another script in case some service needs to be restarted with an IP renewal, like a VPN service.

All the scripts above can be combined to make them monitor each other and provide some resilience. For example, you can use a modification of the port-monitoring script to check the DNS record and alert via Discord if a record does not return results.

Something else: I know not everybody is into AI, but for these short scripts most AIs are actually really good. Try this in Gemini:

> *I am a sysadmin looking after a server. I want a bash script that checks if a specific file has been changed in the last 10 minutes and return a 1 else 0.*