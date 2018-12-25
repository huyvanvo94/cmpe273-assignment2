## Distributed Hash Functions 
``` 
RendezVous Hashing
Consistent Hashing 
```

## To run

#### Start the servers 
```
python3 api.py 5000
python3 api.py 5001
python3 api.py 5002
python3 api.py 5003
```
### Or 

```
sh test.sh
```

#### Run Hash Algorithms against local nodes 

```
python3 consistent_hash.py causes-of-death.csv
python3 hrw_hash.py causes-of-death.csv
``` 
