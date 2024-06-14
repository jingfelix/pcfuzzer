import json
import logging
import os
import random
import subprocess
import tempfile

import pysource_codegen
import typer
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, handlers=[RichHandler()], format="%(message)s")

logger = logging.getLogger(__name__)

app = typer.Typer()

TARGET_VERSION = os.environ.get("TARGET_VERSION", None)
if not TARGET_VERSION:
    logger.error("TARGET_VERSION not set")
    raise typer.Exit(code=1)


@app.command()
def run(
    module: str,
    command: str = typer.Option("", help="Command to pass to the module"),
    option: str = typer.Option("", help="Option to pass to the module"),
):
    """Test python module"""
    logger.info(f"Testing module {module} with command {command} and option {option}")

    # 检查 result 输出目录是否存在
    if not os.path.exists("../result"):
        logger.error("Result directory not found")
        raise typer.Exit(code=1)

    # 检查 module 是否在 path 中
    try:
        res = subprocess.run(
            ["which", module],
            check=True,
            env={"PATH": os.environ["PATH"]},
            capture_output=True,
        )
    except subprocess.CalledProcessError:
        logger.error(f"Module {module} not found in path")
        raise typer.Exit(code=1)

    while True:
        seed = random.randint(0, 10000)

        with tempfile.NamedTemporaryFile(suffix=".py") as tmp:
            code = pysource_codegen.generate(seed)
            tmp.write(bytes(code, "utf-8"))
            tmp.flush()

            logger.debug(f"Running with seed {seed}")
            res = subprocess.run(
                ["python", "-m", module, command, str(tmp.name), option],
                capture_output=True,
            )

            if res.returncode != 0:
                logger.error(f"Error running module {module}")

                with open(f"../result/{TARGET_VERSION}_{seed}.json", "w") as f:
                    report = {
                        "version": TARGET_VERSION,
                        "seed": seed,
                        "code": code,
                        "stdout": res.stdout.decode("utf-8"),
                        "stderr": res.stderr.decode("utf-8"),
                    }

                    json.dump(report, f, indent=4)

                    logger.info(
                        f"Report saved to ../result/{TARGET_VERSION}_{seed}.json"
                    )


@app.callback()
def callback(verbose: bool = False):
    if verbose:
        logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    app()
