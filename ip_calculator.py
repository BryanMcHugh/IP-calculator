# Calculator for finding various information related to IPv4 addresses.
classes={
    'A':{
        'network_bits':7,
        'host_bits':24
    },
    'B':{
        'network_bits':14,
        'host_bits':16
    },
    'C':{
        'network_bits':21,
        'host_bits':8
    },
    'D':{
        'network_bits':'N/A',
        'host_bits':'N/A'
    },
    'E':{
        'network_bits':'N/A',
        'host_bits':'N/A'
    },
}

# Converts decimal IPv4 addresses to binary.
def dec_to_bin(ip_addr):
    ip_addr = ip_addr.split(".")
    ip_bin = []
    for i in ip_addr:
        binary = []
        j = int(i)
        if j == 0:
            ip_bin.append("00000000")
        else:
            while j > 0:
                binary.insert(0, str(j%2))
                j //= 2
            if len(binary) < 8:
            	for i in range(8-len(binary)):
            		binary.insert(0, "0")

            ip_bin.append("".join(binary))
    ip_bin = ".".join(ip_bin)
    return ip_bin

# Converts binary IPv4 addresses to decimal.
def bin_to_dec(ip_bin):
    ip_bin = ip_bin.split(".")
    ip_addr = []
    powers = [7, 6, 5, 4, 3, 2, 1, 0]
    for i in ip_bin:
        decimal = 0
        pwr = 0
        for j in i:
            if j == "1":
                decimal += 2**powers[pwr]
            pwr += 1
        ip_addr.append(str(decimal))
    ip_addr = ".".join(ip_addr)
    return ip_addr

# Checks what class the IPv4 address belongs to.
def ip_class(ip_bin):
    ip_classes = "ABCDE"
    for i in range(4):
        if ip_bin[i] == "0":
            break
    return ip_classes[i]

# Finds the first address in chosen IPv4 address' class.
def first_ip(ip_bin):
	first = ""
	p = 0
	for i in ip_bin:
	    if p == 0:
	        if i == "0":
	            first += "0"
	            p = 1
	        else:
	            first += "1"
	    else:
	        if i == ".":
	            first += "."
	        else:
	            first += "0"
	return first

# Finds the last address in chosen IPv4 address' class.
def last_ip(ip_bin):
	last = ""
	p = 0
	for i in ip_bin:
	    if p == 0:
	        if i == "0":
	            last += "0"
	            p = 1
	        else:
	            last += "1"
	    else:
	        if i == ".":
	            last += "."
	        else:
	            last += "1"
	return last

# Finds the number of subnets on the network.
def subnet_bits(subnet_bin, ip_cls):
	if ip_cls == "A" or ip_cls == "B" or ip_cls == "C":
		del subnet_bin[0]
	if ip_cls == "B" or ip_cls == "C":
		del subnet_bin[0]
	if ip_cls == "C":
		del subnet_bin[0]
	subnets = 1
	for i in subnet_bin:
		for j in i:
			if j == "1":
				subnets *= 2
	return subnets

# Finds the number of addressable hosts per subnet.
def addressable_hosts(subnet_bin, ip_cls):
	if ip_cls == "C" or ip_cls == "B" or ip_cls == "A":
		del subnet_bin[0]
	if ip_cls == "B" or ip_cls == "A":
		del subnet_bin[0]
	if ip_cls == "A":
		del subnet_bin[0]
	hosts = 1
	for i in subnet_bin:
		for j in i:
			if j == "0":
				hosts *= 2
	return hosts - 2

# Finds the valid subnets of the IPv4 address.
def valid_subnets(ip_addr, subnet_mask):
    v_subnets = []
    for i in subnet_mask:
        if i == "255":
            del subnet_mask[0]
            
    for j in range(0, int(subnet_mask[0]), 64):
        ip_addr[(4 - len(subnet_mask)) + 1] = str(j)
        v_subnets.append(".".join(ip_addr))
    
    return v_subnets

# Finds the broadcast address of each subnet.
def broadcast_addresses(ip_addr, subnet_mask, ip_cls):
    v_addresses = []
    for i in subnet_mask:
        if i == "255":
            del subnet_mask[0]
    
    if ip_cls == "B" or ip_cls == "A":
        ip_addr[3] = "255"
    elif ip_cls == "A":
        ip_addr[2] = "255"
    
    for j in range(63, 256, 64):
        ip_addr[(4 - len(subnet_mask)) + 1] = str(j)
        v_addresses.append(".".join(ip_addr))
    
    return v_addresses

# Finds the first addresses of each valid host.
def first_addresses(ip_addr, subnet_mask, ip_cls):
    ft_addresses = []
    for i in subnet_mask:
        if i == "255":
            del subnet_mask[0]
    
    if ip_cls == "B" or ip_cls == "A":
        ip_addr[3] = "1"
    elif ip_cls == "A":
        ip_addr[2] = "1"
    
    for j in range(1, 194, 64):
        ip_addr[(4 - len(subnet_mask)) + 1] = str(j)
        ft_addresses.append(".".join(ip_addr))
    
    return ft_addresses

# Finds the last address of each valid host
def last_addresses(ip_addr, subnet_mask, ip_cls):
    lt_addresses = []
    for i in subnet_mask:
        if i == "255":
            del subnet_mask[0]
    
    if ip_cls == "B" or ip_cls == "A":
        ip_addr[3] = "254"
    elif ip_cls == "A":
        ip_addr[2] = "254"
    
    for j in range(62, 255, 64):
        ip_addr[(4 - len(subnet_mask)) + 1] = str(j)
        lt_addresses.append(".".join(ip_addr))
    
    return lt_addresses

# Compiles and outputs information regarding class stats.
def get_class_stats(ip_addr):
    ip_bin = dec_to_bin(ip_addr)
    ip_cls = ip_class(ip_bin)
    ip_ft = bin_to_dec(first_ip(ip_bin))
    ip_lt = bin_to_dec(last_ip(ip_bin))
    
    if classes[ip_cls]["network_bits"] != "N/A":
        networks = str(2 ** int(classes[ip_cls]["network_bits"]))
    else:
        networks = "N/A"
        
    if classes[ip_cls]["host_bits"] != "N/A":
        hosts = str(2 ** int(classes[ip_cls]["host_bits"]))
    else:
        hosts = "N/A"
        
    print("Class: " + ip_cls)
    print("Network: " + networks)
    print("Host: " + hosts)
    print("First address: " + ip_ft)
    print("Last address: " + ip_lt)
    start()

# Compiles and outputs information regarding subnet stats.
def get_subnet_stats(ip_addr, subnet_mask):
    subnet_bin = dec_to_bin(subnet_mask)
    ip_cls = ip_class(dec_to_bin(ip_addr))
    bits = str(len([i for i in subnet_bin if i == "1"]))
    subnets = str(subnet_bits(subnet_bin.split("."), ip_cls))
    hosts = str(addressable_hosts(subnet_bin.split("."), ip_cls))
    v_subnets = valid_subnets(ip_addr.split("."), subnet_mask.split("."))
    b_addresses = broadcast_addresses(ip_addr.split("."), subnet_mask.split("."), ip_cls)
    ft_addresses = first_addresses(ip_addr.split("."), subnet_mask.split("."), ip_cls)
    lt_addresses = last_addresses(ip_addr.split("."), subnet_mask.split("."), ip_cls)

    print("Address: " + ip_addr + "/" + bits)
    print("Subnets: " + subnets)
    print("Addressable hosts per subnet: " + hosts)
    print("Valid subnets: " + str(v_subnets))
    print("Broadcast addresses: " + str(b_addresses))
    print("First addresses: " + str(ft_addresses))
    print("Last addresses: " + str(lt_addresses))
    start()

# Compiles and outputs information regarding subnet stats.
def get_supernet_stats(addresses):
    bin_addresses = [dec_to_bin(i) for i in addresses]
    cidr = bin_addresses[0]
    for i in bin_addresses:
        maybe_cidr = []
        for j in range(len(cidr)):
            if i[j] == cidr[j]:
                maybe_cidr.append(str(i[j]))
            else:
                break
        cidr = maybe_cidr
    
    true_cidr = len([k for k in cidr if k != "."])
    supernet_mask = ["1","1","1","1","1","1","1","1",".","1","1","1","1","1","1","1","1",".","1","1","1","1","1","1","1","1",".","1","1","1","1","1","1","1","1"]
    
    for k in range(len(cidr), 35):
        if supernet_mask[k] == "1":
            supernet_mask[k] = "0"
    supernet_mask = bin_to_dec("".join(supernet_mask))
    
    p = 0
    for x in supernet_mask.split("."):
        p+=1
        if x != "255":
            x = 256-int(x)
            break
    
    # This will find the first subnet
    if x > len(addresses):
        first_subnet = addresses[0].split(".")
        test_subnet = addresses[0].split(".")
        z = x - len(addresses)
        if int(first_subnet[p]) % 2 == 1:
            if z % 2 == 1:
                for y in range(z):
                    if int(test_subnet[p]) - y == 0:
                        first_subnet[p] = "0"
                        break
                    first_subnet[p] = str(int(first_subnet[p]) - y)
            if z % 2 == 0:
                for y in range(z-1):
                    if int(test_subnet[p]) - y == 0:
                        first_subnet[p] = "0"
                        break
                    first_subnet[p] = str(int(first_subnet[p]) - y)
        else:
            if z % 2 == 1:
                for y in range(z-1):
                    if int(test_subnet[p]) - y == 0:
                        first_subnet[p] = "0"
                        break
                    first_subnet[p] = str(int(first_subnet[p]) - y)
            if z % 2 == 0:
                for y in range(z):
                    if int(test_subnet[p]) - y == 0:
                        first_subnet[p] = "0"
                        break
                    first_subnet[p] = str(int(first_subnet[p]) - y)
        addresses[0] = ".".join(first_subnet)

    print("Address: " + addresses[0] + "/" + str(true_cidr))
    print("Network mask: " + supernet_mask)
    start()

# Checks if the entry is a valid IPv4 address.
def check_ip(ip_addr):
    ip = ip_addr.split(".")
    if len(ip) != 4:
        print("\nInvalid entry. Please read help to see the acceptable entries.\n")
        start()
    else:
        for i in ip:
            if int(i) < 0 or int(i) > 256:
                print("\nInvalid entry. Please read help to see the acceptable entries.\n")
                start()

# Checks if subnet mask is valid for the class of IPv4 address entered.
def check_mask(ip_cls, subnet_mask):
    if ip_cls == "D" or ip_cls == "E":
        print("\nInvalid IPv4 address used. Cannot get subnet stats of class D or E IPv4 address")

    if subnet_mask[0] != "255":
        print("\nInvalid subnet mask for class of IPv4 address found.\n")
        start()
    
    if (ip_cls == "B" and subnet_mask[1] != "255") or (ip_cls == "c" and subnet_mask[1] != "255"):
        print("\nInvalid subnet mask for class of IPv4 address found.\n")
        start()
        
    if ip_cls == "C" and subnet_mask[2] != "255":
        print("\nInvalid subnet mask for class of IPv4 address found.\n")
        start()

def start():
    n = input("\nEnter command to start or enter help for list of acceptable commands:\n")
    if n == "help":
        print("\nThese are the commands that can be entered:\n"
        "\nIf you want information regarding class stats of an IPv4 address,\n"
        "please enter a valid IPv4 address. E.g. 136.206.18.7\n"
        "\nIf you want information regarding subnet stats of an IPv4 address, please enter subnet,\n"
        "the program will then prompt you to enter a valid class A through C IPv4 address followed by a subnet_mask\n"
        "\nIf you want information regarding supernet stats of a list of IPv4 addresses,\n"
        "please enter supernet, the program will then prompt you to enter a valid IPv4 address.\n"
        "You may keep entering addresses until you enter done which will done which will continue the program.\n"
        "\nTo exit the program enter exit.\n")
        start()

    elif n == "subnet":
        ip_addr = str(input("IPv4 Address: "))
        subnet_mask = str(input("Subnet mask: "))
        check_ip(ip_addr)
        check_ip(subnet_mask)
        check_mask(ip_class(dec_to_bin(ip_addr)), subnet_mask.split("."))
        get_subnet_stats(ip_addr, subnet_mask)
    
    elif n == "supernet":
        addresses = []
        ip_addr = str(input("IPv4 Address: "))
        check_ip(ip_addr)
        addresses.append(ip_addr)
        ip_cls1 = ip_class(dec_to_bin(ip_addr))
        ip_addr = str(input("IPv4 Address: "))
        while ip_addr != "done":
            check_ip(ip_addr)
            if ip_cls1 != ip_class(dec_to_bin(ip_addr)):
                print("\nInvalid entry. Please read help to see the acceptable entries.\n")
                start()
            else:
                addresses.append(ip_addr)
            ip_addr = str(input("IPv4 Address: "))
        get_supernet_stats(addresses)
        
    elif n == "exit":
        exit()
        
    else:
        check_ip(str(n))
        get_class_stats(str(n))

start()