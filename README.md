1)
docker build -t finastra-ws-processor .

2)
docker run -d  -p 9090:9090 finastra-ws-processor

or - interactive (for debuging):
docker run -it -p 9090:9090 finastra-ws-processor
