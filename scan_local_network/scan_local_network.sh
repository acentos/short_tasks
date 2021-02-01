#!/usr/bin/bash

RPACK="arp-scan nmap";
INTERFACE=`ifconfig | awk '{print $1}' | grep ":" | grep -Ev "lo|tun" | sed 's/.$//'`
RESULT_DIRECTORY="scan_results_$(date +%Y-%m-%d_%H-%M-%S)"

function directory_check () {
    if [ ! -d "$RESULT_DIRECTORY" ];
    then
        mkdir $RESULT_DIRECTORY;
    fi
    
    if [ ! -d "$RESULT_DIRECTORY" ];
    then
        echo "Directory ERROR.";
        exit 0;
    fi
}

for i in $RPACK;
do
    rpm -q $i;
    if [ $? -ne 0 ];
    then
        sudo yum -y install $i;
    fi
done

directory_check;

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
            directory_check;
            echo -e ">>> hostname: $as\n";
            nmap -A $as >> $RESULT_DIRECTORY/${as}_$(date +%Y-%m-%d_%H-%M-%S).txt;
        fi
    done
done

exit 0
