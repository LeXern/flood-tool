# Troubleshooting: Setup & Dependency Issues

If you encounter errors during the setup process, find the relevant section below.

## 1. "Poetry is not recognized" or "Command Not Found"

If you get an error saying `poetry` is not a recognized command, either it is not installed or it is not in your system's PATH.

### Step A: Verify if Poetry is installed
Try running:
```bash
poetry --version
```

### Step B: Install Poetry
If it's not installed, the recommended way is using the official installer:

**Windows (PowerShell):**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### Step C: Add Poetry to PATH
If you just installed it and it still doesn't work, you may need to manually add it to your PATH:
1.  Open the **Start Menu**, search for "Edit the system environment variables", and press Enter.
2.  Click **Environment Variables**.
3.  Under **User variables**, find the `Path` variable and click **Edit**.
4.  Click **New** and add the following path:
    `%APPDATA%\Python\Scripts`
    *(Alternatively, if you used the official installer, look for `%USERPROFILE%\.local\bin` or `%APPDATA%\pypoetry\venv\Scripts`)*.
5.  Click **OK** on all windows and **restart your terminal**.

---

## 2. Windows Path Length Issues (MAX_PATH)

This is the most robust solution. It tells Windows to allow paths up to 32,767 characters.

### Option A: Using PowerShell (Admin)
Run the following command in an **elevated** PowerShell (Right-click PowerShell -> Run as Administrator):

```powershell
Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' -Name 'LongPathsEnabled' -Value 1
```

### Option B: Using Registry Editor
1.  Press `Win + R`, type `regedit`, and press Enter.
2.  Navigate to: `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`
3.  Find `LongPathsEnabled` and set its value to `1`.

> [!NOTE]
> You may need to restart your computer or restart your terminal/IDE for this change to take effect.

---

## 2. Relocate the Project

If you cannot or do not want to change system settings, move the project folder to a shorter path closer to the drive root.

**Example:**
- **From:** `C:\Users\YourName\Downloads\Projects\university-work\assignment-1\flood-tool-main`
- **To:** `C:\dev\flood-tool`

---

## 3. Configure Poetry Virtualenvs

By default, Poetry may create virtual environments in a deeply nested folder. You can configure it to store them in a shorter path or outside the project folder.

### Store virtualenvs in the default Cache directory
If you have `virtualenvs.in-project` set to `true`, Poetry puts the `.venv` inside your project folder. Disable it to use the default cache directory (which is usually shorter):

```bash
poetry config virtualenvs.in-project false
```

### Change the virtualenv storage location
You can explicitly set where Poetry stores its environments:

```bash
poetry config virtualenvs.path C:\pvenv
```

---

## 4. Shorten User Directory (Advanced)
If your Windows username is very long, it contributes to the path length. Consider using a shorter username or a different drive if available.
