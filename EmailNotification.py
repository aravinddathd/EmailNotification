import smtplib, ssl, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailNotification:
	
	def readFile(self):
		"""
		Function to read the output from the file generated using the CLOC application.
		Create a list of dictionaries in the following format. 
		{
			Language:'',
			Files:'',
			Blank:'',
			Comment:'',
			Code:''
		}	
		"""
		# To identify the data which needs to read
		foundFlag = False
		print('Inside ReadFile')
		seperator = "-------------------------------------------------------------------------------\n"
		listOfLanguage = []
		currentDir = os.getcwd()
		with open(currentDir+'\Input.txt','r') as reader:
			for line in reader.readlines():
				line = str(line).replace("\x00", "")
				if str(line) != seperator and foundFlag == False:	
					continue
				foundFlag = True
				if '-------------------------------------------------------------------------------' in line or 'Language                     files          blank        comment           code' in line\
						or '\n' == line or line == '':
					continue
				else:
					#Create the dictionary here
					
					elems = str(line).split()
					
					languageDict = {
					'Language':elems[0],
					'Files':elems[1],
					'Blank':elems[2],
					'Comment':elems[3],
					'Code':elems[4]
					}
					
					listOfLanguage.append(languageDict)
					
		return(listOfLanguage)
				
		print('length is'+str(len(listOfLanguage)))		
		
	def createTable(self, listOfLanguage):
		"""
			Craft an html table using the list created in function readFile.
		"""
		
		lengthOfRows = len(listOfLanguage)
		
		html = """<html><body><table><tr><td>Language</td><td>Files</td><td>Blank</td><td>Comment</td><td>Code</td></tr>%s
		</table></body></html>"""
		
		tableRow = ''
		for elem in listOfLanguage:
			tableRow += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(elem['Language'],elem['Files'],elem['Blank'],elem['Comment'],elem['Code'])
	
		html = html %(tableRow)
		return html
		
	def sendEmail(self, htmlContent):
		"""
			Function will send the email to the intended person.
			Create a new email in gmail account and enable "Less secure app access:ON"
		"""
		
		sender_email = input("Enter you gmail address for sending the email and press enter:")
		password = input("Type your password and press enter:")
		receiver_email = input("Enter Recepient email address")
		
		
		message = MIMEMultipart("alternative",None,[MIMEText(htmlContent, "html")])
		message["Subject"] = "Extract the line of Code used"
		message["From"] = sender_email
		message["To"] = receiver_email
		
		
		
		# Create secure connection with server and send email
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
			server.login(sender_email, password)
			server.sendmail(
				sender_email, receiver_email, message.as_string()
			)
	
	
	
if __name__ == "__main__":

	emailNotification = EmailNotification()
	listOfLanguage = emailNotification.readFile()
	htmlContent = emailNotification.createTable(listOfLanguage)
	emailNotification.sendEmail(htmlContent)