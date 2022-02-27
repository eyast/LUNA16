"""Conrtains functions to draw Mermaid graphs in Markdown, as well as the graph definitions"""


import base64

import matplotlib.pyplot as plt
from IPython.display import Image, display


def graph(graph):
    """Renders a mermaid graph."""
    graphbytes = graph.encode("ascii")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    display(Image(url="https://mermaid.ink/img/" + base64_string))


data_explanation_06 = """flowchart TD 
    A[LIDC-DIRI dataset] --> |includes # 1776| B[CT scans] 
    A --> |Not sure how many are included|Z[Annotations of lesions]
    subgraph obj [Objective]
    Z --> Y[Nodule >= 3 mm]
    Z --> X[Nodule <= 3 mm]
    end 
    Z --> W[non-Nodule >= 3 cmm]
    subgraph exist [Already explored]
    B --> G[Raw files]
    end
    subgraph coordraw [coord.]
    H[I,R,C] 
    end
    subgraph coordannot [coord.]
    I[X,Y,Z]
    end
exist -->coordraw    
obj --> coordannot"""