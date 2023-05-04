import qrcode

def generate_qr_code(url, box_size=1):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr



if __name__ == "__main__":
    url = "xxxxxxx"
    qr_code = generate_qr_code(url, box_size=1)
    qr_code.print_ascii()



