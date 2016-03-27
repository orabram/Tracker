using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;
using System.Threading;


namespace Tracker_GUI
{
    public partial class TrackerGui : Form
    {
        public TrackerGui()
        {
            InitializeComponent();
            SocketClient socket = new SocketClient();
            Thread update_seeders_list = new Thread(new ParameterizedThreadStart(RecvSeedersList));
            update_seeders_list.Start(socket);
            


        }

        private void AddFile_Click(object sender, EventArgs e)
        {
            /*Process p = new Process();
            p.StartInfo.FileName = "cmd.exe";
            p.StartInfo.Arguments = @"/C C:\Python27\python.exe " + Application.StartupPath + @"\server.py";
            p.Start(); // Starts the python program*/
            OpenFileDialog fDialog = new OpenFileDialog();
            fDialog.Title = "Choose a File";
            fDialog.InitialDirectory = @"C:\";
            if (fDialog.ShowDialog() == DialogResult.OK)
            {
                FileLocation.Text = fDialog.FileName.ToString();
            }
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void SeedersList_SelectedIndexChanged(object sender, EventArgs e)
        {
            if ((string)SeedersList.SelectedItem == "2")
                FileLocation.Text = ((string)SeedersList.SelectedItem);
        }
        public void RecvSeedersList(object oldsocket)
        {
            SocketClient socket = (SocketClient)oldsocket;
            while (true)
            {
                string command = socket.Recv();
                string[] temp = command.Split('#');
                if (temp[0] == "list")
                {
                    for (int i = 1; i < temp.Length; i++)
                    {
                        SeedersList.Items.Add(temp[i]);
                    }
                }
                else if (temp[0] == "info")
                {
                    SeederData.Text = temp[1];
                }
            }
        }

        private void AddSeeder_Click(object sender, EventArgs e)
        {
            if(IP.Text.Split('.').Length != 4)
            {
                ErrorBox.Text = "The IP address is invalid.";
            }
            else if(Port.Text.Length > 5)
            {
                ErrorBox.Text = "The Port you've entered is invalid.";
            }
            string message = "adds#" + IP.Text + Port.Text;
            
        }

        private void RemoveSeeder_Click(object sender, EventArgs e)
        {

        }

        private void SendFile_Click(object sender, EventArgs e)
        {

        }
    }
}
