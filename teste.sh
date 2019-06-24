#/bin/bash
for counter in {1..22}; do
	grupo=0;
	if [ "$counter" -le 10 ];
	then
		grupo=1;
	else
		grupo=2;
	fi
	echo "$grupo";
	python3 alvaromartinsespindola-201811162.py -in data/problemas-grupo$grupo/problema$counter.txt -out alavaroResultados -img SOL$grupo/problema$counter.png -sol SOL$grupo/problema$counterSol
done
