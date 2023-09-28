## Some thoughts

- processPhoto is faster than photo because it writes a reduced file size to the storage account. IO-bound
- It should run faster on Azure App Service, because higher cloud bandwidth
- Separate container to process Blob Triggers for resize (if you want both original image and resize, otherwise request time will be some of both actions)
- Try profiling with Jaeger and OpenTelemetry
