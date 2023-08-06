import argparse
import sys
import makinas
import tensorflow as tf

execname = 'makinas'

def pull():
    parser = argparse.ArgumentParser(description='Pull a model from Makinas',
        usage=execname + ''' pull <runtime> <id>
        ''')
    parser.add_argument('runtime', help="Target Runtime")
    parser.add_argument('id', help="Model ID")
    args = parser.parse_args(sys.argv[2:])
    cli = makinas.Client()
    fname = cli.get_model(args.id+'/'+args.runtime)
    print('Downloaded model: '+fname)

def push():
    parser = argparse.ArgumentParser(description='Push a model to Makinas',
        usage=execname + ''' push <path> [<id>]
        ''')
    parser.add_argument('path', help="Model path")
    parser.add_argument('id', help="Model ID", default=None, nargs='?')
    args = parser.parse_args(sys.argv[2:])
    cli = makinas.Client()
    model = tf.saved_model.load(args.path)
    id = cli.push_model(model, args.id)
    print("Uploaded model: "+id)

def main():
    cmds = {
        'push': push,
        'pull': pull
    }
    parser = argparse.ArgumentParser(description='Makinas CLI Tool',
        usage=execname + ''' <command> [<args>]

Command list:
    push        Push trained model to Makinas
    pull        Pull a model from Makinas
''')
    parser.add_argument('command', help='Subcommand to execute', choices=cmds.keys())

    args = parser.parse_args(sys.argv[1:2])
    if args.command not in cmds:
        print('Unknown command')
        parser.print_help()
        exit(1)
    else:
        cmds[args.command]()
