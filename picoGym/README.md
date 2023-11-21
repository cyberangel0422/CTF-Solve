## Cache me outside
使用 [pwninit](https://github.com/io12/pwninit) 修復rpath

更改tcache entry 指向flag所在的idx

## Unsubscriptions Are Free

從這裡可以找到 dangling pointer

![image](./imgs/1.png)

驗證

![image](./imgs/3.png)

實際chunk大小為`0x20`, 因此可以覆寫已經`free()`掉的`whatToDo`

![image](./imgs/2.png)

## filtered-shellcode

程式會對傳入的資料做一些操作然後當作函式指針執行

![image](./imgs/4-1.png)

由於透過這個filter只能使用兩byte一組的shellcode, 因此逐個byte放入 `/bin//sh` 。此外在32位元下 `syscall` 要替換成 `int 0x80`

![image](./imgs/4-2.png)

![image](./imgs/4-3.png)

## babygame02

跟前面一樣有 `l` 這個選項可以更改玩家頭像，可以用這個特點覆寫return address的最低位

![image](./imgs/5-1.png)

不過在remote上連線不是很穩定，多送幾次之後就能跳去win了

![image](./imgs/5-2.png)

![image](./imgs/5-3.png)

## tic-tac

構造另外一個空檔案跟flag symlinc去同個地方產生race condition，不過我用shell怎麼都沒辦法成功，後來用了c的讀檔就跑出來了

![image](./imgs/6-1.png)

## VNE

試了一下發現需要某個環境變數上指定的路徑，沒逆向binary本身但想試試看command injection : 

![image](./imgs/7-1.png)

結果就讀出來了

![image](./imgs/7-2.png)

## Guessing game 1

file下去可以發現是靜態編譯，並且local測試多次之後會發現key是固定的

![image](./imgs/8-1.png)

直接用ROPGadget製造ropchain

![image](./imgs/8-2.png)

##  Kit Engine

題目給了會把東西餵給d8 shell的界面，在source裡面可以看出已經列出了patch的比較:

![image](./imgs/9-1.png)

可以看到這個function:

![image](./imgs/9-2.png) 

需要通過以下檢驗：

![image](./imgs/9-3.png) 

最後直接當成函式指針呼叫：

![image](./imgs/9-4.png)

由於只能看stdout回顯，沒辦法直接互動，所以用 `shellcraft.cat`

![image](./imgs/9-5.png) 
