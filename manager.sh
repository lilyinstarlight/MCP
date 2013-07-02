#!/bin/sh
homedir="/home/armagetron"
bindir="$homedir/bin"
prefixdir="$homedir/servers"
rundir="$homedir/running"

waiting="[....]"
success="\r[\e[32;1m OK \e[00m]"
failure="\r[\e[31;1mFAIL\e[00m]"

if [ "$1" == "list" ]; then
	for dir in $(ls "$prefixdir"); do
		$0 status $dir
	done
	exit 0
fi

name="$2"
prefix="$prefixdir/$name"
pid="$rundir/$name.pid"
scriptpid="$rundir/$name-script.pid"
running=""
scriptrunning=""

if [ -f $pid ]; then
	if ps "$(< "$pid")" > /dev/null; then
		running="$(< "$pid")"
	else
		rm $pid
	fi
fi

if [ -f $scriptpid ]; then
	if ps "$(< "$scriptpid")" > /dev/null; then
		scriptrunning="$(< "$scriptpid")"
	else
		rm $scriptpid
	fi
fi

function start_script {
	/usr/sbin/daemonize -a -e "$prefix/script-error.log" -l "$scriptpid" "$bindir/script" "$prefix" "$scriptpid" "$bindir"
	if [ $? -ne 0 ]; then
		echo -e "$failure"
		stop
		exit 1
	fi
}


function start {
	echo -n "$waiting Starting server $name."
	if [ -s "$prefix/scripts/script.py" ]; then
		start_script
	fi
	/usr/sbin/daemonize -a -e "$prefix/error.log" -o "$prefix/arma.log" -l "$pid" "$bindir/armagetronad" "$prefix" "$pid"
	if [ $? -ne 0 ]; then
		echo -e "$failure"
		exit 1
	fi
	echo -e "$success"
}

function stop_script {
	echo "QUIT" >> "$prefix/var/ladderlog.txt"
	if [ $? -ne 0 ]; then
		echo -e "$failure"
		exit 1
	fi
	while [ -f $scriptpid ]; do
		continue
	done
	echo > "$prefix/var/ladderlog.txt"
}

function stop {
	echo -n "$waiting Stopping server $name."
	if [ "$scriptrunning" ]; then
		stop_script
	fi
	echo "QUIT" >> "$prefix/var/input.txt"
	if [ $? -ne 0 ]; then
		echo -e "$failure"
		exit 1
	fi
	while [ -f $pid ]; do
		continue
	done
	echo > "$prefix/var/input.txt"
	echo -e "$success"
}

function usage {
	echo -e "Usage:\t$0 {start|stop|status|reload|restart|restart-script} <server>"
	echo -e "\t$0 list"
	exit 1
}

if [ -z "$name" ]; then
	usage
fi

if [ ! -d "$prefix" ]; then
	echo "Server $name does not exist."
	echo
	usage
fi

case "$1" in
	start)
		if [ ! "$running" ]; then
			start
		else
			echo "Server $name is already running."
			exit 1
		fi
		;;
	stop)
		if [ "$running" ]; then
			stop
		else
			echo "Server $name is not running."
			exit 1
		fi
		;;
	status)
		if [ "$running" ]; then
			echo "Server $name status: Running."
		else
			echo "Server $name status: Stopped."
		fi
		;;
	reload)
		if [ "$running" ]; then
			echo "INCLUDE settings.cfg" >> "$prefix/var/input.txt"
			echo "INCLUDE server_info.cfg" >> "$prefix/var/input.txt"
			echo "INCLUDE settings_custom.cfg" >> "$prefix/var/input.txt"
			echo "INCLUDE script.cfg" >> "$prefix/var/input.txt"
			echo "START_NEW_MATCH" >> "$prefix/var/input.txt"
		else
			echo "Server $name is not running."
			exit 1
		fi
		;;
	restart)
		if [ "$running" ]; then
			stop
		fi
		start
		;;
	restart-script)
		if [ -f "$prefix/scripts/script.py" ]; then
			echo -n "$waiting Restarting script on server $name."
			if [ "$scriptrunning" ]; then
				stop_script
			fi
			start_script
			echo -e "$success"
		else
			echo "No script found for server $name."
		fi
		;;
	*)
		echo "Unrecognized command: $1"
		echo
		usage
esac
