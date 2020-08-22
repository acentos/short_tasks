#!/usr/bin/bash

RPACK="arp-scan nmap";
INTERFACE=`ifconfig | awk '{print $1}' | grep ":" | grep -Ev "lo|tun" | sed 's/.$//'`
RESULT_DIRECTORY="result"

for i in $RPACK;
do
    rpm -q $i;
    if [ $? -ne 0 ];
    then
        sudo yum -y install $i;
    fi
done

if [ ! -d "$RESULT_DIRECTORY" ];
then
    mkdir $RESULT_DIRECTORY;
fi


for i in ${INTERFACE};
do
    echo "Check for: ${i}";
    ARPSCAN=`sudo arp-scan --interface=${i} --localnet| grep -v 'Interface\|Starting\|packets\|Ending' | awk '{print $1}'`;
    sudo arp-scan --interface=${i} --localnet
    for as in $ARPSCAN;
    do
        ping -c 2 $as > /dev/null;
        if [ $? -eq 0 ];
        then
            echo -e ">>> hostname: $as\n";
            nmap -A $as >> $RESULT_DIRECTORY/${as}_$(date +%Y-%m-%d_%H-%M-%S).txt;
        fi
    done
done

exit 0
