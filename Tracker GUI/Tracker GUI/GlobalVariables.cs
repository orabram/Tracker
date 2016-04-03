using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tracker_GUI
{
    class GlobalVariables
    {
        private static SocketClient socket = new SocketClient();

        private GlobalVariables()
        {

        }

        public static SocketClient GetSocket()
        {
            return socket;
        }
    }

}
