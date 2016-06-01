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
            SocketClient socket = GlobalVariables.GetSocket();
            socket.Connect();
            Thread update_seeders_list = new Thread(RecvSeedersList);
            update_seeders_list.Start();
        }

        public delegate void ProcessMessage(string message);

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

        public void MessageParse(string message)
        {
            string[] temp = message.Split('#');
            if (temp[0] == "list")
            {
                if (this.SeedersList.InvokeRequired)
                {
                    ProcessMessage p = new ProcessMessage(MessageParse);
                    this.Invoke(p, new object[] { message });
                }
                else
                {
                    SeedersList.Items.Clear();
                }
                for (int i = 1; i < temp.Length; i++)
                {
                    if (this.SeedersList.InvokeRequired)
                    {
                        ProcessMessage p = new ProcessMessage(MessageParse);
                        this.Invoke(p, new object[] { message });
                    }
                    else
                    {
                        if (!SeedersList.Items.Contains(temp[i]))
                        {
                            SeedersList.Items.Add(temp[i]);
                        }
                    }
                }
            }
            else if (temp[0] == "info")
            {
                if (this.SeederData.InvokeRequired)
                {
                    ProcessMessage p = new ProcessMessage(MessageParse);
                    this.Invoke(p, new object[] { message });
                }
                else
                {
                    SeederData.Text = temp[1];
                }
            }

            else if (temp[0] == "")
            {
                if (this.ErrorBox.InvokeRequired)
                {
                    ProcessMessage p = new ProcessMessage(MessageParse);
                    this.Invoke(p, new object[] { message });
                }
                else
                {
                    ErrorBox.Text = "Lost connection.";
                }
            }

            else
            {
                if (this.ErrorBox.InvokeRequired)
                {
                    ProcessMessage p = new ProcessMessage(MessageParse);
                    this.Invoke(p, new object[] { message });
                }
                else
                {
                    ErrorBox.Text = (temp[0]);
                }
            }
        }

        private void AddFile_Click(object sender, EventArgs e)
        {
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

        public void RecvSeedersList()
        {
            SocketClient socket = GlobalVariables.GetSocket();
            while (true)
            {
                string command = socket.Recv();
                MessageParse(command);
            }
        }

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
                string selected = SeedersList.GetItemText(SeedersList.SelectedItem);
                string message = "removes#" + selected;
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

        private void RefreshButton_Click(object sender, EventArgs e)
        {
            GlobalVariables.GetSocket().Send("refresh");
            MessageParse(GlobalVariables.GetSocket().Recv());
        }

        private void Info_Click(object sender, EventArgs e)
        {
            GlobalVariables.GetSocket().Send("info#" + IP.Text);
            SeederData.Text = GlobalVariables.GetSocket().Recv();

        }

        private void Mark_Click(object sender, EventArgs e)
        {
            if (FileLocation.Text == "")
            {
                ErrorBox.Text = "The location you've entered is invalid.";
            }
            else
            {
                string message = "mark" + "#" + FileLocation.Text;
                GlobalVariables.GetSocket().Send(message);
                message = GlobalVariables.GetSocket().Recv();
                MessageParse(message);
            }
        }

        private void Unmark_Click(object sender, EventArgs e)
        {
            if (FileLocation.Text == "")
            {
                ErrorBox.Text = "The location you've entered is invalid.";
            }
            else
            {
                string message = "unmark" + "#" + FileLocation.Text;
                GlobalVariables.GetSocket().Send(message);
                message = GlobalVariables.GetSocket().Recv();
                MessageParse(message);
            }
        }
    }
}
