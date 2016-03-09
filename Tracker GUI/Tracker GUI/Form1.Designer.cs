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
            this.SuspendLayout();
            // 
            // SeedersList
            // 
            this.SeedersList.FormattingEnabled = true;
            this.SeedersList.Items.AddRange(new object[] {
            "a",
            "b",
            "c"});
            this.SeedersList.Location = new System.Drawing.Point(448, 43);
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
            // TrackerGui
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(838, 491);
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
    }
}

