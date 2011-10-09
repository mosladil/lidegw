#!/bin/zsh
#
# @@@ Coded by p4t0k @@@
# 
# e-mail: p4t0kk@gmail.com
#
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# %% This program is licensed under terms of the GNU GPL.
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#
# 2007-01-16 >>> Project started!
#

# <config>

# pefix directory
#
prefix="$HOME/.liphoto/"

# dowloader (currently supported downloaders are wget & curl)
downloader="wget"

# image viewer (only display is supportet nowadays)
viewer="display"

# define whether remove downloaded images after displaying
rmimages="yes"

#
## </config>
## <core>
#
_version="0.3"

# define interrupt trigger
TRAPINT()
{
	print "\n\n${terminfo[sgr0]}[${terminfo[bold]}@${terminfo[sgr0]}] Quitting..."
	exit 0
}

# check whether script can run properly
for bin in "$viewer" "$downloader"
do
	if [[ ${$(whereis -b "$bin")[2]} == "" ]]; then
		print 'Error! It is NOT possible to run script due to missing >>' "$bin" '<< binary.'
		exit 1
	fi
done

# append downloader options
case "$downloader" in
	("wget") downloader+=" -qO";;
	("curl") downloader+=" -so";;
esac

# program info
<<- EOD
----------------------------------------------------------
${terminfo[bold]}Welcome to lide.cz photo parser and browser Z-Shell script${terminfo[sgr0]}
----------------------------------------------------------
               --- version => ${terminfo[bold]}${_version}${terminfo[sgr0]} ---

         !! press ^C to quit this script !!

EOD

# create the prefix directory
if [[ ! -d "$prefix" ]]; then
	install -d "$prefix" &> /dev/null
fi

# main loop
while true

do
	echo -n "user_name: "
	echo -n ${terminfo[bold]}
	read luser
	echo -n ${terminfo[sgr0]}

	if [[ $luser == "" ]]; then
		continue
	fi
	# enter the prefix directory
	cd "$prefix"

	for lnk in $(curl -s "http://profil.lide.cz/profile.fcgi?akce=profile&user=$luser"|awk -F\' '/large([0-9]|[-/])+\.(jpg|jpeg|gif|png|bmp)/{print $2}')
	do
		# check whether image file isn't downloaded already
		if [[ -e "${prefix}${luser}-${lnk##*-}" ]]; then
			continue
		fi
		# download all images
		eval "$downloader${luser}-${lnk##*-} $lnk" &> /dev/null || exit 1
		print "[${terminfo[bold]}*${terminfo[sgr0]}] Downloading ${luser}-${lnk##*-}..."
	done
	# go back
	cd -
# if there are no photos to parse go to the start of the loop
if [[ $lnk == "" ]]; then
	print "[${terminfo[bold]}!${terminfo[sgr0]}] There are NO photos or user of this name!"
	continue
fi

print "[${terminfo[bold]}*${terminfo[sgr0]}] Displaying photos..."
eval "$viewer ${prefix}${luser}*" || exit 1

# remove images
if [[ "$rmimages" == "yes" ]]; then
	print "[${terminfo[bold]}*${terminfo[sgr0]}] Removing files..."
	for file in ${prefix}${luser}*
	do
		rm $file
	done
fi

unset lnk

done

#
## </core>

