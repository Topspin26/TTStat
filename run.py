#!flask/bin/python
from ttstat import ttstat

if __name__ == '__main__':
    ttstat.run(debug=True, use_reloader=False)