using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;


namespace Bittorrent_Client
{
    public partial class Client : Form
    {
        public Client()
        {
            InitializeComponent();
        }

        private void browser_Click(object sender, EventArgs e)
        {
            DialogResult result = openFileDialog1.ShowDialog();
            if (result == DialogResult.OK) // Test result.
            {
                FileLocation.Text = openFileDialog1.FileName;
            }

        }

        private void Download_Click(object sender, EventArgs e)
        {
            SocketClient socket = new SocketClient();
            socket.Connect();
            socket.Send(FileLocation.Text);
            StatusBox.Text = socket.Recv();
            StatusBox.Text = socket.Recv();       

        }
    }
}
