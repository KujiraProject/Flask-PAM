# How to test Flask-PAM?

To test Flask-PAM you need to modify `www_config.py`. You have to set two system
groups which will be used to protected urls: `/group1_protected` and
`group2_protected`.

Secondly you have to run `./init-environment.sh` script and run Flask's dev
server:

    cd test
		./init-environment.sh
		source bin/activate
		python www.py

All files created by Python's virtualenv are ignored by Git. Now you can send
`POST` queries to website. You can use Google Chrome's application called
**Postman**.

After all you can delete environment using `./del-environment.sh` script.
