import smtplib

def test_smtp_connection():
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.ehlo()
        server.login('malvlambo@gmail.com', 'rtmkidatmuzhpjfs')
        print("SMTP connection successful!")
        server.quit()
    except Exception as e:
        print(f"SMTP connection failed: {e}")

if __name__ == "__main__":
    test_smtp_connection()

