import base64
from IPython.display import Image, display
import matplotlib.pyplot as plt

def draw_mermaid_graph(graph):
    """Renders a mermaid graph."""
    graphbytes = graph.encode("ascii")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    display(Image(url="https://mermaid.ink/img/" + base64_string))