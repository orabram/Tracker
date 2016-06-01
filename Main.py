# region -------------Info------------
# Name: http file server
# Version: 1.0
# By: Or Abramovich
# endregion -------------Info------------

# region -------------Imports---------
import ConnectionHandler
# endregion -------------Imports---------

# region -------------Constants-------

# endregion -------------Constants-------

# region -------------Methods---------

# endregion -------------Methods---------

# region -------------Main------------


def main():
    connection_handler = ConnectionHandler.ConnectionHandler()
    while True:
        connection_handler.handle_connections()


if __name__ == '__main__':
    main()
# endregion -------------Main------------
