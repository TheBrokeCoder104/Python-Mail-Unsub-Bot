import webbrowser
import imaplib
import bs4
import email

# Required Config for Gmail accounts.
# Others, please look up the documentation....
# Or let me know in the comment section to make another video :)
imaplib._MAXLINE = 10000000
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT ='993'

client = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

# Added the lines here to take your user input for email and password
email_id = input('Enter your Email-ID: ')
password = input('Enter your Password: ')

# This logs you in to your mail-account.
client.login(email_id, password)

try:
    _, data = client.select('INBOX', readonly=True)
    num_msgs = int(data[0])
    # print(num_msgs)
    # You can print it to see how many mails you have

    _, search_data =client.search(None, 'ALL')
    for nums in search_data[0].split():
        # The mails have to fetched in the RFC822 format, or others.. you can look up :)
        _, data = client.fetch(nums, '(RFC822)')
        _, b = data[0]
        email_msg = email.message_from_bytes(b)
        for part in email_msg.walk():   # loop for going thorugh all the mails
            if part.get_content_type() == 'text/html':
                body = part.get_payload(decode=True)   # get the body of the mail
                soup = bs4.BeautifulSoup(body, 'lxml')   
                links = soup.findAll('a')       # get all links in an email
                for selected in links:     # loop for checking unsub
                    if 'unsubscribe' in selected.text.lower():
                        webbrowser.open(selected.get('href'))

except Exception as e:
    print(e)
