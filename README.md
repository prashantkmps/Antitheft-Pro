# Website to control Security system

Antitheft Pro is a Web App to control the security system. This website is made for product **Antitheft Pro**. This security system can be used to secure costly things like Jwellery, Money, Confidencial Documents etc. This Product can be used in **Banks, Showrooms, Jwellery Shops, Homes** etc.

This product costs between Rs. 20,000 to Rs. 50,000.


### Requirements

- Python3
- PIP
- FLASK
- JNinja2
- Flask-Uploads


**Note-** Some other libraries are required which are different for client and server. These can be installed via:

        pip install -r requirements.txt
        
This project contains Client Machine and Server Machine code-

- Copy **Antitheft-Client** is for Product **(Client Machine Raspberry Pi)** which can be copied to raspberry pi **(In /home/pi)**.
- Host **Antitheft-Server** on the cloud. This is website which can be used to **Control** and **Monitor** the system.

### Installation Procedure for Server
- First Update Your system by executing following commands

        sudo apt-get update -y
        sudo apt-get upgrade -y
        
- Python3 is needed to run this website. To install python3, run the following command
     
         sudo apt-get install --upgrade python3

- Now install **pip**

        sudo apt-get install python-pip --upgrade
        
- Install Dependencies

        sudo pip install -r requirements.txt
        
- Finally, Run the server

        python3 main.py
        
- Browse to http://0.0.0.0:5000

**Note: Port can changed from main.py in the project directory**

#### For any info contact me on

prashantkmps@gmail.com
(+91)9458412843

# Thanks for reading
