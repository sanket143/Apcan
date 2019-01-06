build: cli.py launch.py
	@mkdir -p ~/Programs
	@mkdir -p ~/Programs/Apcan
	@cp launch.py ~/Programs/Apcan/
	@cp cli.py ~/Programs/Apcan/
	@echo "Configured Successfully"
	@echo "Run \`sudo make install\` to install"

install: apcan
	@chmod +x ./apcan
	@cp apcan /usr/bin/ || exit 1
	@echo "Installed Successfully"

remove: /usr/bin/apcan
	@echo "Removing Apcan..."
	@bash ./apcan
