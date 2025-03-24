# SquareCTF 2023
## roplon

保護

![img](./img/1-1.png)

兩種選擇都沒辦法讀出flag，但是可以把return address覆寫成`cat_flag()`

![img](./img/1-2.png)

![img](./img/1-3.png)

但是沒有gadget可以控rdi，跳到main上面的`do_the_thing()`剛好可以執行global buffer的內容

![img](./img/1-4.png)

![img](./img/1-5.png)

## sandbox

由於一次只能用一個單字，使用$IFS繞過檢查

![img](./img/2-1.png)
