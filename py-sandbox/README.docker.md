

```bash
dive ghcr.io/alex-y-kozlov-sandbox/pyflink/table-api:1.14.3
docker-compose down
docker-compose exec jobmanager /bin/bash 
/opt/flink/bin/flink run -py /opt/table-api/table-sql.py -d
/opt/flink/bin/flink run -py /opt/table-api/kafka-mp2.py -d
docker-compose exec jobmanager ./bin/flink run -py /opt/table-api/table-sql.py -d
docker-compose exec jobmanager ./bin/flink run -py /opt/table-api/kafka-pm2.py -d
docker-compose down
```

./bin/flink run -py ~/program/repos/sandbox/flink-playgrounds/py-sandbox/table-api/table-api.py -d
./bin/flink run -py ~/program/repos/sandbox/flink-playgrounds/py-sandbox/table-api/table-sql.py -d
./bin/flink run -py /opt/table-api/kafka-mp.py -d

/usr/local/opt/python@3.8/bin/pip3
/usr/local/opt/python@3.8/bin/python3

echo "alias pip=/usr/local/opt/python@3.8/bin/pip3" >> ~/.zshrc 
echo "alias python=/usr/local/opt/python@3.8/bin/python3" >> ~/.zshrc 
echo "alias pip=/usr/local/opt/python@3.8/bin/pip3" >> ~/.bashrc
echo "alias python=/usr/local/opt/python@3.8/bin/python3" >> ~/.bashrc