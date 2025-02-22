---
tags: [linux>dotfile]
info: aberto.
date: 2024-11-05
type: post
layout: post
published: true
slug: performance-governors
title: 'performance_governors.sh'
---

First, remove the init.d script registration: `sudo update-rc.d performance_governors.sh remove`

Create a systemd service file: `sudo nano /etc/systemd/system/performance_governors.service`

Add this content:

{% codeblock %}
[Unit]
Description=Set CPU and GPU governor to performance
After=multi-user.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/etc/init.d/performance_governors.sh start
ExecStop=/etc/init.d/performance_governors.sh stop

[Install]
WantedBy=multi-user.target
Reload systemd to recognize the new service:
sudo systemctl daemon-reload

{% endcodeblock %}

Reload systemd to recognize the new service: `sudo systemctl daemon-reload`

Enable and start the service:
`sudo systemctl enable performance_governors`
`sudo systemctl start performance_governors`

Check the status: `sudo systemctl status performance_governors`

{% codeblock bash %}

#!/bin/bash
### BEGIN INIT INFO
# Provides:          performance_governors
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: CPU Performance Governors
# Description:       Script to manage CPU performance governor settings for RK3588
### END INIT INFO

# Source function library
. /lib/lsb/init-functions

# Path to the log file
LOG="/var/log/performance_governors.log"

# Function to write to log
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG"
}

# Function to set governor
set_governor() {
    local path="$1"
    if [ -f "$path" ]; then
        echo performance > "$path" 2>/dev/null
        if [ $? -eq 0 ]; then
            log_message "Successfully set performance governor for $path"
            return 0
        else
            log_message "Failed to set performance governor for $path"
            return 1
        fi
    else
        log_message "Path does not exist: $path"
        return 1
    fi
}

# Function to start the service
do_start() {
    log_message "Starting performance governors"
    
    local governors=(
        "/sys/class/devfreq/fb000000.gpu/governor"
        "/sys/devices/system/cpu/cpufreq/policy0/scaling_governor"
        "/sys/devices/system/cpu/cpufreq/policy4/scaling_governor"
        "/sys/devices/system/cpu/cpufreq/policy6/scaling_governor"
        "/sys/class/devfreq/dmc/governor"
        "/sys/class/devfreq/fdab0000.npu/governor"
    )
    
    local failed=0
    for governor in "${governors[@]}"; do
        set_governor "$governor" || failed=1
    done
    
    if [ $failed -eq 0 ]; then
        log_message "All performance governors set successfully"
        return 0
    else
        log_message "Some governors failed to set"
        return 1
    fi
}

# Function to stop the service (reset to default)
do_stop() {
    log_message "Stopping performance governors (resetting to default)"
    return 0
}

# Function to check status
do_status() {
    local failed=0
    for governor in /sys/devices/system/cpu/cpufreq/policy*/scaling_governor; do
        if [ -f "$governor" ]; then
            current=$(cat "$governor")
            echo "Current governor for $governor: $current"
            [ "$current" != "performance" ] && failed=1
        fi
    done
    return $failed
}

# Main script logic
case "$1" in
    start)
        do_start
        ;;
    stop)
        do_stop
        ;;
    restart)
        do_stop
        do_start
        ;;
    status)
        do_status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit $?

{% endcodeblock %}
