---
categories: []
tags:
  - scratchpad
comment: 
info: 
date: '2026-01-21'
type: post
layout: post
published: true
sha: 7f5c7931780b23cbed61d78f2ab143eff11e617a
slug: logs-rotation_deb
title: 'rotation + compression + size caps in logrotate/rsyslog on Debian'
---
You want two layers: (1) rotate/compress aggressively enough, and (2) reduce the log volume at the source.

C1) Strengthen logrotate policy for syslog + daemon.log
Edit `/etc/logrotate.d/rsyslog` and ensure both files are covered with:

* compression enabled
* a retention count (rotate N)
* a size cap (`maxsize` or `size`)
* a postrotate hook that reopens logs via the rsyslog helper (or HUP)

Example policy (conservative, “stop the bleeding”):

* rotate daily
* keep 14 rotations
* compress, with delaycompress
* rotate early if it exceeds 100 MB

Conceptually:

* `maxsize` is useful when you still want a time schedule (daily) but also want rotation triggered by size.
* `size` is similar but is mutually exclusive with time intervals and rotates purely based on size. ([Linux Die][8])

Important operational detail: size-based triggers only take effect when logrotate runs. If logrotate runs once per day, “maxsize 100M” will only be checked once per day, and a runaway log can still grow very large within that day. This is why the logrotate docs note you must run it more frequently (e.g., hourly) if you truly need small, frequent rotations. ([man7.org][9])

C2) If growth is extreme, run logrotate more frequently
If you’re seeing multi-GB growth in hours, consider executing logrotate hourly via a systemd timer override or a cron.hourly job. The key idea is not distro-specific: logrotate must be invoked more frequently to enforce frequent size-based rotation. ([man7.org][9])

D. Reduce the log volume: find what’s flooding syslog/daemon.log
Rotation is containment; the real fix is stopping the spammer.

1. Identify top “talkers” (fast triage)

* Count by program tag (approximate, but often enough to find the culprit):

  * `sudo awk '{print $5}' /var/log/syslog | sed 's/\[.*\]://' | sort | uniq -c | sort -nr | head -30`
* Then inspect that program’s last messages:

  * `sudo grep -F 'programname' /var/log/syslog | tail -n 200`
    Do the same for `/var/log/daemon.log`.

2. Confirm if a single repeating line is exploding volume

* Quickly spot repetition:

  * `sudo tail -n 5000 /var/log/syslog | sort | uniq -c | sort -nr | head -20`

3. Fix at the source
   Typical “log floods” come from:

* a failing service retry-loop (network DNS failures, storage errors, authentication failures, crashing + systemd restart loops)
* debug logging accidentally enabled
* hardware/driver chatter (kernel/udev messages routed onward)
  The correct fix depends on the service you find; but once you identify the top talker, you almost always have a direct knob: reduce log level or fix the underlying error condition.

4. Consider rsyslog repeated-message reduction only with eyes open
   rsyslog supports “Last line repeated n times” behavior via `$RepeatedMsgReduction`. Upstream docs describe it as legacy and many modern workflows consider it a misfeature because it can hide event granularity that tools expect. ([GitHub][5])
   So treat this as a last resort for purely identical spam where you accept the loss of detail.

E. Optional: ensure systemd-journald isn’t also consuming disk
Even if `/var/log/syslog` is your main problem, Debian systems also keep the systemd journal, and it has configurable disk caps like `SystemMaxUse=` / `RuntimeMaxUse=`. ([Debian Sources][4])

* Check usage: `journalctl --disk-usage`
* If needed, cap retention via `/etc/systemd/journald.conf` and vacuum old entries.

# /etc/logrotate.d/rsyslog
{% codeblock %}
/var/log/syslog
/var/log/daemon.log
/var/log/kern.log
/var/log/auth.log
/var/log/messages
{
	# Rotate these frequently to prevent multi-GB growth
	hourly

	# Keep up to 7 days of hourly history (24*7 = 168)
	rotate 168
	maxage 7

	missingok
	notifempty

	# Size guardrails:
	# - minsize prevents rotating tiny files every hour
	# - maxsize forces rotation at next run even if time interval hasn't elapsed
	minsize 1M
	maxsize 50M

	compress
	delaycompress

	# Hour-stamped rotated filenames (avoids collisions with hourly)
	dateext
	dateformat -%Y%m%d-%H
	datehourago

	sharedscripts
	postrotate
		/usr/lib/rsyslog/rsyslog-rotate
	endscript
}

/var/log/mail.info
/var/log/mail.warn
/var/log/mail.err
/var/log/mail.log
/var/log/user.log
/var/log/lpr.log
/var/log/cron.log
/var/log/debug
{
	# These typically don't need hourly rotation; still protected by size caps.
	daily

	# Keep ~30 days
	rotate 30
	maxage 30

	missingok
	notifempty

	minsize 100k
	maxsize 20M

	compress
	delaycompress

	dateext
	sharedscripts
	postrotate
		/usr/lib/rsyslog/rsyslog-rotate
	endscript
}
{% endcodeblock %}

Why this structure works:

* `hourly` is a real directive in bullseye logrotate. ([manpages.debian.org][1])
* `minsize`/`maxsize` behave exactly the way you want for “don’t rotate tiny files, but never let them explode”. ([manpages.debian.org][1])
* `dateext` + an hour-bearing `dateformat` + `datehourago` prevents name collisions and makes the timestamp match the hour the logs cover. ([manpages.debian.org][1])

## Make logrotate actually run hourly (required)

Logrotate configs don’t schedule themselves. You must run logrotate hourly via **systemd timer** or **cron**.

# systemd timer (cleanest if you have it)

Check if it exists:

```bash
systemctl status logrotate.timer 2>/dev/null
systemctl list-timers | grep -i logrotate || true
```

If `logrotate.timer` exists, override it to hourly. The important trick is: when overriding `OnCalendar=`, you should first reset it by assigning an empty value (systemd supports “empty string resets the list”). ([manpages.debian.org][3])

```bash
sudo systemctl edit logrotate.timer
```

Put this in the editor:

```ini
[Timer]
OnCalendar=
OnCalendar=hourly
Persistent=true
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl restart logrotate.timer
systemctl list-timers logrotate.timer
```

## Validate safely

Dry-run the specific policy:

```bash
sudo logrotate -d /etc/logrotate.d/rsyslog
```

Force one rotation to confirm naming/permissions (do this once, not repeatedly):

```bash
sudo logrotate -f /etc/logrotate.d/rsyslog
```

Watch whether the files stop ballooning:

```bash
ls -lh /var/log/syslog /var/log/daemon.log
```

One pragmatic warning: hourly rotation + very noisy logs can still generate lots of compressed archives. If that happens, tighten `maxage` (e.g., 3) or reduce `rotate`, or increase compression aggressiveness later.