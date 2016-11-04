DEST=/home/broihier/test

install: x10_server
	mkdir $(DEST)
	crontab -l > originalCrontab.txt
	cp -p crontabTemplate.txt newCrontabEntries.txt
	sed -i s:_Dest_:$(DEST):g newCrontabEntries.txt
	cp -p x10lightsTemplate x10lights
	sed -i s:_Dest_:$(DEST): x10lights
	cp -p restartTemplate restart
	sed -i s:_Dest_:$(DEST): restart
	cp -p x10_server $(DEST)/
	cp -p x10Client $(DEST)/
	cp -p x10lights $(DEST)/
	cp -p sunset.txt $(DEST)/
	cp -p net $(DEST)/
	cp -p on $(DEST)/
	cp -p off $(DEST)/
	cp -p restart $(DEST)/
	cat originalCrontab.txt newCrontabEntries.txt > newCrontab.txt
	crontab < newCrontab.txt
	rm originalCrontab.txt newCrontab.txt
	cd $(DEST)
	sudo ./x10_server -d
	./x10lights -d

x10_server: x10_server.c
	gcc x10_server.c -o x10_server
