﻿namespace Tracker_GUI
{
    partial class TrackerGui
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.SeedersList = new System.Windows.Forms.ListBox();
            this.AddSeeder = new System.Windows.Forms.Button();
            this.AddFile = new System.Windows.Forms.Button();
            this.folderBrowserDialog1 = new System.Windows.Forms.FolderBrowserDialog();
            this.IP = new System.Windows.Forms.TextBox();
            this.Port = new System.Windows.Forms.TextBox();
            this.IPLabel = new System.Windows.Forms.Label();
            this.PortLabel = new System.Windows.Forms.Label();
            this.SeederData = new System.Windows.Forms.RichTextBox();
            this.SendFile = new System.Windows.Forms.Button();
            this.FileLocation = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.RemoveSeeder = new System.Windows.Forms.Button();
            this.ErrorBox = new System.Windows.Forms.RichTextBox();
            this.Mark = new System.Windows.Forms.Button();
            this.RemoveFile = new System.Windows.Forms.Button();
            this.Unmark = new System.Windows.Forms.Button();
            this.Shuffle = new System.Windows.Forms.Button();
            this.RefreshButton = new System.Windows.Forms.Button();
            this.Info = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // SeedersList
            // 
            this.SeedersList.FormattingEnabled = true;
            this.SeedersList.Location = new System.Drawing.Point(513, 44);
            this.SeedersList.Name = "SeedersList";
            this.SeedersList.SelectionMode = System.Windows.Forms.SelectionMode.MultiExtended;
            this.SeedersList.Size = new System.Drawing.Size(332, 277);
            this.SeedersList.TabIndex = 0;
            this.SeedersList.SelectedIndexChanged += new System.EventHandler(this.SeedersList_SelectedIndexChanged);
            // 
            // AddSeeder
            // 
            this.AddSeeder.Location = new System.Drawing.Point(183, 134);
            this.AddSeeder.Name = "AddSeeder";
            this.AddSeeder.Size = new System.Drawing.Size(75, 23);
            this.AddSeeder.TabIndex = 1;
            this.AddSeeder.Text = "Add";
            this.AddSeeder.UseVisualStyleBackColor = true;
            this.AddSeeder.Click += new System.EventHandler(this.AddSeeder_Click);
            // 
            // AddFile
            // 
            this.AddFile.Location = new System.Drawing.Point(87, 321);
            this.AddFile.Name = "AddFile";
            this.AddFile.Size = new System.Drawing.Size(75, 23);
            this.AddFile.TabIndex = 2;
            this.AddFile.Text = "Browse";
            this.AddFile.UseVisualStyleBackColor = true;
            this.AddFile.Click += new System.EventHandler(this.AddFile_Click);
            // 
            // IP
            // 
            this.IP.Location = new System.Drawing.Point(62, 75);
            this.IP.Name = "IP";
            this.IP.Size = new System.Drawing.Size(100, 20);
            this.IP.TabIndex = 3;
            // 
            // Port
            // 
            this.Port.Location = new System.Drawing.Point(282, 75);
            this.Port.Name = "Port";
            this.Port.Size = new System.Drawing.Size(100, 20);
            this.Port.TabIndex = 4;
            // 
            // IPLabel
            // 
            this.IPLabel.AutoSize = true;
            this.IPLabel.Location = new System.Drawing.Point(59, 59);
            this.IPLabel.Name = "IPLabel";
            this.IPLabel.Size = new System.Drawing.Size(20, 13);
            this.IPLabel.TabIndex = 5;
            this.IPLabel.Text = "IP:";
            // 
            // PortLabel
            // 
            this.PortLabel.AutoSize = true;
            this.PortLabel.Location = new System.Drawing.Point(279, 59);
            this.PortLabel.Name = "PortLabel";
            this.PortLabel.Size = new System.Drawing.Size(29, 13);
            this.PortLabel.TabIndex = 6;
            this.PortLabel.Text = "Port:";
            // 
            // SeederData
            // 
            this.SeederData.Location = new System.Drawing.Point(937, 44);
            this.SeederData.Name = "SeederData";
            this.SeederData.ReadOnly = true;
            this.SeederData.Size = new System.Drawing.Size(322, 277);
            this.SeederData.TabIndex = 7;
            this.SeederData.Text = "";
            // 
            // SendFile
            // 
            this.SendFile.Location = new System.Drawing.Point(193, 321);
            this.SendFile.Name = "SendFile";
            this.SendFile.Size = new System.Drawing.Size(75, 23);
            this.SendFile.TabIndex = 8;
            this.SendFile.Text = "Send";
            this.SendFile.UseVisualStyleBackColor = true;
            this.SendFile.Click += new System.EventHandler(this.SendFile_Click);
            // 
            // FileLocation
            // 
            this.FileLocation.Location = new System.Drawing.Point(62, 283);
            this.FileLocation.Name = "FileLocation";
            this.FileLocation.Size = new System.Drawing.Size(342, 20);
            this.FileLocation.TabIndex = 9;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(59, 256);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(116, 13);
            this.label1.TabIndex = 10;
            this.label1.Text = "Enter the file\'s location:";
            // 
            // RemoveSeeder
            // 
            this.RemoveSeeder.Location = new System.Drawing.Point(760, 371);
            this.RemoveSeeder.Name = "RemoveSeeder";
            this.RemoveSeeder.Size = new System.Drawing.Size(75, 23);
            this.RemoveSeeder.TabIndex = 11;
            this.RemoveSeeder.Text = "Remove";
            this.RemoveSeeder.UseVisualStyleBackColor = true;
            this.RemoveSeeder.Click += new System.EventHandler(this.RemoveSeeder_Click);
            // 
            // ErrorBox
            // 
            this.ErrorBox.Location = new System.Drawing.Point(937, 349);
            this.ErrorBox.Name = "ErrorBox";
            this.ErrorBox.ReadOnly = true;
            this.ErrorBox.Size = new System.Drawing.Size(322, 96);
            this.ErrorBox.TabIndex = 12;
            this.ErrorBox.Text = "";
            // 
            // Mark
            // 
            this.Mark.Location = new System.Drawing.Point(87, 371);
            this.Mark.Name = "Mark";
            this.Mark.Size = new System.Drawing.Size(75, 23);
            this.Mark.TabIndex = 13;
            this.Mark.Text = "Encrypt";
            this.Mark.UseVisualStyleBackColor = true;
            this.Mark.Click += new System.EventHandler(this.Mark_Click);
            // 
            // RemoveFile
            // 
            this.RemoveFile.Location = new System.Drawing.Point(307, 321);
            this.RemoveFile.Name = "RemoveFile";
            this.RemoveFile.Size = new System.Drawing.Size(75, 23);
            this.RemoveFile.TabIndex = 14;
            this.RemoveFile.Text = "Remove";
            this.RemoveFile.UseVisualStyleBackColor = true;
            this.RemoveFile.Click += new System.EventHandler(this.RemoveFile_Click);
            // 
            // Unmark
            // 
            this.Unmark.Location = new System.Drawing.Point(193, 371);
            this.Unmark.Name = "Unmark";
            this.Unmark.Size = new System.Drawing.Size(75, 23);
            this.Unmark.TabIndex = 15;
            this.Unmark.Text = "Decrypt";
            this.Unmark.UseVisualStyleBackColor = true;
            this.Unmark.Click += new System.EventHandler(this.Unmark_Click);
            // 
            // Shuffle
            // 
            this.Shuffle.Location = new System.Drawing.Point(307, 371);
            this.Shuffle.Name = "Shuffle";
            this.Shuffle.Size = new System.Drawing.Size(75, 23);
            this.Shuffle.TabIndex = 16;
            this.Shuffle.Text = "Shuffle";
            this.Shuffle.UseVisualStyleBackColor = true;
            // 
            // RefreshButton
            // 
            this.RefreshButton.Location = new System.Drawing.Point(638, 371);
            this.RefreshButton.Name = "RefreshButton";
            this.RefreshButton.Size = new System.Drawing.Size(75, 23);
            this.RefreshButton.TabIndex = 17;
            this.RefreshButton.Text = "Refresh";
            this.RefreshButton.UseVisualStyleBackColor = true;
            this.RefreshButton.Click += new System.EventHandler(this.RefreshButton_Click);
            // 
            // Info
            // 
            this.Info.Location = new System.Drawing.Point(513, 371);
            this.Info.Name = "Info";
            this.Info.Size = new System.Drawing.Size(75, 23);
            this.Info.TabIndex = 18;
            this.Info.Text = "Info";
            this.Info.UseVisualStyleBackColor = true;
            this.Info.Click += new System.EventHandler(this.Info_Click);
            // 
            // TrackerGui
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1271, 469);
            this.Controls.Add(this.Info);
            this.Controls.Add(this.RefreshButton);
            this.Controls.Add(this.Shuffle);
            this.Controls.Add(this.Unmark);
            this.Controls.Add(this.RemoveFile);
            this.Controls.Add(this.Mark);
            this.Controls.Add(this.ErrorBox);
            this.Controls.Add(this.RemoveSeeder);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.FileLocation);
            this.Controls.Add(this.SendFile);
            this.Controls.Add(this.SeederData);
            this.Controls.Add(this.PortLabel);
            this.Controls.Add(this.IPLabel);
            this.Controls.Add(this.Port);
            this.Controls.Add(this.IP);
            this.Controls.Add(this.AddFile);
            this.Controls.Add(this.AddSeeder);
            this.Controls.Add(this.SeedersList);
            this.Name = "TrackerGui";
            this.Text = "System Monitor";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ListBox SeedersList;
        private System.Windows.Forms.Button AddSeeder;
        private System.Windows.Forms.Button AddFile;
        private System.Windows.Forms.FolderBrowserDialog folderBrowserDialog1;
        private System.Windows.Forms.TextBox IP;
        private System.Windows.Forms.TextBox Port;
        private System.Windows.Forms.Label IPLabel;
        private System.Windows.Forms.Label PortLabel;
        private System.Windows.Forms.RichTextBox SeederData;
        private System.Windows.Forms.Button SendFile;
        private System.Windows.Forms.TextBox FileLocation;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button RemoveSeeder;
        private System.Windows.Forms.RichTextBox ErrorBox;
        private System.Windows.Forms.Button Mark;
        private System.Windows.Forms.Button RemoveFile;
        private System.Windows.Forms.Button Unmark;
        private System.Windows.Forms.Button Shuffle;
        private System.Windows.Forms.Button RefreshButton;
        private System.Windows.Forms.Button Info;
    }
}

