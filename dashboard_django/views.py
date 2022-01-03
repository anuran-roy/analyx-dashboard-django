from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse

from typing import Dict, List, Any, Tuple, NewType
from . import models

import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objects as go
from pandas import DataFrame, to_datetime, to_timedelta
from io import StringIO
import csv
from time import time

import networkx as nx
from pyvis.network import Network
import json

from analyx import metrics, endpoints, flow
import analyx.visualize as vs
# Create your views here.


metricman = metrics.Metrics(loc="Test")


def foo1():
    print("Bar")


def foo2():
    print("Bar2")


def foo3():
    print("Bar3")


def foo4():
    print("Bar4")


def foo5():
    print("Bar5")


def foo6():
    print("Bar6")


def blog(request):
    # Other code

    node2 = flow.FlowNode(endpoints.Endpoint(endpoint="/blog", id=blog), name="Blog")
    metricman.add_to_analytics(node2)

    # any return stuff
    return HttpResponse("<h1>Blog works!</h1>")


def about(request):
    # Other code

    node3 = flow.FlowNode(endpoints.Endpoint(endpoint="/about", id=about), name="About")
    metricman.add_to_analytics(node3)

    # any return stuff
    return HttpResponse("<h1>About works!</h1>")


def contact(request):
    # Other code

    node4 = flow.FlowNode(endpoints.Endpoint(endpoint="/contact", id=contact), name="Contact")
    metricman.add_to_analytics(node4)

    # any return stuff
    return HttpResponse("<h1>Contact works!</h1>")


def collaborations(request):
    # Other code

    node6 = flow.FlowNode(endpoints.Endpoint(endpoint="/collaborations", id=collaborations), name="Collaborations")
    metricman.add_to_analytics(node6)

    # any return stuff
    return HttpResponse("<h1>Collaborations works!</h1>")


def events(request):
    # Other code

    node5 = flow.FlowNode(endpoints.Endpoint(endpoint="/events", id=events), name="Events")
    metricman.add_to_analytics(node5)

    # any return stuff
    return HttpResponse("<h1>Events works!</h1>")


def home(request):
    node1 = flow.FlowNode(endpoints.Endpoint(endpoint="/home1", id=home), name="Home")
    metricman.add_to_analytics(node1)

    return HttpResponse("<h1>Home works!</h1>")


def dashboard(request):
    # G = nx.random_geometric_graph(20, 0.25)
    if request.user.is_superuser:
        graph = metricman.graph.visualize
        # print(f"\n{graph}\n")

        plot = vs.directed_pyvis(graph)
        # for i in metricman.pipeline(data="time_series", mode="live", interval=1, duration=5):
        #     print(i)


        # Plotly timeseries graphs

        data = DataFrame(metricman.time_series()["nodes"])

        if not data.empty:
            data.index = to_datetime(data["time"])

        print(data)

        # data = data.resample('M', on="time")
        # print(f"\n{data.columns}\n")
        # endpoints = list(data["id"].unique())
        # print(endpoints)
        # timeseries_plots = []
        # for i in endpoints:
        #     timeseries_plots += [pyo.plot(px.area(data[data["id"] == i], x="time", y="hits", title=f"Timeseries Hits Plot for {i}:"), output_type='div')]
        
        # timeseries_plots += [pyo.plot(px.area(data, x="time", y="hits", title="Overall Plot"), output_type='div')]

        return render(request, "dashboard_django/index.html", {
            "plot": plot,
            "time_series": sorted(metricman.time_series()["nodes"], key=lambda x:x["time"], reverse=True),
            "stats": sorted(metricman.aggregate().items(), key=lambda x:x[1], reverse=True),
            # "time_series_plots": timeseries_plots
        })
    else:
        return HttpResponse("<h1>Page doesn't exist!</h1>")

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def snapshot(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    return StreamingHttpResponse(
        (writer.writerow([row["id"],row["hits"],row["time"]]) for row in metricman.pipeline(mode="snapshot")),
        content_type="text/csv",
        headers={'Content-Disposition': 'attachment; filename="raw_{}.csv"'.format(time())},
    )


def raw(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    # rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    return StreamingHttpResponse(
        (writer.writerow([row["id"],row["hits"],row["time"]]) for row in metricman.pipeline()),
        content_type="text/csv",
        headers={'Content-Disposition': 'attachment; filename="raw_{}.csv"'.format(int(time()))},
    )


def streaming(request):
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    return StreamingHttpResponse(
        (writer.writerow([row["id"],row["hits"],row["time"], "<br>"]) for row in metricman.pipeline())
    )
