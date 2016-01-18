from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText
from email import Encoders
import getopt
import smtplib
import sys
import getpass


def usage():
    print """Commands: (Delimeter for multiple inputs = ", ")
    -f input files 
    -s subject
    -e email
    -m text message
    """
    sys.exit(1)


def main(argv):
	sender = "paolo.villanueva.215.sender@gmail.com"
	subject = "No Subject"
	to = ["paolo2@pdx.edu"]
	file1 = ""
	message = ""
	password = ""
	try:
            opts, args = getopt.getopt(argv, "he:s:m:f:t:", ["help", "email", 
				"subject", "message", "file"])
	except getopt.GetoptError:
                print "error"
		sys.exit()

	for opt, arg in opts:
		print opt, arg
                if opt in ("-h", "--help"):
                    usage()
                elif opt in ("-f", "--file"):
			file1 = arg.split(", ")
		elif opt in ("-s", "--subject"):
			subject = arg
		elif opt in ("-e", "--email"):
			to = arg.split(", ")
		elif opt in ("-m", "--message"):
			message = arg
		else:
			usage()

	password = getpass.getpass("Enter mailer password: ")
	if not password:
		sys.exit()
		return None
	msg = MIMEMultipart()
	msg["Subject"] = subject
	msg["From"] = sender
	msg["To"] = ", ".join(to)
	msg.attach(MIMEText(message))

        if file1:
            for i in file1:
	        part = MIMEBase("application", "octet-stream")
	        part.set_payload(open(i, "rb").read())
	        Encoders.encode_base64(part)
	        part.add_header("Content-Disposition", "attachment; filename=" + i)
	        msg.attach(part)
	try:
		smtp = smtplib.SMTP("smtp.gmail.com", 587)
		smtp.starttls()
		smtp.login(sender, password)
		smtp.sendmail(sender, to, msg.as_string())
		smtp.quit()
		print "Message sent"
	except:
		print "Error"
		pass


if "__main__" == __name__:
	main(sys.argv[1:])
