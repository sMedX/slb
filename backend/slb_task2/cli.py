import argparse

import aiohttp.web

from slb_task2.app import create_app
from slb_task2.settings import load_config

import asyncio
import sys

if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='SLB Task2 App')

    parser.add_argument('--host',
                        help='Host to listen',
                        default='127.0.0.1')

    parser.add_argument('--port',
                        help='Port to accept connections',
                        default=4449)

    parser.add_argument('--log',
                        help='Logging severity level',
                        default='INFO')

    parser.add_argument('-fl', '--filelog',
                        type=str2bool,
                        help='Logging into file "slb_task2-backend.log"',
                        default=False)

    parser.add_argument('-c', '--config',
                        type=argparse.FileType('r'),
                        help='Path to configuration file')
    return parser

def str2bool(v: str) -> bool:

    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main() -> None:
    args = build_parser().parse_args()
    config = load_config(args.config)
    config.update(**(vars(args)))
    app = create_app(config=config)

    aiohttp.web.run_app(app, host=args.host, port=args.port)


def get_app(argv):
    args = build_parser().parse_args()
    config = load_config(args.config)
    config.update(**(vars(args)))
    app = create_app(config=config)

    return app

if __name__ == '__main__':
    main()
