from OpenSSL.SSL import Connection, Context, SSLv3_METHOD, TLSv1_2_METHOD
from datetime import datetime, time
import socket
host = 'www.facebook.com'
try:
    try:
        ssl_connection_setting = Context(SSLv3_METHOD)
    except ValueError:
        ssl_connection_setting = Context(TLSv1_2_METHOD)
    ssl_connection_setting.set_timeout(5)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, 443))
        c = Connection(ssl_connection_setting, s)
        c.set_tlsext_host_name(str.encode(host))
        c.set_connect_state()
        c.do_handshake()
        cert = c.get_peer_certificate()
        print("Is Expired: ", cert.has_expired())
        print("Issuer: ", cert.get_issuer())
        subject_list = cert.get_subject().get_components()
        cert_byte_arr_decoded = {}
        for item in subject_list:
            cert_byte_arr_decoded.update({item[0].decode('utf-8'): item[1].decode('utf-8')})
        print(cert_byte_arr_decoded)
        if len(cert_byte_arr_decoded) > 0:
            print("Subject: ", cert_byte_arr_decoded)
        if cert_byte_arr_decoded["CN"]:
            print("Common Name: ", cert_byte_arr_decoded["CN"])
        end_date = datetime.strptime(str(cert.get_notAfter().decode('utf-8')), "%Y%m%d%H%M%SZ")
        print("Not After (UTC Time): ", end_date)
        diff = end_date - datetime.now()
        print('Summary: "{}" SSL certificate expires on {} i.e. {} days.'.format(host, end_date, diff.days))
        c.shutdown()
        s.close()
except:
    print("Connection to {} failed.".format(host))  