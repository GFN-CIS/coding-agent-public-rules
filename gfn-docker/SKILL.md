---
name: gfn-docker
description: Use when writing or reviewing Dockerfiles or long-lived containers such as sidecars. Replaces bare `sleep infinity` with signal-handling shell.
---
## Required standards

Apply together with skill `gfn-code`.

For the long-lived containers like a sidecars or so avoid bare `sleep infinity` consider using 
```shell
sleep infinity &
trap 'kill $! 2>/dev/null; exit 0' TERM INT
wait $! 
```
