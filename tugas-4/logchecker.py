import re
"""
Program to check the log to answer these questions:

1. Cetaklah pesan EHLO
Contoh output: 'ehlo 192.168.1.7\r\n'

2. Cetaklah pesan yang menyatakan bahwa server mendukung TLS
Contoh output: '250-STARTTLS\r\n'

3. Cetaklah pesan yang menyatakan server siap mengirim email
Contoh output: retcode (220); Msg: b'2.0.0 SMTP server ready'

4. Cetaklah pesan yang menunjukkan username yang sudah di-hash
Contoh output: 'AUTH LOGIN aHVkYW5AaXRzLmFxxxxx\r\n'

5. Cetaklah pesan balasan server dari sebuah hello message dari client
Contoh output: '250-SG2PR02CA0025.outlook.office365.com Hello [180.251.80.101]\r\n'

6. Cetaklah pesan bahwa koneksi telah ditutup 
Contoh output: '221 2.0.0 Service closing transmission channel\r\n'

"""

class Solution:
    def __init__(self, logfile):
        self.logfile = logfile
        self.log = self.readLog()
        self.log_per_line = self.log.split("\\n")
        self.lines = 5
        self.search_all = True
    
    def set_search_all(self, mode):
        self.search_all = mode

    def readLog(self):
        with open(self.logfile, "r") as f:
            return f.read()

    def printlines(self, num):
        print("-" * num)

    def nomor1(self):
        print("Nomor 1")
        for line in self.log_per_line:
            entry = re.search(r"ehlo.*\[(.*)\]\\r", line)
            if entry != None:
                print(f"ehlo {entry.group(1)}")
                if self.search_all == False:
                    break
        self.printlines(self.lines)


    def nomor2(self):
        print("Nomor 2")
        for line in self.log_per_line:
            entry = re.search(r"reply:[\sb']+(.*STARTTLS)\\r", line)
            if entry != None:
                print(entry.group(1))
                if self.search_all == False:
                    break
        self.printlines(self.lines)

    def nomor3(self):
        print("Nomor 3")
        for line in self.log_per_line:
            # entry = re.search(r"reply:[\sb']+(.*server ready)", line)
            entry = re.search(r"(retcode.*server ready)", line)
            if entry != None:
                print(entry.group(1))
                if self.search_all == False:
                    break
        self.printlines(self.lines)

    def nomor4(self):
        print("Nomor 4")
        for line in self.log_per_line:
            # entry = re.search(r"(AUTH LOGIN.*)\\r", line)
            entry = re.search(r"(AUTH LOGIN.{10,})\\r", line)
            if entry != None:
                print(entry.group(1))
                if self.search_all == False:
                    break
        self.printlines(self.lines)
        pass

    def nomor5(self):
        print("Nomor 5")
        for line in self.log_per_line:
            # entry = re.search(r"(AUTH LOGIN.*)\\r", line)
            entry = re.search(r"reply:[\sb']+(.*Hello \[.*\])\\r", line)
            if entry != None:
                print(entry.group(1))
                if self.search_all == False:
                    break
        self.printlines(self.lines)
        pass

    def nomor6(self):
        #Karena saat melakukan close tidak ada pesan pada debug level dan pada return function nya, maka kosongan
        pass

def main():
    solution = Solution("smtp_debug.log")
    solution.set_search_all(True)
    solution.nomor1()
    solution.nomor2()
    solution.nomor3()
    solution.nomor4()
    solution.nomor5()
    solution.nomor6()

if __name__ == "__main__":
    main()