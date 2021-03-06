import sys
import socket as mysoc

def getHostnameFromEntry(entry):
    splitEntry = entry.split(" ")
    entryHostname = splitEntry[0].strip("\n").strip("\r").strip()
    return entryHostname


def COMserver():
    DNS_Table_Name = sys.argv[1]
    fDNSCOMnames = open(DNS_Table_Name, "r")
    fDNSCOMList = fDNSCOMnames.readlines()
    inputEntries = []

    for entry in fDNSCOMList:
        inputEntries.append(entry.strip("\n"))

    try:
        com_socket=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{}\n'.format("COM socket open error %" % err))

    com_server_binding = ('', 51238)
    com_socket.bind(com_server_binding)
    com_socket.listen(1)
    hostname = mysoc.gethostname()
    com_host_ip = (mysoc.gethostbyname(hostname))
    print("%s" % hostname)
    rsockid,addr=com_socket.accept()

    while True:
        rs_data = rsockid.recv(100)
        if rs_data:
            if rs_data == "**//TERMINATE//**":
                break
        if rs_data:
            foundEntry = False
            rs_data = rs_data.strip("\n").strip("\r").strip()
            print("[COM:] Recieved: %s" % rs_data)

            for entry in inputEntries:
                entryHostname = getHostnameFromEntry(entry)

                if entryHostname == rs_data:
                    foundEntry = True
                    print("[COM:] Sending: %s" % entry)
                    rsockid.send(entry)
                    break
            if not foundEntry:
                error = rs_data + " - Error:HOST NOT FOUND"
                print("[COM:] Sending %s" % error)
                rsockid.send(error)

    print("[COM:] SOCKET CLOSED")
    com_socket.close()
    exit()

COMserver()
