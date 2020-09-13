#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>
#include <netinet/ether.h>
#include <netinet/ip_icmp.h>
#include <stdio.h>
#include <iostream>
#include <string>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <ostream>
#include <netdb.h>
#include <sys/param.h>
#include <netinet/in.h>
#include <time.h>
#include <regex>
#include <net/if.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <ifaddrs.h>
#include <pcap.h>
#include <byteswap.h>
#include <bits/stdc++.h>


using namespace std; 

#define PCKT_LEN 8192

// function for tcp header checksum
// source link: https://github.com/rbaron/raw_tcp_socket/blob/master/raw_tcp_socket.c?fbclid=IwAR2F9aeTIH5t_71gBgdx7i3gn4gdlhiC7J7T_yQonwrCnNJ8mjLetZ7nAts
unsigned short csum_tcp(unsigned short *ptr,int nbytes) {
  long sum;
  unsigned short oddbyte;
  short answer;

  sum=0;
  while(nbytes>1) {
    sum+=*ptr++;
    nbytes-=2;
  }
  if(nbytes==1) {
    oddbyte=0;
    *((u_char*)&oddbyte)=*(u_char*)ptr;
    sum+=oddbyte;
  }

  sum = (sum>>16)+(sum & 0xffff);
  sum = sum + (sum>>16);
  answer=(short)~sum;

  return(answer);
}


// function to get all ports, divided by commas
vector<int> get_by_commas(string str)
{
vector<int> vect;

stringstream st(str);

int i;
while(st >> i) {
    vect.push_back(i);

    if(st.peek() == ',')
        st.ignore();
}

return vect;
}

// function to get all port, from range
vector<int> get_by_range(string str)
{
    vector<int> vect;
    vector<int> vect2;
    stringstream ss(str);

    int i;
    while(ss >> i) {
        vect.push_back(i);

        if(ss.peek() == '-')
            ss.ignore();
    }
    int range = vect.at(1) - vect.at(0);

    for(int i = vect.at(0);i <= vect.at(1) ; i++)
    {
        vect2.push_back(i);
    }

    return vect2;
}

// function for IP header chcecksum
// source link : https://www.tenouk.com/Module43a.html
unsigned short csum(unsigned short *buf, int nwords)
{ 
    unsigned long sum;
    for(sum=0; nwords>0; nwords--)
            sum += *buf++;
    sum = (sum >> 16) + (sum &0xffff);
    sum += (sum >> 16);
    return (unsigned short)(~sum);
}


char net_init(void)
{
    return 1; // nothing to do 
}


void net_deinit(void)
{
    // nothing to do
}

// function that return first IP addres of host
// source link : https://www.gamedev.net/forums/topic/671428-c-cross-platform-resolve-hostname-to-ip-library/
string net_dns_resolve(const char* hostname)
{
    struct addrinfo hints, *results, *item;
    int status;
    char ipstr[INET6_ADDRSTRLEN];


    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;


    if((status = getaddrinfo(hostname, NULL, &hints, &results)) != 0)
    {
        fprintf(stderr, "failed to resolve hostname \"%s\": %s\n", hostname, gai_strerror(status));
        exit(-1);
    }



    for(item = results; item != NULL; item = item->ai_next)
    {
        void* addr;
        const char* ipver;


        // get pointer to the address itself 
        // different fields in IPv4 and IPv6 
        if(item->ai_family == AF_INET)  // address is IPv4 
        {
            struct sockaddr_in* ipv4 = (struct sockaddr_in*)item->ai_addr;
            addr = &(ipv4->sin_addr);
            ipver = "IPv4";
        }
        else  // address is IPv6 
        {
            struct sockaddr_in6* ipv6 = (struct sockaddr_in6*)item->ai_addr;
            addr = &(ipv6->sin6_addr);
            ipver = "IPv6";
        }


        // convert IP to a string and return it
        inet_ntop(item->ai_family, addr, ipstr, sizeof ipstr);
        return ipstr;
    }
    freeaddrinfo(results);
}


// function that returns IPv4 of the interface
// source link: https://gist.github.com/edufelipe/6108057?fbclid=IwAR162K0dU_C59IPC_I34qRS2OIYLNQ_-QFSwtXGAFu-tRL-frUycxlwftSQ
string get_interface_IP(const char* interface)
{
    int fd;
    struct ifreq ifr;

    fd = socket(AF_INET, SOCK_DGRAM, 0);

    // I want to get an IPv4 IP address
    ifr.ifr_addr.sa_family = AF_INET;

    // I want IP address attached to "interface" 
    strncpy(ifr.ifr_name, interface, IFNAMSIZ-1);

    ioctl(fd, SIOCGIFADDR, &ifr);
    close(fd);
    return inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr)->sin_addr);
}

// function that returns IPv6 of the interface
// source link : https://stackoverflow.com/questions/33125710/how-to-get-ipv6-interface-address-using-getifaddr-function
string get_interface_IPV6(string interface)
{
    struct ifaddrs *ifa, *ifa_tmp;
    char addrs[50];

    if (getifaddrs(&ifa) == -1) {
        perror("getifaddrs failed");
        exit(-1);
    }

    ifa_tmp = ifa;
    while (ifa_tmp) {
        if ((ifa_tmp->ifa_addr) && ((ifa_tmp->ifa_addr->sa_family == AF_INET6))) {
            if (ifa_tmp->ifa_addr->sa_family == AF_INET6 && ifa_tmp->ifa_name == interface)
            {
                struct sockaddr_in6 *in6 = (struct sockaddr_in6*) ifa_tmp->ifa_addr;
                inet_ntop(AF_INET6, &in6->sin6_addr, addrs, sizeof(addrs));
                return addrs;
            }
        }
        ifa_tmp = ifa_tmp->ifa_next;
    }
}

// function that check if IP addres is IPv6
bool is_ipv6_address(const string& str)
{
    struct sockaddr_in6 sa;
    return inet_pton(AF_INET6, str.c_str(), &(sa.sin6_addr))!=0;
}


int main(int argc,char *argv[]){


bool ipv6 = false;
string addr; // destination addres
char buffer[PCKT_LEN];

srand(time(NULL)); // to always get new value from rand()
int sd;
char errbuf[PCAP_ERRBUF_SIZE];
string interface; // source addres
int ch=0; // temp
string arg_i; // interface
string arg_pt; // port dest TCP
string arg_pu; // port dest UDP
string arg_addr; 
int one = 1;
const int *val = &one;
int ICMP_cout = 0; // count ICMP packets in UDP

memset(buffer, 0, PCKT_LEN);



for(int i = 1; i<argc;i++)
{
    if (strcmp(argv[i],"-i") == 0)
    {
        if(argc != i+1) arg_i = argv[i+1]; else {cerr << "Wrong argument format!\n"; exit(10);}
        i++;
        if((i+1) >= argc) break;
    }
    else if (strcmp(argv[i],"-pt") == 0)
    {
        if(argc != i+1) arg_pt = argv[i+1]; else {cerr << "Wrong argument format!\n"; exit(10);}
        i++;
        if((i+1) >= argc) break;
    }
    else if (strcmp(argv[i],"-pu") == 0)
    {
        if(argc != i+1) arg_pu = argv[i+1]; else {cerr << "Wrong argument format!\n"; exit(10);}
        i++;
        if((i+1) >= argc) break;
    }
    else
    {
        if (argv[i][0] == '-') {
            cerr << "Wrong argument format!\n";
            exit(10);
        }
        else
        {
            arg_addr = argv[i];
        }
    }
}

if(arg_i[0]=='-' || arg_pt[0]=='-' || arg_pu[0]=='-') {cerr << "Wrong argument format!\n"; exit(10);}

if(arg_pu == "" && arg_pt == "")
{
    cerr << "PU and PT is not set!\n";
    exit(10);
}

// automaticly set interface if its not specified by argument
if(arg_i == "")
{
    struct ifaddrs *ifaddr, *ifa;

    if (getifaddrs(&ifaddr) == -1) 
    {
        return -1;
    }
    for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
        char protocol[IFNAMSIZ]  = {0};

        if (ifa->ifa_addr == NULL || ifa->ifa_addr->sa_family != AF_PACKET) continue;

        interface = get_interface_IP(ifa->ifa_name);

        // if I am working with localhost
        if(interface == "127.0.0.1" && addr == "127.0.0.1")
        {
            arg_i = ifa->ifa_name;
            break;
        }
        if(interface == "127.0.0.1") continue;
        arg_i = ifa->ifa_name;
        break;
    }
}


regex numbers_comma("^\\d+(,\\d+)*$"); // regex for numbers divided by comma

regex numbers_range("^[\\d]+[-][\\d]+$"); // regex for range numbers

regex ipv4("^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$"); //r egex to check if IP is IPv4


// check if destination is IP addres or hostname
if(regex_match(arg_addr,ipv4))
{
    addr = arg_addr;
    interface = get_interface_IP(arg_i.c_str());
}
else if(is_ipv6_address(arg_addr))
{
    cerr << " Sorry, program does not support IPv6!" <<endl;
    exit(-1);
    addr = arg_addr;
    interface = get_interface_IPV6(arg_i.c_str());
    ipv6 = true;
}
// if its a hostname I use net_dns_resolve to get IP of host
else
{
    net_init();
    addr = net_dns_resolve(arg_addr.c_str());
    net_deinit();

    if(regex_match(addr,ipv4))
    {
        interface = get_interface_IP(arg_i.c_str());
    }
    else if(is_ipv6_address(addr))
    {
        interface = get_interface_IPV6(arg_i.c_str());
        ipv6 = true;
    }
}


//test if "-pu" is in right format
vector<int> input;
vector<int> input_pt;
if(arg_pu != "")
{
    if(regex_match(arg_pu,numbers_comma))
    {
        input = get_by_commas(arg_pu);
    }
    else if (regex_match(arg_pu,numbers_range))
    {
        input = get_by_range(arg_pu);
    }
    else
    {
        cerr << "PU in wrong format!" << endl;
        exit(10);
    }
}

//test if "-pt" is in right format
if(arg_pt != "")
{
    if(regex_match(arg_pt,numbers_comma))
    {
        input_pt = get_by_commas(arg_pt);
    }
    else if (regex_match(arg_pt,numbers_range))
    {
        input_pt = get_by_range(arg_pt);
    }
    else
    {
        cerr << "PT in wrong format!" << endl;
        exit(10);
    }
}


cout << "PORT" << "                 " << "STATE" << endl;

//UDP ports testing
// source link: https://www.tenouk.com/Module43a.html
for(int i=0;i<input.size();i++)
{ 
    struct iphdr *ip = (struct iphdr *) buffer;
    struct udphdr *udp = (struct udphdr *) (buffer + sizeof(struct iphdr));
    struct sockaddr_in sin, din;

    //inicializacia pcap
    pcap_t *pcap = pcap_create(arg_i.c_str(), errbuf);
    pcap_set_immediate_mode(pcap,1);
    pcap_set_timeout(pcap, 500);
    pcap_setnonblock(pcap,1,errbuf);
    pcap_activate(pcap);

    memset(buffer, 0, PCKT_LEN);

    //open RAW socket
    sd = socket(PF_INET, SOCK_RAW, IPPROTO_UDP);
    if(sd < 0)
    {
        perror("socket() error");
        exit(1);
    }

    //set socket
    if(setsockopt(sd, IPPROTO_IP, IP_HDRINCL, val, sizeof(one)) < 0)
    {
        exit(1);
    }


    // The address family
    sin.sin_family = AF_INET;
    din.sin_family = AF_INET;
    // Port numbers
    din.sin_port = htons(input.at(i));
    // IP addresses
    sin.sin_addr.s_addr = inet_addr(interface.c_str());
    din.sin_addr.s_addr = inet_addr(addr.c_str());

    // IP header
    ip->ihl = 5;
    ip->version = 4;
    ip->tos = 16; // Low delay
    ip->tot_len = sizeof(struct iphdr) + sizeof(struct udphdr);
    ip->id = htons(54321);
    //ip->frag_off=0;
    ip->ttl = 64; // hops
    ip->protocol = 17; // UDP
    // Source IP address
    ip->saddr = inet_addr(interface.c_str());
    // The destination IP address
    ip->daddr = inet_addr(addr.c_str());

    // UDP header
    // Destination port number
    udp->dest = htons(input.at(i));
    udp->len = htons(sizeof(struct udphdr));
    // Calculate the checksum for integrity
    ip->check = csum((unsigned short *)buffer, sizeof(struct iphdr) + sizeof(struct udphdr));


    const u_char *packet;
    struct pcap_pkthdr packet_header;
    // creating filter for received packets
    struct bpf_program filter;
    string temp = "ip host " + interface;
    bpf_u_int32 subnet_mask, ipp;


    pcap_compile(pcap, &filter, temp.c_str(), 0, ipp);
    // setting filter
    pcap_setfilter(pcap, &filter);


    
    int count;
    ICMP_cout = 0;
    // send 3 packets
    for(count = 1; count <=3; count++)
    {
        if(sendto(sd, buffer, ip->tot_len, 0, (struct sockaddr *)&din, sizeof(din)) < 0)
        {
            perror("sendto() error");
            exit(1);
        }
        else
        {
            // capture packet
            packet = pcap_next(pcap, &packet_header);
            if (packet == NULL) 
            {
                continue;
            }
            struct ether_header *eth = (struct ether_header*)packet;
            struct iphdr *ip = (struct iphdr*)(packet + sizeof(struct ether_header));
            struct icmphdr *icmp = (struct icmphdr*)(packet + sizeof(struct ether_header) + sizeof(struct iphdr));
            
            // comparing type and code of packets 
            uint16_t tmp=ntohs(icmp->type);
            uint16_t tmp2=ntohs(icmp->code);

            // check if ist Little or Big endian 
            if ( htonl(47) == 47 ) {
                // nothing to do
                // Big endian
            } else {
                // byteswap to get actual value if Little endian
                tmp = bswap_16(tmp);
                tmp2 = bswap_16(tmp2);
            }

            // if its "3" they are ICMP packets
            if (tmp == 3 && tmp2 == 3)
            {
                ICMP_cout++;
            }
            usleep(100000);
        }
    }
    // print results on stdout
    if(ICMP_cout > 0)
    {
        cout << input.at(i) << "/udp"  << "               closed" << endl;
    }
    else if(ICMP_cout == 0)
    {
        cout << input.at(i) << "/udp"  << "               open" << endl;
    }
    else
    {
        cerr << "addres does not exist!";
        exit(1);
    }
    pcap_close(pcap);
}


// pseudo header for TCP header checksum
struct pseudoTcpHeader
    {
        u_int32_t ip_src;
        u_int32_t ip_dst;
        u_int8_t zero;
        u_int8_t protocol;
        u_int16_t tcp_len;
    };

// TCP ports testing
// source link : https://www.tenouk.com/Module43a.html
for(int i=0; i< input_pt.size();i++)
{
    struct iphdr *ip = (struct iphdr *) buffer;
    struct tcphdr *tcp = (struct tcphdr *) (buffer + sizeof(struct iphdr));
    struct sockaddr_in sin, din;
    char *pseudo_packet;

    struct pseudoTcpHeader pseudoHdr;
    memset(buffer, 0, PCKT_LEN);

    // inicialization pcap
    pcap_t *pcap = pcap_create(arg_i.c_str(), errbuf);
    pcap_set_immediate_mode(pcap,1);
    pcap_set_timeout(pcap, 1000);
    pcap_setnonblock(pcap,1,errbuf);
    pcap_activate(pcap);

    // open RAW socket
    sd = socket(PF_INET, SOCK_RAW, IPPROTO_TCP);
    if(sd < 0)
    {
        perror("socket() error");
        exit(1);
    }

    // set socket
    if(setsockopt(sd, IPPROTO_IP, IP_HDRINCL, val, sizeof(one)) < 0)
    {
        exit(1);
    }


    // The source is redundant, may be used later if needed
    // The address family
    sin.sin_family = AF_INET;
    din.sin_family = AF_INET;
    // Port numbers
    din.sin_port = htons(input_pt.at(i));
    // IP addresses
    sin.sin_addr.s_addr = inet_addr(interface.c_str());
    din.sin_addr.s_addr = inet_addr(addr.c_str());

    // IP header
    ip->ihl = 5;
    ip->version = 4;
    ip->tos = 16; // Low delay
    ip->tot_len = sizeof(struct iphdr) + sizeof(struct tcphdr);
    ip->id = htons(54321);
    ip->ttl = 64; // hops
    ip->protocol = 6; // TCP
    // Source IP address
    ip->saddr = inet_addr(interface.c_str());
    // The destination IP address
    ip->daddr = inet_addr(addr.c_str());
    // Source poer number (random generated)
    int src_p=(rand() % 8000+4000);
    tcp->source = htons(src_p);
    // The destination port
    tcp->dest = htons(input_pt.at(i));
    tcp->seq = htonl(rand() % 1000+10);
    tcp->ack_seq = 0;
    tcp->doff = 5;
    tcp->syn = 1;
    tcp->ack = 0;
    tcp->window = htons(32767);
    tcp->urg = 0;


    // Inicialization pseudo TCP header
    pseudoHdr.ip_src = inet_addr(interface.c_str());
    pseudoHdr.ip_dst = inet_addr(addr.c_str());
    pseudoHdr.zero = 0;
    pseudoHdr.protocol = IPPROTO_TCP;
    pseudoHdr.tcp_len = htons(sizeof(struct tcphdr));

    // allocking memory for pseudo packet
    // source link : https://github.com/rbaron/raw_tcp_socket/blob/master/raw_tcp_socket.c?fbclid=IwAR2F9aeTIH5t_71gBgdx7i3gn4gdlhiC7J7T_yQonwrCnNJ8mjLetZ7nAts
    pseudo_packet = (char *) malloc((int) (sizeof(struct pseudoTcpHeader) + sizeof(struct tcphdr)));
    memset(pseudo_packet, 0, sizeof(struct pseudoTcpHeader) + sizeof(struct tcphdr));

    memcpy(pseudo_packet, (char *) &pseudoHdr, sizeof(struct pseudoTcpHeader));

    memcpy(pseudo_packet + sizeof(struct pseudoTcpHeader), tcp, sizeof(struct tcphdr));
    // calculate checksum of tcp header
    tcp->check = (csum_tcp((unsigned short *) pseudo_packet, (int) (sizeof(struct pseudoTcpHeader) + sizeof(struct tcphdr))));

    // Calculate the checksum for integrity
    ip->check = csum((unsigned short *)buffer, sizeof(struct iphdr) + sizeof(struct tcphdr));

    const u_char *packet;
    struct pcap_pkthdr packet_header;
    // creating filter for received packets
    struct bpf_program filter;
    string temp = ("ip src host " +addr + " and dst host " + interface + " and src port "+to_string(input_pt.at(i))+" and dst port "+to_string(src_p));
    bpf_u_int32 subnet_mask, ipp;

    pcap_compile(pcap, &filter, temp.c_str(), 0, ipp);
    // setting filter
    pcap_setfilter(pcap, &filter);

    // sending packets
    if(sendto(sd, buffer, ip->tot_len, 0, (struct sockaddr *)&din, sizeof(din)) < 0)
        {
            perror("sendto() error");
            exit(1);
        }
        else
        {
            //capture incoming packet
            packet = pcap_next(pcap, &packet_header);
            if (packet == NULL) 
            {
                // if I dont received packet I try to sent another
                if(sendto(sd, buffer, ip->tot_len, 0, (struct sockaddr *)&din, sizeof(din)) < 0)
                {
                    perror("sendto() error");
                    exit(1);
                }
                else
                {
                    // if I still dont received any packet its "filtered" port
                    packet = pcap_next(pcap, &packet_header);
                    if (packet == NULL)
                    {
                        cout << input_pt.at(i) << "/tcp"  << "               filtered" << endl;
                    }
                    else
                    {
                        struct ether_header *eth = (struct ether_header*)packet;
                        struct iphdr *ip = (struct iphdr*)(packet + sizeof(struct ether_header));
                        struct tcphdr *tcp = (struct tcphdr*)(packet + sizeof(struct ether_header) + sizeof(struct iphdr));
                        // get SYN , ACK and RST flag value of received packet
                        uint16_t tmp=ntohs(tcp->syn);
                        uint16_t tmp2=ntohs(tcp->ack);
                        uint16_t tmp3=ntohs(tcp->rst);
                        
                        // check if ist Little or Big endian
                        if ( htonl(47) == 47 ) {
                            // nothing to do
                            // Big endian
                        } else {
                            // byteswap to get actual value if Little endian.
                            tmp = bswap_16(tmp);
                            tmp2 = bswap_16(tmp2);
                            tmp3 = bswap_16(tmp3);
                        }
                        // if I received SYN and ACK ist "open" port
                        if (tmp == 1 && tmp2 == 1)
                        {
                            cout << input_pt.at(i) << "/tcp"  << "               open" << endl;
                        }
                        // if I received ACK and RST ist "closed" port
                        if (tmp2 == 1 && tmp3 ==1)
                        {
                            cout << input_pt.at(i) << "/tcp"  << "               closed" << endl;
                        }
                        usleep(100000);
                    }
                }
            }
            else
            {
                struct ether_header *eth = (struct ether_header*)packet;
                struct iphdr *ip = (struct iphdr*)(packet + sizeof(struct ether_header));
                struct tcphdr *tcp = (struct tcphdr*)(packet + sizeof(struct ether_header) + sizeof(struct iphdr));
                // get SYN , ACK and RST flag value of received packet
                uint16_t tmp=ntohs(tcp->syn);
                uint16_t tmp2=ntohs(tcp->ack);
                uint16_t tmp3=ntohs(tcp->rst);
                
                // check if ist Little or Big endian
                if ( htonl(47) == 47 ) {
                    // nothing to do
                    // Big endian
                } else {
                    // byteswap to get actual value if Little endian.
                    tmp = bswap_16(tmp);
                    tmp2 = bswap_16(tmp2);
                    tmp3 = bswap_16(tmp3);
                }
                // if I received SYN and ACK ist "open" port
                if (tmp == 1 && tmp2 == 1)
                {
                    cout << input_pt.at(i) << "/tcp"  << "               open" << endl;
                }
                // if I received ACK and RST ist "closed" port
                if (tmp2 == 1 && tmp3 ==1)
                {
                    cout << input_pt.at(i) << "/tcp"  << "               closed" << endl;
                }
                usleep(100000);
            }

        }
    pcap_close(pcap);
}

close(sd);

return 0;
}