namespace Bittorrent_Client
{
    partial class Client
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
            this.browser = new System.Windows.Forms.Button();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.Download = new System.Windows.Forms.Button();
            this.FileLocation = new System.Windows.Forms.TextBox();
            this.StatusBox = new System.Windows.Forms.RichTextBox();
            this.SuspendLayout();
            // 
            // browser
            // 
            this.browser.Location = new System.Drawing.Point(136, 160);
            this.browser.Name = "browser";
            this.browser.Size = new System.Drawing.Size(75, 23);
            this.browser.TabIndex = 0;
            this.browser.Text = "Browse";
            this.browser.UseVisualStyleBackColor = true;
            this.browser.Click += new System.EventHandler(this.browser_Click);
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.FileName = "openFileDialog1";
            // 
            // Download
            // 
            this.Download.Location = new System.Drawing.Point(410, 160);
            this.Download.Name = "Download";
            this.Download.Size = new System.Drawing.Size(75, 23);
            this.Download.TabIndex = 1;
            this.Download.Text = "Download";
            this.Download.UseVisualStyleBackColor = true;
            this.Download.Click += new System.EventHandler(this.Download_Click);
            // 
            // FileLocation
            // 
            this.FileLocation.Location = new System.Drawing.Point(136, 62);
            this.FileLocation.Name = "FileLocation";
            this.FileLocation.Size = new System.Drawing.Size(349, 20);
            this.FileLocation.TabIndex = 2;
            // 
            // StatusBox
            // 
            this.StatusBox.BackColor = System.Drawing.SystemColors.Menu;
            this.StatusBox.Location = new System.Drawing.Point(111, 284);
            this.StatusBox.Name = "StatusBox";
            this.StatusBox.ReadOnly = true;
            this.StatusBox.Size = new System.Drawing.Size(402, 135);
            this.StatusBox.TabIndex = 3;
            this.StatusBox.Text = "";
            // 
            // Client
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(685, 521);
            this.Controls.Add(this.StatusBox);
            this.Controls.Add(this.FileLocation);
            this.Controls.Add(this.Download);
            this.Controls.Add(this.browser);
            this.Name = "Client";
            this.Text = "Form1";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button browser;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
        private System.Windows.Forms.Button Download;
        private System.Windows.Forms.TextBox FileLocation;
        private System.Windows.Forms.RichTextBox StatusBox;
    }
}

