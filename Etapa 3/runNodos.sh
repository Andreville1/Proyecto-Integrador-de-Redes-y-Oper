#!/bin/bash
declare -a distros=(A B C D E F)
for i in ${distros[@]}
do 
	#echo "server.py "$i
	gnome-terminal -- sh -c 'cd /home/eyson/Escritorio/Proyecto\ PI/Proyecto-Integrador-de-Redes-y-Oper/Etapa\ 3/; python3 ./server.py '$i'; exec bash'
	
done
