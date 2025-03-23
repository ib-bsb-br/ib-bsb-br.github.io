---
tags:
- scratchpad
info: aberto.
date: 2025-03-23
type: post
layout: post
published: true
slug: backing-up-windows-machines-using-rsync-and-ssh
title: Backing up Windows machines using rsync and ssh
comment: https://articles.manugarg.com/backup_rsync.html
---


Markdown Content:
Economical backup solution: rsync and ssh
-----------------------------------------

As all other unix tricks this is also the result of laziness and the need. I wanted to backup data on my windows laptop to a central linux/unix server. I didn't want all the features of available expensive backup solutions. Just a simple updated copy of my data on a central machine which is backed up to the tape daily. rsync is known for fast incremental transfer and was an obvious choice for the purpose.

We have a unix machine at our workplace which has a directory structure /backup/username allocated for backing up user data. rsync has a client/server architecture, where rsync client talks to an rsync daemon at the server side (This statement may not be completely true. I am not sure and don't care also. You can refer to rsync manpage for complete discussion over rsync.). rsync client can connect to rsync server directly or through other remote transport programs like rsh, ssh etc. I decided to use ssh for transport for security and simplicity.

rsync daemon requires a configuration file rsyncd.conf. For my use, I have set it up like this:

\[manu@amusbocldmon01 ~\]$ cat rsyncd.conf
use chroot = no
\[backup\]
        path = /backup
        read only = no
        comment = backup area

This says,

\-do no chroot (required because I'll run it as a non-root user)  
\-\[backup\] specifies a module named backup.  
\-/backup is the path to backup module on filesystem

That's all we need at the server side. We don't need to keep rsync deamon running on the server. We'll start rsync daemon from the client using ssh before starting the backup.

At Windows side, we need rsync and some ssh client. rsync is available for windows through cygwin port. You can download cygwin from [http://www.cygwin.com/](http://www.cygwin.com/). While installing cygwin, remember to select rsync. For ssh client, you can either use ssh that comes with cygwin or plink command line tool that comes with putty. Since, I have already set up my putty for password-less authentication using public/private key pair and pageant, I'll demonstrate this solution using plink. However you can use any other ssh client too. You can download putty and plink from [http://www.chiark.greenend.org.uk/~sgtatham/putty/.](http://www.chiark.greenend.org.uk/~sgtatham/putty/) You can find much information about ssh password less authentication on the web. To keep commands short, add rsync and plink to Windows path. Let's start our backup now.

First, we need to start rsync daemon at the server. It can be started from the client using following command:

plink -v -t -l manu fileserver.local.com rsync --daemon --port=1873 --config=$HOME/rsyncd.conf

where, fileserver.local.com is the central server where we are going to store our data. This logs in user 'manu' on fileserver and starts a rsync daemon there at the port 1873. rsync goes to the background and plink returns immediately.

Next we need to setup an ssh transport tunnel using plink:

plink -v -N -L 873:localhost:1873 -l manu fileserver.local.com

This sets up the local port forwarding -- forwarding local port 873 to port 1873 on the remote server.

After running this, we have port 873 on our windows box connected to the port 1873 on the fileserver on which rsync daemon is listening. So, now we just need to run rsync on windows machine with localhost as the target server:

rsync -av src 127.0.0.1::backup/manu

This command copies file or dir '`src`' incrementally to directory '`manu`' inside 'backup' module. Since this rsync is the one that comes with cygwin, it understand only cygwin paths for the files. For that reason, 'src' needs to be specified in cygwin terms. For example, `D:\project `becomes `/cygdrive/d/project` in cygwin terms.

Putting it all in scripts:
--------------------------

This trick is not much handy, unless you put it in the scripts and make it easy to run. To automate the process, I created 2 small scripts:

plink\_rsync.bat: (To start plink for rsync)

REM Start rsync daemon the server
plink -v -t %\* rsync --daemon --port=1873 --config=$HOME/rsyncd.conf
REM Setup ssh transport tunnel.
plink -v -N -L 873:localhost:1873 %\*

runrsync.bat: (Main script - calls plink\_rsync.bat and starts rsync)

REM Start plink\_rsync.bat
START /MIN "PLINK\_FOR\_RSYNC" plink\_rsync.bat -l manu fileserver.local.com
REM Sleep for 15 seconds to give plink enough time to finish
sleep 15
REM Iterate through filenames in filelist.txt and rsync them
for /F "delims=" %%i in (filelist.txt) do rsync -av %%i 127.0.0.1::backup/manu
REM Kill plink\_rsync.bat window
TASKKILL /T /F /FI "WINDOWTITLE eq PLINK\_FOR\_RSYNC \*"
REM Kill remote rsync daemon
plink -l manu fileserver.local.com pkill rsync

The main script starts `plink_rsync.bat` in another window and sleeps for 15 seconds to make sure that connection is set up. Then it runs rsync over the files and directories list in` filelist.txt`. After rsyncing is done, it kills `plink_rsync.bat` window and kills rsync daemon on the remote server by running pkill though plink.

filelist.txt contains the list of files and directories that you want to take backup of. For example, my `filelist.txt` contains:

filelist.txt:

"/cygdrive/d/Documents and Settings/501106700/My Documents/project"
"/cygdrive/d/Documents and Settings/501106700/My Documents/Outlook"
"/cygdrive/c/Program Files/Lotus/Sametime Client/Chat Transcripts"

You can schedule runrsync.bat to run everyday or every week depending on your requirement.