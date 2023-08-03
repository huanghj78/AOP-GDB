#!/usr/bin/expect -f
set pid [lindex $argv 0]

set timeout -1
spawn ./gdb -p ${pid}
expect "(gdb)"
send "source main.py\n"
expect "(gdb)"
# send "q\n