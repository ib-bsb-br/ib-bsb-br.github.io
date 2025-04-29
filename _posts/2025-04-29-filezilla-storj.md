---
tags:
- scratchpad
info: aberto.
date: 2025-04-29
type: post
layout: post
published: true
slug: filezilla-storj
title: FileZilla Native Integration to Storj
comment: https://storj.dev/dcs/third-party-tools/filezilla/filezilla-native
---


Markdown Content:
This guide walks users through the process of setting up FileZilla to transfer files over Storj.

This is the only integration available for the **free version of Filezilla**. If you wish to use the Hosted Gateway MT you will need the [FileZilla Pro Integration](https://storj.dev/dcs/third-party-tools/filezilla/filezilla-pro)

The **\_ FileZilla\_** Client is a fast and reliable cross-platform (Windows, Linux, and Mac OS X) FTP, FTPS, and SFTP client with many useful features and an intuitive graphical user interface.

It includes a site manager to store all your connection details and logins, as well as an Explorer-style interface that shows the local and remote folders and can be customized independently.

With the launch of the native Storj Integration into the FileZilla client, developers can use the client configured to transfer files point-to-point using the decentralized cloud.

[![Image 1: Getting Started Guide to Configure Storj with Filezilla](https://link.storjshare.io/raw/jua7rls6hkx5556qfcmhrqed2tfa/docs/images/A3axDH9IIHl-G8gI--gjT_fz.png)](https://link.storjshare.io/raw/jua7rls6hkx5556qfcmhrqed2tfa/docs/images/A3axDH9IIHl-G8gI--gjT_fz.png)

A Storj access grant is a serialized, self-contained credential that allows users to access a specific bucket, or object, within a Storj project. It encapsulates everything needed for authentication and authorization on the Storj network.

Create Access Grant in the Storj Console:

1.  Navigate to **Access Keys** on the left side menu.
    
2.  Click the **New Access Key** button.
    
3.  When the New Access dialog comes up, set specifications according to the following guidelines:
    
    *   **Name:** The name of the credentials (e.g. my-access-grant)
    *   **Type:** Access Grant
4.  Click **Next** to provide permissions, either Full Access or Advanced:
    
    *   **Permissions:** All
        
    *   **Buckets:** Feel free to specify the bucket (e.g. my-bucket), or leave as “All”
        
    *   **End date**: provide an expiration date for these credentials (optional)
        
5.  Click **Next** to provide Access encryption Information (Skip this section if you have opted into [Storj-managed passphrases](https://storj.dev/learn/concepts/encryption-key/storj-vs-user-managed-encryption) for the project)
    
    In order to see the data uploaded to your bucket in the web console, you must unlock the bucket with the same encryption passphrase as the credentials.
    
    *   **Use the current passphrase**: this is default option
        
    *   **Advanced**: you may provide a different encryption phrase either your own or generate a new one.
        
        *   **Enter a new passphrase**: use this option, if you would like to provide your own new encryption phrase
            
        *   **Generate 12-word passphrase**: use this option, if you would like to generate a new encryption phrase
            

**This passphrase is important!** Encryption keys derived from it are used to encrypt your data at rest, and your data will have to be re-uploaded if you want it to change!

Importantly, if you want two access grants to have access to the same data, **they must use the same passphrase**. You won't be able to access your data if the passphrase in your access grant is different than the passphrase you uploaded the data with.

Please note that **Storj does not know or store your encryption passphrase**, so if you lose it, you will not be able to recover your files.

6.  Click **Create Access** to finish creation of your Access key.
    
7.  Click **Confirm** the Confirm details pop-up message
    
8.  Your Access Grant is created. Write it down and store it, or click the **Download** button. You will need the Access Grant for the following steps.
    

To download the latest release of FileZilla, navigate to [https://filezilla-project.org/download.php?show\_all=1](https://filezilla-project.org/download.php?show_all=1) and select the version appropriate for your operating system, then install FileZilla.

### [Creating a new Site](https://storj.dev/dcs/third-party-tools/filezilla/filezilla-native#creating-a-new-site)

Open the Site Manager by clicking on the leftmost icon.

[![Image 2](https://link.storjshare.io/raw/jua7rls6hkx5556qfcmhrqed2tfa/docs/images/ptIx46T-1UVKXUjFN4ogP_filezilla1.png)](https://link.storjshare.io/raw/jua7rls6hkx5556qfcmhrqed2tfa/docs/images/ptIx46T-1UVKXUjFN4ogP_filezilla1.png)

Select the 'New Site' option

[![Image 3](https://link.storjshare.io/raw/jua7rls6hkx5556qfcmhrqed2tfa/docs/images/R_IRpQKcgfDIUbxsBnW7d_image.png)](https://link.storjshare.io/raw/jua7rls6hkx5556qfcmhrqed2tfa/docs/images/R_IRpQKcgfDIUbxsBnW7d_image.png)

### [Configure the Satellite and Access Grant](https://storj.dev/dcs/third-party-tools/filezilla/filezilla-native#configure-the-satellite-and-access-grant)

Next, select Protocol: "Storj - Decentralized Cloud Storage" from the Protocol dropdown in the "General" tab.

Now enter the **Satellite** and **Access Grant** as shown below (Entering the port is not required)

1.  Use the **Satellite** URL from which you created the Access Grant.
    
2.  For **Access Grant** please enter the Access Grant you saved above.
    

[![Image 4](https://link.storjshare.io/raw/jua7rls6hkx5556qfcmhrqed2tfa/docs/images/QfVDo6-BAPCOq85iJqWEJ_image.png)](https://link.storjshare.io/raw/jua7rls6hkx5556qfcmhrqed2tfa/docs/images/QfVDo6-BAPCOq85iJqWEJ_image.png)

After you enter the above information, hit the "Connect" button, and FileZilla will connect directly to the remote site. You should see a screen showing your local site vs. Storj, like so:

[![Image 5](https://link.storjshare.io/raw/jua7rls6hkx5556qfcmhrqed2tfa/docs/images/LKG7hFgbpmSQUM5Ps8GIh_filezilla2.png)](https://link.storjshare.io/raw/jua7rls6hkx5556qfcmhrqed2tfa/docs/images/LKG7hFgbpmSQUM5Ps8GIh_filezilla2.png)

### [Uploading a File](https://storj.dev/dcs/third-party-tools/filezilla/filezilla-native#uploading-a-file)

To upload a file to your local machine, simply drag it from the local to the remote site (on the decentralized cloud), as shown below:

[![Image 6](https://link.storjshare.io/raw/jua7rls6hkx5556qfcmhrqed2tfa/docs/images/yC9FAbglEVJ3Ps7eL4Eik_filezilla3.gif)](https://link.storjshare.io/raw/jua7rls6hkx5556qfcmhrqed2tfa/docs/images/yC9FAbglEVJ3Ps7eL4Eik_filezilla3.gif)

### [Downloading a File](https://storj.dev/dcs/third-party-tools/filezilla/filezilla-native#downloading-a-file)

To download a file to your local machine, simply drag it from the remote site to the local site, as shown below:

[![Image 7](https://link.storjshare.io/raw/jua7rls6hkx5556qfcmhrqed2tfa/docs/images/TvSrHNg6pSIvsXyeKGm2A_filezilla4.gif)](https://link.storjshare.io/raw/jua7rls6hkx5556qfcmhrqed2tfa/docs/images/TvSrHNg6pSIvsXyeKGm2A_filezilla4.gif)