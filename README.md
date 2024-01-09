# DNS Service simulation

In the context of the Computer Communications course, a project was proposed aiming to implement a DNS (Domain Name System). Initially, it was crucial to comprehend DNS concepts and understand the workings of networks and communication among computers, servers, and clients. Creating a communication model that supported and fulfilled the project's requirements was essential.

This system's structure is composed by Top-Level Domain Servers, Top Servers, Primary Servers, Secondary Servers, DNS resolvers and the Clients, wich are connected by sockets and communicate using DNS queries.
It was also necessary understanding and analysing all the files that a server needs, so all servers have a database, a log file, a cache file and a settings file, except for the DNS resolver.

Finally, we implemented, as well, the zone transfer, where if a server feels like its database is not updated, it can ask the primary server for its database, being that the primary server's databse is allways updated.

