For the long-lived containers like a sidecars or so avoid bare `sleep infinity` consider using 
```shell
sleep infinity &
trap 'kill $! 2>/dev/null; exit 0' TERM INT
wait $! 
```
