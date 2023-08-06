# get info
OS = $(shell uname)
SFLAG = $(shell id -u)

# set commands
RM = rm -f
MV = mv
MKDIR = mkdir -p
INSTALLER = pyinstaller --onefile

# default
default: build

# build
build: clean
	@$(INSTALLER) ptmv.py
	@$(MKDIR) bin
	@$(MV) dist/ptmv bin/
	@$(RM) -r build/ dist/ ptmv.spec

# install
install: uninstall build
	@$(MV) bin/ptmv /usr/local/bin

# uninstall
uninstall:
	@$(RM) /usr/local/bin/ptmv

# clean
clean:
	@$(RM) -r bin/