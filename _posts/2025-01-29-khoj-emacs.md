---
tags: software
info: aberto.
date: 2025-01-29
type: post
layout: post
published: true
slug: khoj-emacs
title: 'KHOJ Emacs'
---
### **Step 1: Install Emacs**

**For Linux:**

- Open your terminal and run:
  - **Debian/Ubuntu:** `sudo apt-get install emacs`
  - **Fedora:** `sudo dnf install emacs`
  - **Arch Linux:** `sudo pacman -S emacs`

**For macOS:**

- If you have Homebrew installed, run:
  - `brew install emacs`
- Or download Emacs directly from [emacsformacosx.com](https://emacsformacosx.com/).

**For Windows:**

- Download the installer from the [GNU Emacs website](https://www.gnu.org/software/emacs/download.html#windows).
- Run the installer and follow the prompts.

---

### **Step 2: Get Your Khoj API Key**

1. **Sign Up or Log In:**

   - Go to [Khoj.ai](https://khoj.ai/) and create an account or log in.

2. **Access the Web App:**

   - Navigate to the [Khoj Web App](https://app.khoj.dev/).

3. **Generate an API Key:**

   - Click on your profile or settings.
   - Find the **API Keys** section.
   - Generate a new API key.
   - **Important:** Copy and save this API key—you'll need it soon.

---

### **Step 3: Set Up Your Emacs Configuration**

We'll create a minimal configuration file to set up Khoj in Emacs.

**Locate or Create the Emacs Init File (`init.el`):**

- **On Linux/macOS:**

  - The file is typically located at `~/.emacs.d/init.el`.
  - If it doesn't exist, you can create it:
    - Open a terminal.
    - Run `mkdir -p ~/.emacs.d` to ensure the directory exists.
    - Run `touch ~/.emacs.d/init.el` to create the file.

- **On Windows:**

  - The file may be located at `C:\Users\YourUsername\AppData\Roaming\.emacs.d\init.el`.
  - You might need to enable viewing hidden files to see the AppData folder.
  - Create the `.emacs.d` folder and `init.el` file if they don't exist.

**Edit `init.el`:**

Open `init.el` in Emacs or any text editor and add the following content:

```emacs-lisp
;;; Minimal init.el for using Khoj

;; 1. Initialize package sources
(require 'package)
(setq package-archives
      '(("gnu" . "https://elpa.gnu.org/packages/")
        ("melpa-stable" . "https://stable.melpa.org/packages/")))
(package-initialize)

;; 2. Install use-package if it's not already installed
(unless (package-installed-p 'use-package)
  (unless package-archive-contents
    (package-refresh-contents))
  (package-install 'use-package))
(require 'use-package)
(setq use-package-always-ensure t)

;; 3. Install and configure Khoj
(use-package khoj
  :pin melpa-stable
  :bind ("C-c s" . khoj)  ;; Press Ctrl+c then s to open Khoj
  :config
  (setq khoj-api-key "YOUR_KHOJ_API_KEY"  ;; Replace with your API key
        khoj-server-url "https://app.khoj.dev"))
```

**Replace `YOUR_KHOJ_API_KEY` with the API key you obtained earlier.**

---

### **Step 4: Start Emacs and Install Khoj**

1. **Launch Emacs:**

   - Open Emacs as you normally would (e.g., by clicking its icon or running `emacs` in the terminal).

2. **Allow Packages to Install:**

   - Emacs will read your `init.el` file and start installing the packages specified (`use-package` and `khoj`).
   - This may take a few minutes depending on your internet connection.
   - You can monitor the installation progress in the `*Messages*` buffer or the minibuffer at the bottom.

3. **Restart Emacs (Recommended):**

   - After installation completes, it's a good idea to restart Emacs to ensure all settings take effect.

---

### **Step 5: Use Khoj in Emacs**

**Access the Khoj Interface:**

- Press `Ctrl + c` then `s` (`C-c s`) to open the Khoj menu.
- Alternatively, you can use `M-x khoj` (press `Alt + x`, then type `khoj`, and press `Enter`).

**Perform a Search:**

1. After opening Khoj, press `s` for search.
2. Type your query in natural language, for example:
   - "What meetings do I have next week?"
3. Press `Enter` to see search results from your notes.

**Start a Chat Session:**

1. Open Khoj (`C-c s`), then press `c` for chat.
2. Ask a question or start a conversation, such as:
   - "Summarize my notes on project X."
3. Khoj will provide responses based on your data.

---

### **Tips to Keep Things Simple**

- **Avoid Overloading Emacs:**

  - Stick to this minimal setup to prevent getting overwhelmed.
  - Refrain from adding extra plugins or configurations until you're comfortable.

- **Learn Gradually:**

  - Familiarize yourself with basic Emacs commands.
  - Use `C-h t` (Ctrl + h, then t) to access the Emacs tutorial.
  - Remember that it's okay to take it slow.

- **Get Help When Needed:**

  - Consult the [Khoj Documentation](https://docs.khoj.dev/clients/emacs) for more details.
  - Join communities or forums if you have questions.

---

**You're all set!**

With this minimal configuration, you can now use Khoj within Emacs without the complexity. Enjoy exploring your notes and leveraging Khoj's powerful features in a simplified environment.