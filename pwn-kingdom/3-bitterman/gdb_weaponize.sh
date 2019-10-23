#!/usr/bin/env bash

# Usage: bash gdb_weaponize.sh
# Inspired by "Pwndbg + GEF + Peda — One for all, and all for one" -- https://medium.com/bugbountywriteup/pwndbg-gef-peda-one-for-all-and-all-for-one-714d71bf36b8

G="\033[1;32m"  # GREEN
Y="\033[1;33m"  # YELLOW
R="\033[1;31m"  # RED
NC="\033[0m"    # NO COLOR

# --------------- Check for root privileges ----------------

if [[ $EUID -ne 0 ]]; then
	printf "${Y}[!] Please run as root:\nsudo %s${NC}\n" "${0}"
	exit 0
fi

# ------------ Check for required dependencies -------------

if ! which git >/dev/null 2>&1; then
	printf "${Y}[-] Git not found! Aborting...{NC}\n"
	exit 0
fi

# -------------------- Remove old stuff --------------------

rm -rf /opt/gdb_weaponize /usr/bin/gdb-* ~/.gdbinit

# ---------------------- Installation ----------------------

printf "${G}[+] Downloading PEDA...${NC}\n"
git clone https://github.com/longld/peda.git /opt/gdb_weaponize/peda
# echo "source /opt/gdb_weaponize/peda/peda.py" > ~/.gdbinit

printf "${G}[+] Downloading GEF...${NC}\n"
wget -O /opt/gdb_weaponize/gef.py https://github.com/hugsy/gef/raw/master/gef.py
# echo "source /opt/gdb_weaponize/gef.py" > ~/.gdbinit

printf "${G}[+] Downloading pwndbg...${NC}\n"
git clone https://github.com/pwndbg/pwndbg /opt/gdb_weaponize/pwndbg
cd /opt/gdb_weaponize/pwndbg
./setup.sh
cd ~
# echo "source /opt/gdb_weaponize/pwndbg/gdbinit.py" > ~/.gdbinit

printf "${G}[+] Creating ~/.gdbinit...${NC}\n"
cat << EOT > ~/.gdbinit
define init-peda
source /opt/gdb_weaponize/peda/peda.py
end
document init-peda
Initializes the PEDA (Python Exploit Development Assistant for GDB) framework
end

define init-gef
source /opt/gdb_weaponize/gef.py
end
document init-gef
Initializes GEF (GDB Enhanced Features)
end

define init-pwndbg
source /opt/gdb_weaponize/pwndbg/gdbinit.py
end
document init-pwndbg
Initializes PwnDBG
end
EOT

printf "${G}[+] Creating /usr/bin/gdb-peda...${NC}\n"
cat << EOT > /usr/bin/gdb-peda
#!/bin/sh
exec gdb -q -ex init-peda "\$@"
EOT

printf "${G}[+] Creating /usr/bin/gdb-gef...${NC}\n"
cat << EOT > /usr/bin/gdb-gef
#!/bin/sh
exec gdb -q -ex init-gef "\$@"
EOT

printf "${G}[+] Creating /usr/bin/gdb-pwndbg...${NC}\n"
cat << EOT > /usr/bin/gdb-pwndbg
#!/bin/sh
exec gdb -q -ex init-pwndbg "\$@"
EOT

printf "${G}[*] Setting permission bits...${NC}\n"
chmod +x /usr/bin/gdb-*

printf "${G}[+] Done${NC}\n"
