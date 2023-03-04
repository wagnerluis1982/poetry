from __future__ import annotations

import os
import sys


def main() -> int:
    if sys.argv[0] == sys.argv[1]:
        if not os.path.exists(sys.argv[0]):
            raise RuntimeError(f"sys.argv[0] does not exist: {sys.argv[0]}")
    else:
        raise RuntimeError(
            f"unexpected sys.argv[0]: '{sys.argv[0]}', should be '{sys.argv[1]}'"
        )

    return 0


if __name__ == "__main__":
    raise sys.exit(main())
