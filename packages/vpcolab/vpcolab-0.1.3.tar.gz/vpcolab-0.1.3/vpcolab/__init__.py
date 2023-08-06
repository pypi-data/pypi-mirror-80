from .functions import average, power
from .greet import SayHello
try:
  import google.colab
  RunningInCOLAB = True
except:
  RunningInCOLAB = False
  
# Jupyter Extension points
def _jupyter_nbextension_paths():
    if RunningInCOLAB:
        return [dict(
            section="notebook",
            # the path is relative to the `vpython` directory
            src="vpython_libraries",
            # directory in the `nbextension/` namespace
            dest="vpython_libraries",
            # _also_ in the `nbextension/` namespace
            require="vpython_libraries/glowcommcolab"),
            dict(
            section="notebook",
            # the path is relative to the `vpython` directory
            src="vpython_data",
            # directory in the `nbextension/` namespace
            dest="vpython_data",
            # _also_ in the `nbextension/` namespace
            require="vpython_libraries/glowcommcolab")]
    else:
        return [dict(
            section="notebook",
            # the path is relative to the `vpython` directory
            src="vpython_libraries",
            # directory in the `nbextension/` namespace
            dest="vpython_libraries",
            # _also_ in the `nbextension/` namespace
            require="vpython_libraries/glowcomm"),
            dict(
            section="notebook",
            # the path is relative to the `vpython` directory
            src="vpython_data",
            # directory in the `nbextension/` namespace
            dest="vpython_data",
            # _also_ in the `nbextension/` namespace
            require="vpython_libraries/glowcomm")]

