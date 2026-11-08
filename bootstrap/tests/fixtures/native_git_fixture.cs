using System;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading;

internal static class NativeGitFixture
{
    private const string Version = "git version 2.53.0\n";
    private static readonly string Root = AppDomain.CurrentDomain.BaseDirectory;
    private static string ReadyEvent;
    private static string ReleaseEvent;

    private static bool HasArg(string[] args, string value)
    {
        foreach (string arg in args) if (arg == value) return true;
        return false;
    }

    private static void Mark(string name, string value)
    {
        File.WriteAllText(Path.Combine(Root, name), value, new UTF8Encoding(false));
    }

    private static string Mode()
    {
        string path = Path.Combine(Root, "control.txt");
        FileInfo info = new FileInfo(path);
        if (!info.Exists || info.Length > 256) throw new InvalidOperationException();
        string[] rows = File.ReadAllLines(path, Encoding.ASCII);
        if (rows.Length != 3 || !rows[1].StartsWith("ready=") ||
            !rows[2].StartsWith("release=")) throw new InvalidOperationException();
        ReadyEvent = rows[1].Substring(6);
        ReleaseEvent = rows[2].Substring(8);
        string value = rows[0].Trim();
        string[] allowed = { "ordinary", "version-hang", "config-hang", "stdout-flood",
            "stderr-flood", "hold-pipes", "quiet-descendant", "early-config-exit" };
        bool known = false;
        foreach (string mode in allowed) if (mode == value) known = true;
        if (!known) throw new InvalidOperationException();
        foreach (string name in new[] { ReadyEvent, ReleaseEvent })
        {
            if (name.Length == 0) continue;
            if (!name.StartsWith("CairnGit-") || name.Length != 41)
                throw new InvalidOperationException();
            for (int i = 9; i < name.Length; i++)
                if (!Uri.IsHexDigit(name[i])) throw new InvalidOperationException();
        }
        if ((value == "hold-pipes" || value == "quiet-descendant") && ReadyEvent.Length == 0)
            throw new InvalidOperationException();
        if (value == "quiet-descendant" && ReleaseEvent.Length == 0)
            throw new InvalidOperationException();
        return value;
    }

    private static void HoldChild(string readyEvent)
    {
        Mark("child.ready", Process.GetCurrentProcess().Id.ToString());
        using (EventWaitHandle ready = EventWaitHandle.OpenExisting(readyEvent)) ready.Set();
        while (true) Thread.Sleep(1000);
    }

    private static void StartChild(bool redirect)
    {
        string self = Process.GetCurrentProcess().MainModule.FileName;
        ProcessStartInfo start = new ProcessStartInfo(self, "--fixture-child " + ReadyEvent)
        {
            UseShellExecute = false,
            CreateNoWindow = true
        };
        if (redirect)
        {
            start.RedirectStandardInput = true;
            start.RedirectStandardOutput = true;
            start.RedirectStandardError = true;
        }
        Process child = Process.Start(start);
        if (child == null) throw new InvalidOperationException();
        if (redirect)
        {
            child.StandardInput.Close();
            child.StandardOutput.Close();
            child.StandardError.Close();
        }
        Mark("child.pid", child.Id.ToString());
        using (EventWaitHandle ready = EventWaitHandle.OpenExisting(ReadyEvent))
            if (!ready.WaitOne(3000)) throw new InvalidOperationException();
    }

    private static void Flood(Stream stream, int count, byte value)
    {
        byte[] block = new byte[8192];
        for (int i = 0; i < block.Length; i++) block[i] = value;
        while (count > 0)
        {
            int next = Math.Min(block.Length, count);
            stream.Write(block, 0, next);
            count -= next;
        }
        stream.Flush();
    }

    public static int Main(string[] args)
    {
        if (args.Length > 0 && args[0] == "--fixture-child")
        {
            if (args.Length != 2) return 8;
            HoldChild(args[1]);
            return 0;
        }
        string mode = Mode();
        string command = String.Join(" ", args);
        File.AppendAllText(Path.Combine(Root, "launches.txt"), command + "\n",
            new UTF8Encoding(false));

        if (HasArg(args, "--version"))
        {
            if (mode == "version-hang")
            {
                Mark("ready.txt", "version");
                Thread.Sleep(30000);
                return 0;
            }
            if (mode == "stdout-flood")
            {
                Mark("ready.txt", "stdout");
                Flood(Console.OpenStandardOutput(), 32768, (byte)'o');
                return 0;
            }
            if (mode == "stderr-flood")
            {
                Mark("ready.txt", "stderr");
                Flood(Console.OpenStandardError(), 131072, (byte)'e');
                Console.Write(Version);
                return 0;
            }
            Console.Write(Version);
            return 0;
        }

        if (HasArg(args, "--file") && HasArg(args, "--no-includes"))
        {
            if (mode == "config-hang")
            {
                Mark("ready.txt", "config");
                Thread.Sleep(30000);
                return 0;
            }
            if (mode == "early-config-exit")
            {
                Mark("ready.txt", "early-config");
                Console.Write("remote.origin.url\nhttps://example.invalid/repo.git\0");
                Console.Out.Flush();
                Console.OpenStandardInput().ReadByte();
                return 0;
            }
            MemoryStream input = new MemoryStream();
            Console.OpenStandardInput().CopyTo(input);
            Mark("config-eof.txt", input.Length.ToString());
            string text = Encoding.UTF8.GetString(input.ToArray());
            if (!text.Contains("[remote \"origin\"]") ||
                !text.Contains("https://example.invalid/repo.git")) return 9;
            Console.Write("remote.origin.url\nhttps://example.invalid/repo.git\0");
            return 0;
        }

        if (mode == "hold-pipes")
        {
            StartChild(false);
            return 0;
        }
        if (mode == "quiet-descendant")
        {
            StartChild(true);
            using (EventWaitHandle release = EventWaitHandle.OpenExisting(ReleaseEvent))
                release.WaitOne(5000);
        }

        if (mode == "ordinary")
        {
            int byteRead;
            do { byteRead = Console.OpenStandardInput().ReadByte(); }
            while (byteRead >= 0);
            Mark("ordinary-eof.txt", "eof");
            Console.WriteLine("true");
            return 0;
        }

        Console.WriteLine("true");
        return 0;
    }
}
