import sys
from Painter import Painter

painter = Painter(sys.argv[1:-1], sys.argv[-1])
painter.print_figure()