import imaplib
import email
import email.header
import email.utils
from time import sleep, mktime, time
from threading import Thread, Event
import html2text



class EmailClient:
    def __init__(self, account, password, address="imap.gmail.com",
                 port=993, folder="inbox"):
        self.account = account
        self.password = password
        self.port = port
        self.address = address
        self.folder = folder

    def list_old_emails(self, whitelist=None):
        return self.list_emails(whitelist, mark_as_seen=False,
                                search_filter="(SEEN)")

    def list_new_emails(self, whitelist=None, mark_as_seen=False):
        return self.list_emails(whitelist, mark_as_seen,
                                search_filter="(UNSEEN)")

    def list_emails(self, whitelist=None, mark_as_seen=False,
                    search_filter="(ALL)"):
        """
        Returns new emails.
        output:
        dicts in the format :{name,sender,subject}
        whitelist: the a list of emails that it will return
        """
        M = imaplib.IMAP4_SSL(str(self.address), port=int(self.port))
        M.login(str(self.account), str(self.password))  # Login
        M.select(str(self.folder))

        rv, data = M.search(None, search_filter)  # Only get unseen/unread emails
        new_emails = []
        for num in data[0].split():
            rv, data = M.fetch(num, '(RFC822)')

            msg = email.message_from_bytes(data[0][1])

            from_email = email.utils.parseaddr(msg['From'])[1]
            subject = str(msg['Subject'])
            sender = str(msg['From'])
            payload = self.get_body(msg)

            try:
                if msg.get("Date"):
                    ts = email.utils.parsedate(msg['Date'])
                    ts = mktime(ts)
                else:
                    ts = email.utils.parsedate(
                        msg['Received'].split("\n")[-1].strip())
                    ts = mktime(ts)
            except:
                ts = time()

            is_in_whitelist = not whitelist or from_email in whitelist

            if not is_in_whitelist:
                # The user does not want emails from that sender, skip it
                continue
            if "<" in sender:
                mail = sender.split("<")[1].split(">")[0]
                sender = sender.split("<")[0].strip()
            else:
                mail = sender
            mail = {"sender": sender,
                    "email": mail,
                    "payload": payload,
                    "ts": ts,
                    "subject": subject}
            if mark_as_seen:
                M.store(num, "+FLAGS", '\\SEEN')
            else:
                # Some email providers automatically mark a message as seen: undo that
                M.store(num, "-FLAGS", '\\SEEN')

            new_emails.append(mail)
        # Clean up
        M.close()
        M.logout()

        return list(new_emails)

    def mark_all_read(self):
        self.list_new_emails(mark_as_seen=True)

    @staticmethod
    def get_body(msg):
        payload = msg.get_payload()
        if isinstance(payload, list):
            payload = payload[-1]
            payload = html2text.html2text(str(payload))
            payload = [l for l in payload.split("\n") if
                       not l.startswith("Content-Type:")]
            payload = "\n".join(payload)
        return payload.strip()

    def send(self, subject, email, body):
        raise NotImplementedError


class EmailMonitor(Thread):
    """
    enable less secure apps https://myaccount.google.com/lesssecureapps
    enable imap  https://mail.google.com/mail/u/1/?tab=mm#settings/fwdandpop
    """
    def __init__(self, mail, password, address="imap.gmail.com", port=993,
                 folder="inbox", time_between_checks=30, whitelist=None,
                 mark_as_seen = True, filter="(UNSEEN)"):
        super().__init__()
        self.mark_as_seen = mark_as_seen
        self.time_between_checks = time_between_checks
        self.whitelist = whitelist
        self.filter = filter
        self.email = EmailClient(mail, password, address, port, folder)
        self.stop_event = Event()

    def run(self):
        self.stop_event.clear()
        while not self.stop_event.is_set():

            mails = self.email.list_emails(self.whitelist,
                                           self.mark_as_seen,
                                           search_filter=self.filter)
            for mail in mails:
                self.on_new_email(mail)
            sleep(self.time_between_checks)

    def on_new_email(self, email):
        print("new email", email)

    def stop(self):
        self.stop_event.set()
