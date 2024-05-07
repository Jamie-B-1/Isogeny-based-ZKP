# Isogeny-based Zero-Knowledge Protocol
A Python implementation of a Zero-Knowledge Protocol from '[SIDH Proof of Knowledge](https://link.springer.com/chapter/10.1007/978-3-031-22966-4_11)', section 5.3, as part of a dissertation project for the module CSC3094 at Newcastle University.

---
## Requirements
- Pari/GP version 2.15.5 or higher
- Python 3.8 or higher
- `requirements.txt` packages including cypari python wrapper for Pari/GP
---
## Usage
This project has been run and tested using the Pycharm IDE but can still be run from the terminal provided the requirements are met.

The main file of the project is `sigma_protocol.py`. To run the file, use the following command:
```bash
python zk_protocol/sigma_protocol.py
```
The command above will run the program, first asking for an input for the number of iterations of the protocol.

The program will then run the protocol for the specified number of iterations and
output the result of the verification process.

If the verification process is successful, 
the program will output `response accepted`, otherwise it will output `response rejected`.

---
## Example
Sample output with fixed challenge of 1 and 4 iterations:
```bash
Enter number of iterations: 4
-------------------
Verifying based on challenge: 1
Verifying based on challenge: 1
Verifying based on challenge: 1
Verifying based on challenge: 1
response accepted
-------------------
Time taken: 6.923935499973595
```
Sample output with random challenge and 4 iterations:
```bash
Enter number of iterations: 4
-------------------
Verifying based on challenge: 1
Verifying based on challenge: -1
response rejected
-------------------
Time taken: 3.1004421999678016
```
This second example shows that the verification process failed, as the response was rejected. This is because the 
dual isogeny computation is not implemented in the current version of the program. In the cases of a challenge being 0
or -1, the verification process will always fail due to the current decisional statement to return False.

---