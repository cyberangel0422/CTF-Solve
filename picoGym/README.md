## Cache me outside
使用 [pwninit](https://github.com/io12/pwninit) 修復rpath

更改tcache entry 指向flag所在的idx

## Unsubscriptions Are Free
### Dangling pointer
從這裡可以找到

![image](./imgs/1.png)

驗證

![image](./imgs/3.png)
### 更改 function pointer

實際chunk大小為`0x20`, 因此可以覆寫已經`free()`掉的`whatToDo`

![image](./imgs/2.png)
