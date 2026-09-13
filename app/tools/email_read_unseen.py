import os
import imaplib

from email.parser import BytesParser

from pydantic import BaseModel


class EmailReadUnseenResponse(BaseModel):
    from_address: str
    subject: str
    date: str


def email_read_unseen() -> list[EmailReadUnseenResponse] | str:
    """
    If there is an email in the inbox, it will be returned as a list of
    EmailReadUnseenResponse objects.
    If there is no email in the inbox, it will return "NO_EMAIL_FOUND".
    If there is an error, it will be returned as a string.
    """

    mail = imaplib.IMAP4_SSL(os.getenv("IMAP_SERVER_NAME", ""))

    mail.login(os.getenv("IMAP_USER", ""), os.getenv("IMAP_PASSWORD", ""))

    mail.select("INBOX")

    status, data = mail.search(None, "UNSEEN")

    if status != "OK":
        return "SEARCH_FAILED"

    if data[0] is None:
        return "NO_EMAIL_FOUND"

    email_ids = data[0].split()

    email_reads_unseen_list: list[EmailReadUnseenResponse] = []

    for email_id in email_ids:
        email_str = email_id.decode("utf-8")
        status, msg_data = mail.fetch(email_str, "(BODY.PEEK[])")
        if status == "OK" and msg_data:
            msg_item = msg_data[0]

            if not isinstance(msg_item, tuple) or len(msg_item) < 2:
                continue

            email_bytes = msg_item[1]

            msg_obj = BytesParser().parsebytes(email_bytes)
            email_reads_unseen_list.append(
                EmailReadUnseenResponse(
                    from_address=msg_obj.get("From", "FROM_ADDRESS_NOT_FOUND"),
                    subject=msg_obj.get("Subject", "SUBJECT_NOT_FOUND"),
                    date=msg_obj.get("Date", "DATE_NOT_FOUND"),
                )
            )

    mail.logout()

    return email_reads_unseen_list
