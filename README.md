# tplink-stats
Generate statistics for a TP-Link TL-SG1016DE switch.

The switch only has a very rudimentary Web GUI, and I've found no
way to extract the data by other means than scraping off the generated
HTML format from the GUI.

Also it's not using the standard HTML password features, ie you can't
just use `curl -u <username>:<password> http://<ipaddress>/<url>` to
get to the data; rather one has to use PUT with a special formatted
HTML for logging in. After that, every access from the given IP address is
considered validated until logout is called from the address.
So be careful when experimenting.
In a similar vein the GUI isn't the fastest, so I deliberately chose a
1 minute interval to not overload the GUI.

The generated statistics are formatted for import into influxdb to
easily build up a grafana dashboard.

I'm using *telegraf* to push the data into influxdb; sample configuration
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
