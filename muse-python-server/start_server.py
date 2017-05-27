import argparse
import server.muse_server

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="10.0.0.5",
                        help="The ip to listen on")
    parser.add_argument("--port",
                        type=int,
                        default=5001,
                        help="The port to listen on")
    args = parser.parse_args()

    server.muse_server.MuseServer("muse-123456789", args.ip, args.port).start_server()
