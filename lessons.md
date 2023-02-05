04. Protocol Parsing
 - Server should be able to process multiple requests from a client.
 - A protocol is needed to handle multiple requests from a client.
 - Method we are going to follow is *split requests apart is by declaring how long the request is at the beginning of the request*
 - Diagram:
 +-----+------+-----+------+-----
 | len | msg1 | len | msg2 | more ...
 +-----+------+-----+------+-----