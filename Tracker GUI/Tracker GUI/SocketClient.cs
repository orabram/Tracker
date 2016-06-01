using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Net.Sockets;
using System.Net;
using System.Text;


public class SocketClient
{
    private Socket clientsocket;
    private TcpListener serverSocket;
    private TcpClient clientSocket;
    private byte[] buffer = new byte[4096]; // The amount of data

    public SocketClient()
    {
        serverSocket = new TcpListener(IPAddress.Parse("0.0.0.0"), 6666);
        clientSocket = default(TcpClient);
    }

    public bool Connect()
    {
        serverSocket.Start();
        try
        {
            clientSocket = serverSocket.AcceptTcpClient();
            serverSocket.Stop();
            this.clientsocket = clientSocket.Client;
            return true;
        }
        catch
        {
            return false;
        }

    }

    private byte[] Encode(string message) // Turning the message from string to byte[] to send it through the socket.
    {
        byte[] message2 = Encoding.UTF8.GetBytes(message); // Encoding the message
        return message2; // Returns the byte array.
    }

    public string Recv() // Decodes the incoming message from byte[] to string.
    {
        try
        {
            int message = this.clientsocket.Receive(buffer);
        }
        catch
        {
            return "";
        }
        string message2 = Encoding.ASCII.GetString(this.buffer, 0, message); // Decoding the message. 
        return message2; // Returns the string.
    }

    public void Send(string message) // Sends the message.
    {
        clientsocket.Send(Encode(message)); // Sends an encoded message.
    }
}