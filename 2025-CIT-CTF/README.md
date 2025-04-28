# CTF@CIT 2025 Writeup

## Reverse
### Read Only (solved)
Open the binary in IDA, and see the flag

![image](./imgs/1-1.png)

### Ask Nicely (solved)
The password is hard-coded

![image](./imgs/2-1.png)

### Serpent (solved)
The code is obfuscated with a bunch of `I` and `L` :

![a](./imgs/3-1.png)

We can first rename the function in `main`, then we can trace the calls by renaming the functions globally, with vim command :

```
%s/<name>/<new-name>/g
```

After renaming 3 functions, we can see the output is the variable `lIIlllllIl`, inside `stage1`. Simply print it out

![a](./imgs/3-2.png)

### Baby Keygen (solved)
The initial check validates :

1. If the length is 16
2. If the prefix is `KEY_`
3. If every bytes are numbers/alphabets

![a](./imgs/4-1.png)

Then we can step in the `validate()`, but it seems like a packed payload, since there's a extra RXP region on the memory

![a](./imgs/4-2.png)

I used the string `KEY_AAAABBBBCCCC`, and got the flag after stepping into `validate()`.

![a](./imgs/4-3.png)

### Secure keygen (unsolved)
The program holds a account pool with a menu, but it keeps crashing. Maybe patches are needed.

![a](./imgs/5-1.png)


## OSINT
### The Domain Always Resolves Twice (solved)
We can see a link to a website on the LinkedIn profile, dig the flag by using `whois`

![a](./imgs/6-1.png)

## Web
### Breaking Authentication (solved)
There's SQLi on the login page, and we can verify by logging in with username `admin` and password `'or 1='1` :

![a](./imgs/7-1.png)

But there's nothing after we login, so try find flag in the database, and this can be done by `sqlmap` :

```
sqlmap -u 'http://23.179.17.40:58001/' --form --smart -D app --dump
```

The flag is inside `secret` table :

![a](./imgs/7-2.png)

### Mr. Chatbot (unsolved)
Thought it is a prompt injection challenge, but the app is actually implemented by JS :

![a](./imgs/8.png)
