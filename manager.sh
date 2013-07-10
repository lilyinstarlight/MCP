#!/bin/sh
homedir="/home/armagetron"
bindir="$homedir/bin"
prefixdir="$homedir/servers"
rundir="$homedir/running"

daemonize="/usr/sbin/daemonize"

if [ $(tput colors) -ge 8 ]; then
	waiting="$(tput sc)[....]"
	success="$(tput rc)[$(tput setaf 2) OK $(tput sgr0)]"
	failure="$(tput rc)[$(tput setaf 1)FAIL$(tput sgr0)]"
else
	waiting="*"
	success=" OK!"
	failure=" FAIL!"
fi

if [ "$1" = "list" ]; then
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
	if ps "$(cat "$pid")" > /dev/null; then
		running="$(cat "$pid")"
	else
		rm $pid
		echo > "$prefix/var/ladderlog.txt"
		echo > "$prefix/var/input.txt"
	fi
fi

if [ -f $scriptpid ]; then
	if ps "$(cat "$scriptpid")" > /dev/null; then
		scriptrunning="$(cat "$scriptpid")"
	else
		rm $scriptpid
		echo > "$prefix/var/ladderlog.txt"
	fi
fi

start_script() {
	"$daemonize" -a -e "$prefix/script-error.log" -l "$scriptpid" "$bindir/script" "$prefix" "$scriptpid" "$bindir"
	if [ $? -ne 0 ]; then
		echo "$failure"
		stop
		exit 1
	fi
}


start() {
	echo -n "$waiting Starting server $name..."
	if [ -s "$prefix/scripts/script.py" ]; then
		start_script
	fi
	"$daemonize" -a -e "$prefix/error.log" -o "$prefix/arma.log" -l "$pid" "$bindir/armagetronad" "$prefix" "$pid"
	if [ $? -ne 0 ]; then
		echo "$failure"
		exit 1
	fi
	echo "$success"
}

stop_script() {
	echo "QUIT" >> "$prefix/var/ladderlog.txt"
	if [ $? -ne 0 ]; then
		echo "$failure"
		exit 1
	fi
	KILL=0
	while [ -f "$scriptpid" ]; do
		KILL=$((KILL + 1))
		if [ $KILL -gt 50 ]; then
			kill -KILL -$scriptrunning
			rm "$scriptpid"
			break
		fi
		sleep 0.1
	done
	echo > "$prefix/var/ladderlog.txt"
}

stop() {
	echo -n "$waiting Stopping server $name..."
	if [ "$scriptrunning" ]; then
		stop_script
	fi
	echo "QUIT" >> "$prefix/var/input.txt"
	if [ $? -ne 0 ]; then
		echo "$failure"
		exit 1
	fi
	KILL=0
	while [ -f "$pid" ]; do
		KILL=$((KILL + 1))
		if [ $KILL -gt 50 ]; then
			kill -KILL -$running
			rm "$pid"
			break
		fi
		sleep 0.1
	done
	echo > "$prefix/var/ladderlog.txt"
	echo > "$prefix/var/input.txt"
	echo "$success"
}

usage() {
	echo "Usage:\t$0 {start|stop|status|reload|restart|restart-script} <server>"
	echo "\t$0 list"
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
			echo "$success"
		else
			echo "No script found for server $name."
		fi
		;;
	*)
		echo "Unrecognized command: $1"
		echo
		usage
esac
