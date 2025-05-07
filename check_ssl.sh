#!/bin/bash

get_host() {
    # Eliminar 'https://' o 'http://'
    url="${1//https:\/\//}"
    url="${url//http:\/\//}"

    # Verificar si la URL contiene un puerto
    if [[ "$url" =~ ^([a-zA-Z0-9.-]+):([0-9]+) ]]; then
        # Si contiene un puerto, extraerlo

        echo "$url"
    else
        # Si no contiene un puerto, devolver 443 por defecto
        echo "$url:443"
    fi
}

sweet32(){
	local url="$1"
	echo -e "

    ╭━━━╮╱╱╱╱╱╱╱╱╱╱╭╮╭━━━┳━━━╮
    ┃╭━╮┃╱╱╱╱╱╱╱╱╱╭╯╰┫╭━╮┃╭━╮┃
    ┃╰━━┳╮╭╮╭┳━━┳━┻╮╭┻╯╭╯┣╯╭╯┃
    ╰━━╮┃╰╯╰╯┃┃━┫┃━┫┃╭╮╰╮┣━╯╭╯
    ┃╰━╯┣╮╭╮╭┫┃━┫┃━┫╰┫╰━╯┃┃╰━╮
    ╰━━━╯╰╯╰╯╰━━┻━━┻━┻━━━┻━━━╯
    $url\n\n"

	testssl --quiet --sweet32 -E "$url"
}


lucky13(){
	local url="$1"
	echo -e "
        █████████████████████████████████████████
        █▄─▄███▄─██─▄█─▄▄▄─█▄─█─▄█▄─█─▄█▀░██▄▄▄░█
        ██─██▀██─██─██─███▀██─▄▀███▄─▄███░███▄▄░█
        ▀▄▄▄▄▄▀▀▄▄▄▄▀▀▄▄▄▄▄▀▄▄▀▄▄▀▀▄▄▄▀▀▄▄▄▀▄▄▄▄▀
        $url\n\n"
    tempfile=$(basename $(mktemp))
    testssl --quiet -P --lucky13 $url > /tmp/$tempfile
    vulnerable=$(cat /tmp/$tempfile | grep VULNERABLE)
    if [[ -n "$vulnerable" ]]; then
        cat /tmp/$tempfile
        host=$(get_host $url)
        cipher=$(grep -m 1 -oE "TLS_[A-Z0-9_]*_CBC_[A-Z0-9_]*" /tmp/$tempfile | awk '{print $NF}')
        echo -e "\e[1;30;47m Running openssl s_client -cipher '$cipher' -connect $host \e[0m"
        echo -e "\n\n\e[34mopenssl\e[0m \e[37ms_client\e[0m \e[32m-cipher\e[0m \e[33m'$cipher'\e[0m \e[32m-connect\e[0m \e[37m$host\e[0m"
        openssl s_client -cipher $cipher -connect $host
    else
        echo -e "not vulnerable (OK)"
    fi
	
    
}

beast(){
	local url="$1"
    tempfile=$(basename $(mktemp))
    
	echo -e "
    ███████████████████████████████
    █▄─▄─▀█▄─▄▄─██▀▄─██─▄▄▄▄█─▄─▄─█
    ██─▄─▀██─▄█▀██─▀─██▄▄▄▄─███─███
    ▀▄▄▄▄▀▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀▀▄▄▄▀▀
    $url\n\n"
	testssl --quiet -P --beast  $url > /tmp/$tempfile
    vulnerable=$(cat /tmp/$tempfile | grep VULNERABLE)
    if [[ -n "$vulnerable" ]]; then
        cat /tmp/$tempfile
        cipher=$(grep -m1 -oE "TLS_[A-Z0-9_]*_CBC_[A-Z0-9_]*" /tmp/$tempfile | awk '{print $NF} ')
        echo -e "\e[1;30;47m Running openssl s_client -cipher '$cipher' -connect $url \e[0m\n\n"
        echo -e "\e[34mopenssl\e[0m \e[37ms_client\e[0m \e[32m-cipher\e[0m \e[33m'$cipher'\e[0m \e[32m-tls1\e[0m \e[32m-connect\e[0m \e[37m$url\e[0m"
        host=$(get_host $url)
        openssl s_client -cipher $cipher -tls1 -connect $host
    else
        echo -e "No Vulnerable!!!\n"
        cat /tmp/$tempfile
    fi
}

breach(){
    tempfile=$(basename $(mktemp))
    testssl --quiet -P --breach  $url > /tmp/$tempfile 
    vulnerable=$(cat /tmp/$tempfile | grep VULNERABLE)
    if [[ -n "$vulnerable" ]]; then
        cat /tmp/$tempfile
        cipher=$(grep -m1 -oE "TLS_[A-Z0-9_]*_CBC_[A-Z0-9_]*" /tmp/$tempfile | awk '{print $NF} ')
        echo -e "\e[1;30;47m Running openssl s_client -cipher '$cipher' -connect $url \e[0m\n\n"
        echo -e "\e[34mopenssl\e[0m \e[37ms_client\e[0m \e[32m-cipher\e[0m \e[33m'$cipher'\e[0m \e[32m-tls1\e[0m \e[32m-connect\e[0m \e[37m$url\e[0m"
        host=$(get_host $url)
        openssl s_client -cipher $cipher -tls1 -connect $host
    else
        echo -e "No Vulnerable!!!\n"
        cat /tmp/$tempfile
    fi
}


url="${!#}"

case "$1" in
    --sweet32)
        sweet32 "$url"
        ;;
    --lucky13)
        lucky13 "$url"
        ;;
    --beast)
        beast "$url"
        ;;
    --breach)
        breach "$url"
        ;;
    *)
        echo "Parámetro no reconocido: $1"
        echo "Uso: $0 [--sweet32] | [--lucky13]| [--beast] | [--breach] <URL>"
        exit 1
        ;;
esac

