---
tags: [scratchpad]
info: aberto.
date: 2025-05-15
type: post
layout: post
published: true
slug: github-actions-build-workflow-locally-on-a-debian
title: 'GitHub Actions Build Workflow Locally on a Debian'
---
**Goal:** To build the OS images and related artifacts as specified in the workflow, using a Debian-based environment like Finnix.

**Assumed Environment:**
*   A running Debian-based Linux distribution (e.g., Finnix booted, or a standard Debian/Ubuntu desktop/server). This guide assumes your distribution is reasonably compatible with Debian 12 (Bullseye), as the workflow specifies `image-debian-12`.
*   Internet connectivity (for downloading packages and tools).
*   `sudo` privileges.

---

### 1. Prerequisites & Initial Setup

Before starting the build, ensure your system and environment are ready.

**a. Resource Requirements:**
The original GitHub Actions workflow specifies `runs-on` parameters that suggest the following minimum resources. Ensure your local machine or VM has:
*   **CPU:** At least 4 cores.
*   **Memory (RAM):** At least 4 GB.
*   **Disk Space:** At least 100 GB free, especially in your build directory and system partitions like `/tmp` and `/var`.

**b. System Update (Recommended):**
Open a terminal and update your package lists:
```bash
sudo apt-get update
```
*(On a fresh Finnix boot, this might be less critical but is good practice on persistent systems.)*

**c. Install Essential Tools:**
Some tools might already be present, especially on Finnix, but ensure they are installed:
```bash
sudo apt-get install -y git curl ca-certificates gnupg
```

**d. Clone Your Repository:**
If you haven't already, clone the repository containing the workflow and the source code.
```bash
git clone <your-repository-url>
cd <your-repository-name>
```
Replace `<your-repository-url>` and `<your-repository-name>` with your actual repository details.

**e. Checkout the Target Tag:**
The workflow triggers on any tag push (`on: push: tags: - '*'`). To reproduce a build for a specific tag (e.g., `v1.2.3`), check it out:
```bash
# Replace v1.2.3 with your actual tag
export TARGET_TAG="v1.2.3"
git checkout tags/${TARGET_TAG} -b build-${TARGET_TAG}
```
This creates a local branch `build-${TARGET_TAG}` based on the tag.

**f. Define the Tag Name Environment Variable:**
The workflow uses `github.ref_name` for the tag. We'll simulate this:
```bash
export GITHUB_REF_NAME="${TARGET_TAG}"
echo "Building for tag: ${GITHUB_REF_NAME}"
```

---

### 2. Installing Build Tools and Dependencies

This section mirrors the setup steps from your GitHub Actions workflow.

**a. Install Go:**
The workflow uses `actions/setup-go@v5` with `go-version: stable`.
```bash
sudo apt-get install -y golang-go
# Verify installation (optional)
go version
```
For most "stable" use cases, the version of Go provided by Debian's repositories should suffice.

**b. Repository Permissions (Conditional):**
The workflow runs `sudo chown -R $(id -u):$(id -g) .`. This is often for GitHub Actions runner environments. Locally, if you cloned as your user and manage `sudo` appropriately, you might not need this. If you encounter permission errors during `make` or `mkosi` operations related to file ownership *within your working directory*, you might revisit this. Generally, proceed without it first.

**c. Install Core Build Dependencies:**
These are the packages listed in the workflow.
```bash
sudo apt-get install --yes \
    binutils \
    debian-archive-keyring \
    devscripts \
    make \
    parted \
    pipx \
    qemu-utils
```

**d. Setup Incus (Daily Build):**
The workflow uses a script to get daily builds of Incus.
```bash
echo "Setting up Incus (daily build)..."
curl https://pkgs.zabbly.com/get/incus-daily | sudo sh

# The script above should handle repository setup and installation.
# The workflow then initializes Incus and sets socket permissions.
sudo incus admin init --auto

# The workflow uses 'sudo chmod 666 /var/lib/incus/unix.socket'.
# This makes the socket world-writable, which is generally not recommended for production.
# A better long-term approach is to add your user to the 'incus' group:
#   sudo usermod -a -G incus $USER
#   # Then log out and back in, or start a new shell: newgrp incus
# This allows running 'incus' commands without sudo.
# For immediate effect in the current script, or if not adding user to group,
# the chmod command from the workflow can be used, but be aware of its implications.
sudo chmod 666 /var/lib/incus/unix.socket # As per workflow; consider security implications

# Verify Incus (you might need sudo if group membership isn't active yet or chmod wasn't run)
incus list
# If 'incus list' fails due to permissions and you haven't run chmod 666, try: sudo incus list
```

**e. Setup mkosi:**
`mkosi` is installed using `pipx` from a specific git commit.
```bash
pipx install git+https://github.com/systemd/mkosi.git@v25.3

# IMPORTANT: Understanding PATH for mkosi and sudo
# pipx installs applications to $HOME/.local/bin by default for the current user.
# Add this to your PATH for the current session if it's not already configured in your .bashrc/.zshrc:
export PATH="${HOME}/.local/bin:${PATH}"
echo "Make sure $HOME/.local/bin is in your PATH. Current PATH: $PATH"

# Verify mkosi installation
mkosi --version
```
If `pipx` prompts you to run `pipx ensurepath`, do so, and it might require opening a new terminal or sourcing your shell's profile file (`.bashrc`, `.zshrc`, etc.).

---

### 3. Configuring for the Build

Prepare files and environment variables specific to this build.

**a. Create `mkosi.version` File:**
This file stores the version (tag name) for the build.
```bash
echo "${GITHUB_REF_NAME}" > mkosi.version
cat mkosi.version # Verify content
```

**b. Handle Secrets (`mkosi.crt`, `mkosi.key`):**
The workflow uses GitHub secrets `secrets.SB_CERT` and `secrets.SB_KEY`. You must provide these files locally. **These are sensitive files; handle them securely.**
Create `mkosi.crt` and `mkosi.key` in your repository root with the *actual certificate and private key content*.
```bash
# Example: Replace placeholder content with your actual secrets.
echo "---BEGIN CERTIFICATE---
This is a placeholder for your SB_CERT.
Replace this with the actual certificate content.
---END CERTIFICATE---" > mkosi.crt
chmod 644 mkosi.crt

echo "---BEGIN PRIVATE KEY---
This is a placeholder for your SB_KEY.
Replace this with the actual private key content.
---END PRIVATE KEY---" > mkosi.key
chmod 600 mkosi.key # Restrict permissions for the private key

echo "IMPORTANT: Placeholder mkosi.crt and mkosi.key created. REPLACE with actual content."
```

---

### 4. Executing the Build

This is where `mkosi` and your `Makefile` perform the image creation.

**a. Run the Main Build Command:**
The workflow uses `make build-iso`. This assumes your `Makefile` has this target.
```bash
# The original workflow exports PATH="${PATH}:/root/.local/bin".
# This implies 'pipx install' might have been run as root, or the runner's $HOME is /root.
# Since we installed mkosi as the current user (via pipx to $HOME/.local/bin),
# and 'make build-iso' might invoke 'mkosi' which often requires root privileges
# for operations like mounting filesystems, you'll likely need to run 'make' with sudo.
#
# Using 'sudo -E' is crucial here:
# -E preserves the existing environment variables, including:
#   1. GITHUB_REF_NAME: Needed by your build scripts.
#   2. PATH: Ensures sudo can find 'mkosi' from $HOME/.local/bin (of the user who ran export).

echo "Running the build via 'sudo -E make build-iso'..."
sudo -E make build-iso
```

**b. Troubleshooting Build Failures:**
If the build fails:
*   **Examine `make` output:** Look for the first error message.
*   **`mkosi` logs:** `mkosi` often creates detailed logs. Check for logs inside the `mkosi.output/` directory or its subdirectories (e.g., `mkosi.output/*.log`, `mkosi.output/build-*/`).
*   **Verbose `make`:** If your `Makefile` supports it, try: `sudo -E make build-iso VERBOSE=1` (or similar flags like `V=1`) for more detailed command output.
*   **Incus issues:** If `mkosi` uses Incus containers for the build:
    *   Check container status: `sudo incus list`
    *   View container logs: `sudo incus logs <container_name_shown_in_list_or_mkosi_output>`
*   **Permissions:** Ensure `sudo -E` was used. Double-check file permissions for scripts or configuration files used by `make` or `mkosi`.
*   **Dependencies:** Verify all packages from step 2.c were installed successfully.

**c. Organize Output Files:**
After a successful build, `mkosi` places output files (typically in `mkosi.output/`). The workflow then moves these.
```bash
mkdir -p upload
echo "Moving build artifacts to 'upload/' directory..."

# Adjust these mv commands if your output filenames differ based on mkosi config or GITHUB_REF_NAME.
# The glob patterns like *.usr-x86-64.* should handle variations.
mv mkosi.output/debug.raw upload/
mv mkosi.output/incus.raw upload/

mv mkosi.output/IncusOS_${GITHUB_REF_NAME}.raw upload/IncusOS_${GITHUB_REF_NAME}.img
mv mkosi.output/IncusOS_${GITHUB_REF_NAME}.iso upload/IncusOS_${GITHUB_REF_NAME}.iso
mv mkosi.output/IncusOS_${GITHUB_REF_NAME}.efi upload/
mv mkosi.output/IncusOS_${GITHUB_REF_NAME}.usr-x86-64.* upload/
mv mkosi.output/IncusOS_${GITHUB_REF_NAME}.usr-x86-64-verity.* upload/
mv mkosi.output/IncusOS_${GITHUB_REF_NAME}.usr-x86-64-verity-sig.* upload/

echo "Files moved to 'upload/' directory:"
ls -lh upload/
```
If files are missing, review the build logs from `make build-iso` to see what `mkosi` actually produced in `mkosi.output/`.

---

### 5. Compressing the Artifacts

The workflow compresses the built files using `gzip`.
```bash
# Install gzip if not already present
sudo apt-get install -y gzip

echo "Compressing files in 'upload/' directory..."
cd upload
for i in *; do
  if [ -f "${i}" ]; then # Check if it's a regular file
    echo "Compressing ${i}..."
    gzip -9 "${i}"
  fi
done
cd .. # Return to repository root

echo "Compressed files in 'upload/' directory:"
ls -lh upload/
```

---

### 6. Managing Build Artifacts (Local "Release")

The GitHub Actions workflow uploads these compressed files to a GitHub Release. Locally, your "release" artifacts are in the `upload/` directory.

You can:
*   Copy them to another location for testing or distribution.
*   Optionally, create an actual GitHub Release from your local machine using the GitHub CLI (`gh`):
    1.  **Install GitHub CLI:** (If not already installed. Instructions at [cli.github.com](https://cli.github.com/))
        ```bash
        # Example for Debian/Ubuntu:
        type -p curl >/dev/null || sudo apt install curl -y
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
        && sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
        && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
        && sudo apt update \
        && sudo apt install gh -y
        ```
    2.  **Authenticate `gh` CLI:**
        ```bash
        gh auth login
        ```
    3.  **Create Release and Upload Files:**
        ```bash
        # Ensure you are in the root of your repository directory
        gh release create "${GITHUB_REF_NAME}" ./upload/* --title "Release ${GITHUB_REF_NAME}" --notes "Locally built release for ${GITHUB_REF_NAME}"
        ```

---

### 7. Important Considerations

*   **`Makefile` and `mkosi` Configurations:** This tutorial heavily relies on your project's `Makefile` (with the `build-iso` target) and `mkosi` configuration files (`mkosi.conf`, `mkosi.local.conf`, `mkosi.conf.d/*`, `mkosi.build` scripts) being correct and present in your repository.
*   **Root Privileges (`sudo -E`):** Be mindful of commands requiring `sudo`. Using `sudo -E` is critical for `make build-iso` to ensure it inherits necessary environment variables like your modified `PATH` (for `mkosi`) and `GITHUB_REF_NAME`.
*   **Environment Differences:** A local environment will always have subtle differences from a GitHub Actions runner.
*   **Finnix Specifics:** If using Finnix, remember its live nature means installed packages or system changes are typically not persistent across reboots unless you've configured persistence. For a single build session, this is usually fine.
*   **Clean Builds:** For truly reproducible builds, consider cleaning previous build outputs (e.g., `mkosi.output/`, `upload/`) before starting a new build. Your `Makefile` might have a `clean` target: `sudo -E make clean`.
*   **Resource Intensive:** OS image building can be very demanding on CPU, RAM, and disk I/O.
*   **Alternative: Containerized Builds:** For higher fidelity reproduction and isolation, consider running the entire build process within a Docker or Podman container based on a `debian:12` image. This is more complex to set up but offers a cleaner environment.

---