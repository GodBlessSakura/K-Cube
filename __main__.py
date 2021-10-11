from app import create_app

import argparse
parser = argparse.ArgumentParser(description='K-CUBE flask server')
parser.add_argument('--config', metavar='config_name', type=str,default='default',
                    help='name of configuration')
parser.add_argument('--port' , metavar='port', type=int,default=5000,
                    help='port for the web server')
if __name__ == "__main__":
    args = parser.parse_args()
    app = create_app(args.config)
    app.run(port = args.port)