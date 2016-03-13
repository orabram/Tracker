namespace Tracker_GUI
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
            this.label1 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // SeedersList
            // 
            this.SeedersList.FormattingEnabled = true;
            this.SeedersList.Items.AddRange(new object[] {
            "a",
            "b",
            "c"});
            this.SeedersList.Location = new System.Drawing.Point(936, 43);
            this.SeedersList.Name = "SeedersList";
            this.SeedersList.Size = new System.Drawing.Size(332, 381);
            this.SeedersList.TabIndex = 0;
            // 
            // AddSeeder
            // 
            this.AddSeeder.Location = new System.Drawing.Point(182, 131);
            this.AddSeeder.Name = "AddSeeder";
            this.AddSeeder.Size = new System.Drawing.Size(75, 23);
            this.AddSeeder.TabIndex = 1;
            this.AddSeeder.Text = "Add";
            this.AddSeeder.UseVisualStyleBackColor = true;
            // 
            // AddFile
            // 
            this.AddFile.Location = new System.Drawing.Point(182, 317);
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
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(202, 275);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(35, 13);
            this.label1.TabIndex = 7;
            this.label1.Text = "label1";
            this.label1.Click += new System.EventHandler(this.label1_Click);
            // 
            // TrackerGui
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1271, 469);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.PortLabel);
            this.Controls.Add(this.IPLabel);
            this.Controls.Add(this.Port);
            this.Controls.Add(this.IP);
            this.Controls.Add(this.AddFile);
            this.Controls.Add(this.AddSeeder);
            this.Controls.Add(this.SeedersList);
            this.Name = "TrackerGui";
            this.Text = "Form1";
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
        private System.Windows.Forms.Label label1;
    }
}

