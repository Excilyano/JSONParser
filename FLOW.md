# Process followed during the project
This document will describe the process we followed and the elements we tested to make the JSON parser and the visual report.

## JSON Parser

## Visual report
The goal of this visual report is to show the main metrics of each request to see where can be found huge time consumption.
1. First, we tried to use Graphviz to make a tree view of the request calls and to see the parent/children relationship between the requests.
After generating a few graphs, we abandonned it because of the illegibility of the generated tree, which was too small on the page, 
and requested a huge zoom in to see something. Moreover, the tree wasn't disposed in a helpful way.
2. Then, we tried Grafana, which is already used to monitor some metrics in OpenStack. But it was too powerfull for what we were trying to do, 
and we lost some time to try to use it for the metrics form our generated JSON.
3. Finally, we choose to use Plotly, in order to generate a webpage which contains all our graphs. It simply generates an HTML page from a python source code.
