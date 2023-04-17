# Binghamton University, Spring 2023

## CS428/528 Project-3: UDP Pinger

### SUMMARY

For Part 1, our program creates a server socket, which receives client packets via UDP. Our program runs for 3 minutes, and every 3 seconds, the client sends a ping to the server with its sequence number and the timestamp at which it is sent. If the server sucessfully receives the ping, it sends a response/echo message back to the client within 1 second. Otherwise, the client ping times out. Our program also prints out the RTT on the client side, providing the time it takes for the client to send the ping and receive an echo. However, because UDP is unreliable, even if all the above is successful, if a random integer is less than 4, the packet is considered lost.

For Part 2, our program also prints the minimum RTT< maximum RTT, total number of RTTs (number of successful ping-echo pairs), the packet loss rate (as a percentage), and the average RTTs.

For Part 3, ...

### NOTES, KNOWN BUGS, AND/OR INCOMPLETE PARTS

[Add any notes you have here and/or any parts of the project you were not able to complete]: #

### REFERENCES


### INSTRUCTIONS

to run PART 1: $ python3 udppinger-client1.py
to run PART 2: $ python3 udppinger-client2.py

### SUBMISSION

I have done this assignment completely on my own. I have not copied it, nor have I given my solution to anyone else. I understand that if I am involved in plagiarism or cheating I will have to sign an official form that I have cheated and that this form will be stored in my official university record. I also understand that I will receive a grade of "0" for the involved assignment and my grade will be reduced by one level (e.g., from "A" to "A-" or from "B+" to "B") for my first offense, and that I will receive a grade of "F" for the course for any additional offense of any kind.

By signing my name below and submitting the project, I confirm the above statement is true and that I have followed the course guidelines and policies.

Submission date: 

Team member 1 name: Katie Welcher

Team member 2 name: Joseph Lieberman
