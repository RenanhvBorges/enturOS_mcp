"""Ponto de entrada usado pelo pacote .mcpb (evita problemas de import relativo)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enturos_mcp.server import main

if __name__ == "__main__":
    main()
