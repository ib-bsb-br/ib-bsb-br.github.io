---
title: Alternative option to upload a file to GitHub without cloning the entire repository
date: 2023-12-24 01:00:00 -02:00
categories:
- Tutorial
tags:
- linux
comment: 
info: aberto.
type: post
layout: post
---

1. **Initialize an empty Git repository**:

   ```shell

   git init my-repository
   cd my-repository

   ```

2. **Add a remote for the GitHub repository**:

   ```shell

   git remote add origin https://github.com/marioseixas/marioseixas.github.io.git

   ```

3. **Configure sparse-checkout**:

   ```shell

   git config core.sparseCheckout true

   ```

4. **Specify the directory you want to checkout** (if applicable):

   ```shell

   echo '_posts/*' >> .git/info/sparse-checkout

   ```

5. **Fetch the main branch** (change 'main' to your target branch if it's named differently):

   ```shell

   git fetch origin main

   ```

6. **Checkout the files**:

   ```shell

   git checkout main

   ```

Git could ask for your GitHub credentials:

- [Generating SSH key](https://docs.github.com/pt/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

- [Managing DEPLOY keys](https://docs.github.com/pt/authentication/connecting-to-github-with-ssh/managing-deploy-keys)

To set up your credentials with SSH for Git on your local machine after generating an SSH key and adding it to your GitHub account, follow these steps:

1. **Ensure SSH Agent is Running**:

   You need to make sure the SSH agent is running so that it can manage your keys. You seem to have already started the ssh-agent and added your key. If needed again, you can use:

   ```shell

   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519

   ```

2. **Test Your SSH Connection**:

   Before you try to push your changes to GitHub, you should test your SSH connection. You can do this with the following command:

   ```shell

   ssh -T git@github.com

   ```

   You should see a message like "Hi username! You've successfully authenticated...".

3. **Configure Git to Use SSH**:

   If you haven't already set Git to use SSH for GitHub, you can do so by changing your remote URL from HTTPS to SSH. Since you just added a deploy key for a specific repository, it's tied to that repository only. The general command to change the remote URL is:

   ```shell

   git remote set-url origin git@github.com:username/repository.git

   ```

   Replace `username` with your GitHub username and `repository.git` with your repository's name.

4. **Pushing Changes to GitHub**:

   When you push changes, Git will use your SSH key for authentication. Because you've added the key to the SSH agent, you should not be prompted for your passphrase again during the current session.

   ```shell

   git push origin main

   ```

**Important Note**: Since you used a deploy key you showed in the example, and if you have set it up in the GitHub repository correctly, you can push to the repository as the key has read/write access. You must ensure that your Git remote URL uses the SSH format.
