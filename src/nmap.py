import nmap

nm = nmap.PortScanner()
nm.scan(hosts='192.168.0.0/24', arguments='-sn')  # -sn = ping scan

for host in nm.all_hosts():
    print(f"{host} ({nm[host].hostname()}): {nm[host]['status']['state']}")