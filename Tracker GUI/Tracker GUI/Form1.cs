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
        delegate void SetTextCallback(string text);

        public TrackerGui()
        {
            InitializeComponent();
            SocketClient socket = GlobalVariables.GetSocket();
            socket.Connect();
            /*Thread update_seeders_list = new Thread(RecvSeedersList);
            update_seeders_list.Start();*/
        }
        
        public bool CheckIP()
        {
            if (IP.Text.Split('.').Length != 4)
            {
                ErrorBox.Text = "The IP address is invalid.";
                return false;
            }
            else if (Port.Text.Length > 5)
            {
                ErrorBox.Text = "The Port you've entered is invalid.";
                return false;
            }
            return true;
        }

        private void SetText(string text)
        {
            // InvokeRequired required compares the thread ID of the
            // calling thread to the thread ID of the creating thread.
            // If these threads are different, it returns true.
            if (this.ErrorBox.InvokeRequired)
            {
                SetTextCallback d = new SetTextCallback(SetText);
                this.Invoke(d, new object[] { text });
            }
            else
            {
                this.ErrorBox.Text = text;
            }
        }


        public void MessageParse(string message)
        {
            string[] temp = message.Split('#');
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
            else
            {
                SetText(temp[1]);
            }
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
        /*public void RecvSeedersList()
        {
            SocketClient socket = GlobalVariables.GetSocket();
            while (true)
            {
                string command = socket.Recv();
                MessageParse(command);
            }
        }
        */
        private void AddSeeder_Click(object sender, EventArgs e)
        {
            if (CheckIP())
            {
                string message = "adds#" + IP.Text + "#" + Port.Text;
                GlobalVariables.GetSocket().Send(message);
            }
            
        }

        private void RemoveSeeder_Click(object sender, EventArgs e)
        {
            if (CheckIP())
            {
                string message = "removes#" + IP.Text;
                GlobalVariables.GetSocket().Send(message);
                message = GlobalVariables.GetSocket().Recv();
                MessageParse(message);
            }
        }

        private void SendFile_Click(object sender, EventArgs e)
        {
            if (FileLocation.Text == "")
            {
                ErrorBox.Text = "The location you've entered is invalid.";
            }
            else
            {
                string message = "addf" + "#" + FileLocation.Text;
                GlobalVariables.GetSocket().Send(message);
                message = GlobalVariables.GetSocket().Recv();
                MessageParse(message);
            }
        }

        private void RemoveFile_Click(object sender, EventArgs e)
        {
            if (FileLocation.Text == "")
            {
                ErrorBox.Text = "The location you've entered is invalid.";
            }
            else
            {
                string message = "removef" + "#" + FileLocation.Text;
                GlobalVariables.GetSocket().Send(message);
                message = GlobalVariables.GetSocket().Recv();
                MessageParse(message);
            }
        }
    }
}
