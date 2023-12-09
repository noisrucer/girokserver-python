import argparse
import os

import uvicorn


def extract_args() -> dict:
    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        "-e",
        "--env",
        type=str,
        help='Server environment. Either "local", "dev", or "prod".',
        choices=["dev", "local", "prod"],
        default="dev",
    )
    args = argParser.parse_args()
    return {"env": args.env}


def main(env: str) -> None:
    os.environ["ENV"] = env
    os.environ["ENV_FILE_PATH"] = f".env.{env}"
    print(f"- Running server in {env} environment...")
    uvicorn.run(
        app="girok.server:app",
        host="127.0.0.1",
        port=8080,
        log_level="info",
        reload=True if env == "dev" else False,
    )


# Run `python -m girok` to start the server
if __name__ == "__main__":
    args = extract_args()
    main(env=args["env"])
