# tplink-stats
Generate statistics for a TP-Link TL-SG1016DE switch

The generated statistics are formatted for import into influxdb to
easily build up a grafana dashboard.

I'm using 'telegraf' to push the data into influxdb; sample configuration
is:
```
[[inputs.exec]]
  ## Commands array
  commands = [
    "/usr/local/bin/tplink-stats",
  ]

  ## Do not check too often to avoid flooding the GUI
  interval = "1m"

  ## Timeout for each command to complete.
  timeout = "10s"

  ## Data format to consume.
  ## Each data format has its own unique set of configuration options, read
  ## more about them here:
  ## https://github.com/influxdata/telegraf/blob/master/docs/DATA_FORMATS_INPUT.md
  data_format = "influx"
```
