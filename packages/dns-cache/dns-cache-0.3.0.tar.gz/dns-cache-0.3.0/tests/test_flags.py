import dns


class Foo(object):
    def junk(self):
        answer = None
        print(answer.response.flags)
        flags = answer.response.flags
        flags_text = dns.flags.to_text(flags)
        print(flags_text)
        # if nameserver == '36.86.63.182':  # ns1.digitalocean.com
        #    assert flags == dns.flags.QR | dns.flags.RD | dns.flags.RA

        assert flags & (dns.flags.QR | dns.flags.RD) == dns.flags.QR | dns.flags.RD
