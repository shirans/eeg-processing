#!/usr/bin/env python3

import argparse
import m_server.muse_server

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="10.0.0.3",
                        help="The ip to listen on")
    parser.add_argument("--port",
                        type=int,
                        default=8001,
                        help="The port to listen on")
    args = parser.parse_args()

    m_server.muse_server.MuseServer("muse-123456789", args.ip, args.port,"bot").start_server()
