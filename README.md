# Introdução

In the context of the Computer Communications course, a project was proposed aiming to implement a DNS (Domain Name System). Initially, it was crucial to comprehend DNS concepts and understand the workings of networks and communication among computers, servers, and clients. Creating a communication model that supported and fulfilled the project's requirements was essential.

This involved understanding and analyzing all necessary files to create a server and store essential information. These insights were crucial to solving problems and executing the requested tasks.

DNS, although used daily by us, often goes unnoticed by most users. It stands for Domain Name System, a registry containing records associating website names with their corresponding IP addresses.

Throughout this project, the architecture, information model, communication model, and necessary testing environment to implement a DNS system were presented. This project allowed for the exploration of infrastructure and fundamental processes enabling the translation of domain names into IP addresses, facilitating communication on the internet.
# System structure
The Primary Server is a DNS server that responds to and performs DNS queries, having direct access to the DNS domain database and managing it. This means that any necessary updates to the DNS domain information must be made directly in the Primary Server's database. Additionally, a Primary Server has access to its assigned domains, service ports, file identification of databases and log files, security information for database access, identification of respective Secondary Servers (SS) and Subdomain Primary Servers (SP), as well as the addresses of top-level servers, etc.

In this project, the Primary Server starts by reading its configuration files and storing them in memory. It then establishes a TCP connection (to communicate with Secondary Servers) and another UDP connection (to communicate with clients). During communications with Secondary Servers, it can send them a copy of the current information. In communications with clients, it receives and responds to queries.

The Secondary Server is a DNS server that responds to and performs DNS queries, having authorization and authority to possess and attempt to keep an updated copy of the original database from the authoritative Primary Server (SP) of a DNS domain. In this project, a Secondary Server takes as input a configuration file and a file containing a list of top-level servers, and as output, it generates a log file. The replicated information from the Primary Server is stored solely in volatile memory on the Secondary Server due to security reasons.

The Secondary Server starts by comparing its version of the information with that of the Primary Server. If the information on the Secondary Server is outdated, it initiates a request to obtain the most recent information from the Primary Server.

A DNS client application is the process that requires information from the DNS database of a specific domain. It obtains this information by making DNS queries to a DNS Resolver (SR). In a way, this project will develop a specific CL (Command-Line) client to directly query the DNS (similar to the nslookup application). The client interacts with input and output solely through the command line interface without the need for a configuration file. The client's sole functionality is to send queries and receive response(s).
The Resolver Server doesn't have access to any database files nor any authority over any domain. It acts solely as an intermediary between the client and other servers. Configuring the resolver server involves specifying potential domains and servers it needs to communicate with, available ports, addresses of top-level servers, and the path for the log file.

In addition to these fundamental elements, there are two special variants of servers: the Top Servers (ST, or DNS root servers) and the Top-Level Domain Servers (SDT, or DNS Top-Level Domain servers).

The behavior of the SDT is similar to the SP or SS (meaning an authoritative SP or SS for a top-level domain is an SDT), even though they do not have hierarchically superior domains in the DNS tree.

The STs are akin to SPs but have only one database that includes information from the corresponding SDTs for each top-level domain (i.e., the names and IP addresses of their SS and their SP). In other words, they only respond with these two types of information.

Both the STs and the SDTs are implemented using the same components that implement an SP or an SS.

The developed software components must support at least three operational parameters: one to indicate the server's service port when it differs from the standardized port (53), another parameter specifying the timeout value while waiting for a query response, and a third parameter that specifies whether it operates in debug mode or not. Consequently, all activity logged should also be sent to the standard output.
For this project, it's also necessary to use a caching system, which is an essential feature to ensure the efficient performance of the DNS service. Practically all components of a DNS system perform positive caching (when responses provide the requested results) and negative caching (when responses indicate that certain information does not exist). Cache systems are more crucial in non-authoritative servers. In the context of this project, only the implementation of a simple positive caching system in volatile memory on the servers is expected (with the same implementation for any type of server). The Command-Line (CL) interface of this project does not require any caching.
# Information model
For this project, it is necessary to define some configuration, data, and log files with a predefined syntax. The configuration files are read and processed upon the startup of the respective software component. Data files are also consulted only during startup, and their information is stored in memory. The behavior of the servers can only be altered using information in the configuration or data files that pertain to them by restarting these servers.
The configuration file for the SP, SS, and SR servers follows these rules: lines starting with "#" are considered comments and are ignored, blank lines are also ignored. Each line follows a syntax for a configuration parameter definition (parameter type value: value associated with the parameter). If there is a situation where these rules are not followed, the component logs this information in the respective logs and terminates execution.

The file containing the list of ST (Root Servers) contains the list of STs that are contacted whenever necessary. Each line of the file contains an IP address of an ST.

The log files record all relevant activity of the component, with one log entry per line in the file. When a component starts, it checks for the existence of the log files specified in its configuration file. If they do not exist, they are created. If they already exist, new entries are logged starting from the last existing entry in the file. The syntax for each entry corresponds to: timestamp label entry type IP address[:port] entry data.

The SP data file follows a syntax with the same rules as the configuration file, except for the syntax used to define data parameters on each line. It is as follows: parameter type value value expiration_time priority.

The expiration_time represents the maximum time in seconds that the data can exist in a server's cache. The priority field is an integer value less than 256, defining a priority order for various values associated with the same parameter. The lower the value, the higher the priority.

Full email names, domains, servers, and hosts should end with a ".", and if they do not end with ".", it is understood that they are concatenated with a default prefix defined by the "@" parameter of type DEFAULT.
# Comunication model
All non-connection-oriented interactions in this system are made using DNS messages encapsulated in the UDP protocol. A DNS message comprises a fixed-size header and a data part that should occupy up to 1 kilobyte. The interactions start with sending a DNS query to a server. This query originates from a Command-Line (CL) or any other DNS server and is carried within a DNS message.

A server processes the received query by first decoding the query information. If the decoding of the query information is correct, the server attempts to find direct information that answers the query in its cache or database. In the case of the cache, if the server doesn't find a direct response to the query, it forwards the query to an SDT (Server of the Top-Level Domain) that is the server for the top-level domain included in the NAME field. This process continues recursively until the server obtains a final response. This final response can be either a response where direct information has been obtained for the query or a response indicating that from that point onward, no further information about the query is available.
The Client comunicates with the server by sending a query. The queries, in this project, have the following format:
- ID;
- FLAGS;
- RESPONDE-CODE;
- N-VALUES;
- N-AUTHORITIES;
- N-EXTRA-VALUES;
- QUERY-INFO.NAME;
- QUERY-INFO.TYPE;

For example: 3874,Q+R,0,0,0,0;example.com.,MX;

The Primary Server receives this query and processes its information, responding with a query in the same format and then sending the requested information. In case the Server does not have the requested information, it still sends the response query but does not provide any further information, allowing the Client to reach a timeout.

Concurrently, the Primary Server runs a TCP connection. If it receives a CHECK VERSION from a Secondary Server, it responds with the version of the database file. After this, if it receives a query with one of its domains, for example, "adororedes.com.," it first sends the number of lines in the database file and then sends each line of the file.

The Secondary Server can receive requests from the Client in the same way as the Primary Server. Communication with the Primary Server was explained earlier. For now, the Protocol Data Units (PDUs) do not have binary encoding.

Another form of communication present is the zone transfer, which uses a TCP connection. Typically, the Secondary Server sends messages to the Primary Server to check if its replica of the database is up to date. If it isn't, the Secondary Server sends the desired domain, and the Primary Server sends a copy of the database for that domain, line by line, to the Secondary Server, as illustrated in the following diagram.

In our project, we implemented the zone transfer. However, currently, our Secondary Server does not check if its database is up-to-date. Instead, it only requests a zone transfer upon initialization by sending the domain, and the Primary Server sends a replica of its database line by line. The Secondary Server waits for the Primary Server to finish sending everything. However, the future goal is for the Secondary Server to wait for a predefined time, and if the Primary Server doesn't send everything within that time, it will attempt again after waiting for another predefined time.


