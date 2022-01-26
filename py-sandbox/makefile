docker-pyflink:
	echo $(pwd); \
	cd ./pyflink/base; \
	echo $(pwd); \
	docker build -t "ghcr.io/alex-y-kozlov-sandbox/pyflink/pyflink:1.14.3" . ;\
	cd ../.. ;\
	echo -e $(pwd) ;

docker-table-api:
	echo $(pwd) ;\
	cd ./table-api ;\
	echo $(pwd) ;\
	docker build -t "ghcr.io/alex-y-kozlov-sandbox/pyflink/table-api:1.14.3" . ;\
	cd ../.. ;\
	echo -e $(pwd) ;

dive-table-api:
	dive ghcr.io/alex-y-kozlov-sandbox/pyflink/table-api:1.14.3
