# Fix Permission Issues on Remote Server

## Commands to run on your remote server (cheburator@stomat-test-diagrams):

### 1. Check current directory and permissions
```bash
pwd
ls -la
```

### 2. Check who owns the directory
```bash
ls -la ~/zykovagexagon/
```

### 3. Fix ownership (if needed)
```bash
# Option A: Change ownership to current user
sudo chown -R $USER:$USER ~/zykovagexagon/stom-app-gexagonal/

# Option B: If directory doesn't exist, create it first
mkdir -p ~/zykovagexagon/
cd ~/zykovagexagon/
git clone https://github.com/shpriz/stom-app-gexagonal.git
```

### 4. Navigate to the correct directory
```bash
cd ~/zykovagexagon/stom-app-gexagonal/
```

### 5. Copy the environment file
```bash
cp .env.example .env
```

### 6. Make the file writable
```bash
chmod 644 .env
```

### 7. Edit the environment file
```bash
nano .env
```

## Alternative: Use sudo if ownership can't be changed
```bash
# Copy with sudo
sudo cp .env.example .env

# Change ownership after copying
sudo chown $USER:$USER .env

# Make it writable
chmod 644 .env
```

## Quick Fix Command (run this on your server):
```bash
cd ~/zykovagexagon/stom-app-gexagonal && sudo chown -R $USER:$USER . && cp .env.example .env
```