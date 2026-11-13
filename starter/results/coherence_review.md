# Báo cáo đánh giá độ mạch lạc của chunk


Lấy 10 trang vật lý đầu tiên theo thứ tự tăng dần (111–120). Mỗi trang lấy ký tự không trắng đầu tiên từ vị trí giữa trang trở đi làm mốc. Nếu nhiều chunk bao phủ mốc, chọn chunk bắt đầu sớm nhất, rồi theo chunk_id. C dùng cùng chunk của B. Quy tắc không dựa vào điểm retrieval; xác định trước khi chấm coherence.

## Cách chấm

- 0: bị cắt giữa ý hoặc thiếu chủ thể, không hiểu được.
- 1: hiểu một phần nhưng còn thiếu ngữ cảnh.
- 2: tự hiểu được và giữ trọn ý.

Mỗi chunk được đánh giá khi đọc độc lập, sau đó đối chiếu nguồn để xác định phần ngữ cảnh bị thiếu. Điểm và lý do được lưu trong coherence_audit.json.
Điểm coherence được đánh giá riêng với Hit@3. Cấu hình B và C sử dụng cùng chunk nên có cùng điểm coherence; bộ lọc truy xuất không thay đổi nội dung đoạn.

## Kết quả tổng hợp

| Cấu hình | Số mẫu | Trung bình /2 | Mức 0 | Mức 1 | Mức 2 |
|---|---:|---:|---:|---:|---:|
| A | 10 | 1.0 | 0 | 10 | 0 |
| B | 10 | 1.5 | 0 | 5 | 5 |
| C | 10 | 1.5 | 0 | 5 | 5 |

Cấu hình A đạt 1,0/2: các đoạn được lấy mẫu vẫn truyền tải một phần nội dung nhưng thường bắt đầu hoặc kết thúc giữa câu, từ hay ví dụ code. Cấu hình B và C đạt 1,5/2: ranh giới mục giúp giữ thêm tiêu đề và ngữ cảnh, nhưng giới hạn 1.000 ký tự vẫn có thể cắt dở nội dung.

Giới hạn: 10 vị trí đều nằm trên trang 111–120 thuộc chương Lists, vì vậy kết quả chưa đại diện cho toàn bộ ba chương. Đánh giá dựa trên văn bản trích xuất; sơ đồ bị trải phẳng và một số từ dính nhau có thể ảnh hưởng khả năng đọc.

## Trang PDF 111 — mốc ký tự 591 (đếm từ 0)

### Nội dung trang nguồn để đối chiếu

```text
Chapter 10
Lists
This chapter presents one of Python’s most useful built-in types, lists. You will also learn
more about objects and what can happen when you have more than one name for the same
object.
10.1 A list is a sequence
Like a string, alistis a sequence of values. In a string, the values are characters; in a list,
they can be any type. The values in a list are calledelementsor sometimesitems.
There are several ways to create a new list; the simplest is to enclose the elements in square
brackets ([and]):
[10, 20, 30, 40]
['crunchy frog','ram bladder','lark vomit']
The first example is a list of four integers. The second is a list of three strings. The elements
of a list don’t have to be the same type. The following list contains a string, a float, an
integer, and (lo!) another list:
['spam', 2.0, 5, [10, 20]]
A list within another list isnested.
A list that contains no elements is called an empty list; you can create one with empty
brackets,[].
As you might expect, you can assign list values to variables:
>>> cheeses = ['Cheddar','Edam','Gouda']
>>> numbers = [42, 123]
>>> empty = []
>>> print(cheeses, numbers, empty)
['Cheddar','Edam','Gouda'] [42, 123] []
```

### A_p111

Chunk: `thinkpython2_p111_450`; bắt đầu ở ký tự 450.

```text
the simplest is to enclose the elements in square
brackets ([and]):
[10, 20, 30, 40]
['crunchy frog','ram bladder','lark vomit']
The first example is a list of four integers. The second is a list of three strings. The elements
of a list don’t have to be the same type. The following list contains a string, a float, an
integer, and (lo!) another list:
['spam', 2.0, 5, [10, 20]]
A list within another list isnested.
A list that contains no elements is called an empty list; you can create one with em
```

Điểm: **1/2**. Lý do: Giữ được ví dụ và ý chính về list, nhưng mở đầu thiếu vế dẫn, kết thúc cắt giữa từ empty (with em).

### B_p111

Chunk: `thinkpython2_B_p111_1_0`; bắt đầu ở ký tự 203.

```text
10.1 A list is a sequence
Like a string, alistis a sequence of values. In a string, the values are characters; in a list,
they can be any type. The values in a list are calledelementsor sometimesitems.
There are several ways to create a new list; the simplest is to enclose the elements in square
brackets ([and]):
[10, 20, 30, 40]
['crunchy frog','ram bladder','lark vomit']
The first example is a list of four integers. The second is a list of three strings. The elements
of a list don’t have to be the same type. The following list contains a string, a float, an
integer, and (lo!) another list:
['spam', 2.0, 5, [10, 20]]
A list within another list isnested.
A list that contains no elements is called an empty list; you can create one with empty
brackets,[].
As you might expect, you can assign list values to variables:
>>> cheeses = ['Cheddar','Edam','Gouda']
>>> numbers = [42, 123]
>>> empty = []
>>> print(cheeses, numbers, empty)
['Cheddar','Edam','Gouda'] [42, 123] []
```

Điểm: **2/2**. Lý do: Có tiêu đề 10.1, định nghĩa list, ví dụ kiểu dữ liệu và list lồng, list rỗng cùng kết quả in đầy đủ. Nội dung đoạn tự hiểu được; còn lỗi dính chữ từ PDF nhưng không làm mất ý chính.

### C_p111

Chunk: `thinkpython2_B_p111_1_0`; bắt đầu ở ký tự 203.

```text
10.1 A list is a sequence
Like a string, alistis a sequence of values. In a string, the values are characters; in a list,
they can be any type. The values in a list are calledelementsor sometimesitems.
There are several ways to create a new list; the simplest is to enclose the elements in square
brackets ([and]):
[10, 20, 30, 40]
['crunchy frog','ram bladder','lark vomit']
The first example is a list of four integers. The second is a list of three strings. The elements
of a list don’t have to be the same type. The following list contains a string, a float, an
integer, and (lo!) another list:
['spam', 2.0, 5, [10, 20]]
A list within another list isnested.
A list that contains no elements is called an empty list; you can create one with empty
brackets,[].
As you might expect, you can assign list values to variables:
>>> cheeses = ['Cheddar','Edam','Gouda']
>>> numbers = [42, 123]
>>> empty = []
>>> print(cheeses, numbers, empty)
['Cheddar','Edam','Gouda'] [42, 123] []
```

Điểm: **2/2**. Lý do: Có tiêu đề 10.1, định nghĩa list, ví dụ kiểu dữ liệu và list lồng, list rỗng cùng kết quả in đầy đủ. Nội dung đoạn tự hiểu được; còn lỗi dính chữ từ PDF nhưng không làm mất ý chính. C dùng đúng cùng chunk với B tại vị trí này; filter truy xuất không thay đổi coherence của đoạn.

## Trang PDF 112 — mốc ký tự 731 (đếm từ 0)

### Nội dung trang nguồn để đối chiếu

```text
90 Chapter 10. Lists
0
1
list
numbers
123
5
list
empty
0
1
2
’Cheddar’
’Edam’
’Gouda’
list
cheeses
42
Figure 10.1: State diagram.
10.2 Lists are mutable
The syntax for accessing the elements of a list is the same as for accessing the characters
of a string—the bracket operator. The expression inside the brackets specifies the index.
Remember that the indices start at 0:
>>> cheeses[0]
'Cheddar'
Unlike strings, lists are mutable. When the bracket operator appears on the left side of an
assignment, it identifies the element of the list that will be assigned.
>>> numbers = [42, 123]
>>> numbers[1] = 5
>>> numbers
[42, 5]
The one-eth element ofnumbers, which used to be 123, is now 5.
Figure 10.1 shows the state diagram forcheeses,numbersandempty.
Lists are represented by boxes with the word “list” outside and the elements of the list
inside.cheesesrefers to a list with three elements indexed 0, 1 and 2.numberscontains
two elements; the diagram shows that the value of the second element has been reassigned
from 123 to 5.emptyrefers to a list with no elements.
List indices work the same way as string indices:
• Any integer expression can be used as an index.
• If you try to read or write an element that does not exist, you get anIndexError.
• If an index has a negative value, it counts backward from the end of the list.
Theinoperator also works on lists.
>>> cheeses = ['Cheddar','Edam','Gouda']
>>>'Edam'in cheeses
True
>>>'Brie'in cheeses
False
```

### A_p112

Chunk: `thinkpython2_p112_450`; bắt đầu ở ký tự 450.

```text
operator appears on the left side of an
assignment, it identifies the element of the list that will be assigned.
>>> numbers = [42, 123]
>>> numbers[1] = 5
>>> numbers
[42, 5]
The one-eth element ofnumbers, which used to be 123, is now 5.
Figure 10.1 shows the state diagram forcheeses,numbersandempty.
Lists are represented by boxes with the word “list” outside and the elements of the list
inside.cheesesrefers to a list with three elements indexed 0, 1 and 2.numberscontains
two elements; the diag
```

Điểm: **1/2**. Lý do: Mở đầu operator appears thiếu phần xác định bracket operator. Ví dụ gán phần tử vẫn hiểu được, nhưng phần mô tả sơ đồ cuối đoạn bị cắt ở the diag và không có hình đi kèm.

### B_p112

Chunk: `thinkpython2_B_p112_1_0`; bắt đầu ở ký tự 130.

```text
10.2 Lists are mutable
The syntax for accessing the elements of a list is the same as for accessing the characters
of a string—the bracket operator. The expression inside the brackets specifies the index.
Remember that the indices start at 0:
>>> cheeses[0]
'Cheddar'
Unlike strings, lists are mutable. When the bracket operator appears on the left side of an
assignment, it identifies the element of the list that will be assigned.
>>> numbers = [42, 123]
>>> numbers[1] = 5
>>> numbers
[42, 5]
The one-eth element ofnumbers, which used to be 123, is now 5.
Figure 10.1 shows the state diagram forcheeses,numbersandempty.
Lists are represented by boxes with the word “list” outside and the elements of the list
inside.cheesesrefers to a list with three elements indexed 0, 1 and 2.numberscontains
two elements; the diagram shows that the value of the second element has been reassigned
from 123 to 5.emptyrefers to a list with no elements.
List indices work the same way as string indices:
• Any int
```

Điểm: **1/2**. Lý do: Có tiêu đề, giải thích chỉ số và tính mutable cùng ví dụ hoàn chỉnh. Tuy nhiên mục quy tắc chỉ số bắt đầu ở cuối bị cắt giữa Any int, nên toàn đoạn chưa trọn ý.

### C_p112

Chunk: `thinkpython2_B_p112_1_0`; bắt đầu ở ký tự 130.

```text
10.2 Lists are mutable
The syntax for accessing the elements of a list is the same as for accessing the characters
of a string—the bracket operator. The expression inside the brackets specifies the index.
Remember that the indices start at 0:
>>> cheeses[0]
'Cheddar'
Unlike strings, lists are mutable. When the bracket operator appears on the left side of an
assignment, it identifies the element of the list that will be assigned.
>>> numbers = [42, 123]
>>> numbers[1] = 5
>>> numbers
[42, 5]
The one-eth element ofnumbers, which used to be 123, is now 5.
Figure 10.1 shows the state diagram forcheeses,numbersandempty.
Lists are represented by boxes with the word “list” outside and the elements of the list
inside.cheesesrefers to a list with three elements indexed 0, 1 and 2.numberscontains
two elements; the diagram shows that the value of the second element has been reassigned
from 123 to 5.emptyrefers to a list with no elements.
List indices work the same way as string indices:
• Any int
```

Điểm: **1/2**. Lý do: Có tiêu đề, giải thích chỉ số và tính mutable cùng ví dụ hoàn chỉnh. Tuy nhiên mục quy tắc chỉ số bắt đầu ở cuối bị cắt giữa Any int, nên toàn đoạn chưa trọn ý. C dùng đúng cùng chunk với B tại vị trí này; filter truy xuất không thay đổi coherence của đoạn.

## Trang PDF 113 — mốc ký tự 749 (đếm từ 0)

### Nội dung trang nguồn để đối chiếu

```text
10.3. Traversing a list 91
10.3 Traversing a list
The most common way to traverse the elements of a list is with aforloop. The syntax is
the same as for strings:
for cheese in cheeses:
print(cheese)
This works well if you only need to read the elements of the list. But if you want to write
or update the elements, you need the indices. A common way to do that is to combine the
built-in functionsrangeandlen:
for i in range(len(numbers)):
numbers[i] = numbers[i] * 2
This loop traverses the list and updates each element.lenreturns the number of elements
in the list.rangereturns a list of indices from 0 ton−1, wherenis the length of the list.
Each time through the loopigets the index of the next element. The assignment statement
in the body usesito read the old value of the element and to assign the new value.
Aforloop over an empty list never runs the body:
for x in []:
print('This never happens.')
Although a list can contain another list, the nested list still counts as a single element. The
length of this list is four:
['spam', 1, ['Brie','Roquefort','Pol le Veq'], [1, 2, 3]]
10.4 List operations
The+operator concatenates lists:
>>> a = [1, 2, 3]
>>> b = [4, 5, 6]
>>> c = a + b
>>> c
[1, 2, 3, 4, 5, 6]
The*operator repeats a list a given number of times:
>>> [0] * 4
[0, 0, 0, 0]
>>> [1, 2, 3] * 3
[1, 2, 3, 1, 2, 3, 1, 2, 3]
The first example repeats[0]four times. The second example repeats the list[1, 2, 3]
three times.
10.5 List slices
The slice operator also works on lists:
```

### A_p113

Chunk: `thinkpython2_p113_450`; bắt đầu ở ký tự 450.

```text
 = numbers[i] * 2
This loop traverses the list and updates each element.lenreturns the number of elements
in the list.rangereturns a list of indices from 0 ton−1, wherenis the length of the list.
Each time through the loopigets the index of the next element. The assignment statement
in the body usesito read the old value of the element and to assign the new value.
Aforloop over an empty list never runs the body:
for x in []:
print('This never happens.')
Although a list can contain another list, 
```

Điểm: **1/2**. Lý do: Bắt đầu giữa phép gán, thiếu vòng lặp gốc mà This loop đang giải thích. Vẫn hiểu phần vòng lặp trên list rỗng, nhưng câu cuối về list lồng chưa hoàn thành.

### B_p113

Chunk: `thinkpython2_B_p113_1_0`; bắt đầu ở ký tự 27.

```text
10.3 Traversing a list
The most common way to traverse the elements of a list is with aforloop. The syntax is
the same as for strings:
for cheese in cheeses:
print(cheese)
This works well if you only need to read the elements of the list. But if you want to write
or update the elements, you need the indices. A common way to do that is to combine the
built-in functionsrangeandlen:
for i in range(len(numbers)):
numbers[i] = numbers[i] * 2
This loop traverses the list and updates each element.lenreturns the number of elements
in the list.rangereturns a list of indices from 0 ton−1, wherenis the length of the list.
Each time through the loopigets the index of the next element. The assignment statement
in the body usesito read the old value of the element and to assign the new value.
Aforloop over an empty list never runs the body:
for x in []:
print('This never happens.')
Although a list can contain another list, the nested list still counts as a single element. The
length of this list is
```

Điểm: **1/2**. Lý do: Giữ tiêu đề và ví dụ duyệt/cập nhật list trước phần giải thích nên ngữ cảnh tốt hơn A. Cuối đoạn dừng ở The length of this list is, thiếu số lượng và ví dụ tiếp theo.

### C_p113

Chunk: `thinkpython2_B_p113_1_0`; bắt đầu ở ký tự 27.

```text
10.3 Traversing a list
The most common way to traverse the elements of a list is with aforloop. The syntax is
the same as for strings:
for cheese in cheeses:
print(cheese)
This works well if you only need to read the elements of the list. But if you want to write
or update the elements, you need the indices. A common way to do that is to combine the
built-in functionsrangeandlen:
for i in range(len(numbers)):
numbers[i] = numbers[i] * 2
This loop traverses the list and updates each element.lenreturns the number of elements
in the list.rangereturns a list of indices from 0 ton−1, wherenis the length of the list.
Each time through the loopigets the index of the next element. The assignment statement
in the body usesito read the old value of the element and to assign the new value.
Aforloop over an empty list never runs the body:
for x in []:
print('This never happens.')
Although a list can contain another list, the nested list still counts as a single element. The
length of this list is
```

Điểm: **1/2**. Lý do: Giữ tiêu đề và ví dụ duyệt/cập nhật list trước phần giải thích nên ngữ cảnh tốt hơn A. Cuối đoạn dừng ở The length of this list is, thiếu số lượng và ví dụ tiếp theo. C dùng đúng cùng chunk với B tại vị trí này; filter truy xuất không thay đổi coherence của đoạn.

## Trang PDF 114 — mốc ký tự 633 (đếm từ 0)

### Nội dung trang nguồn để đối chiếu

```text
92 Chapter 10. Lists
>>> t = ['a','b','c','d','e','f']
>>> t[1:3]
['b','c']
>>> t[:4]
['a','b','c','d']
>>> t[3:]
['d','e','f']
If you omit the first index, the slice starts at the beginning. If you omit the second, the slice
goes to the end. So if you omit both, the slice is a copy of the whole list.
>>> t[:]
['a','b','c','d','e','f']
Since lists are mutable, it is often useful to make a copy before performing operations that
modify lists.
A slice operator on the left side of an assignment can update multiple elements:
>>> t = ['a','b','c','d','e','f']
>>> t[1:3] = ['x','y']
>>> t
['a','x','y','d','e','f']
10.6 List methods
Python provides methods that operate on lists. For example,appendadds a new element
to the end of a list:
>>> t = ['a','b','c']
>>> t.append('d')
>>> t
['a','b','c','d']
extendtakes a list as an argument and appends all of the elements:
>>> t1 = ['a','b','c']
>>> t2 = ['d','e']
>>> t1.extend(t2)
>>> t1
['a','b','c','d','e']
This example leavest2unmodified.
sortarranges the elements of the list from low to high:
>>> t = ['d','c','e','b','a']
>>> t.sort()
>>> t
['a','b','c','d','e']
Most list methods are void; they modify the list and returnNone. If you accidentally write
t = t.sort(), you will be disappointed with the result.
```

### A_p114

Chunk: `thinkpython2_p114_450`; bắt đầu ở ký tự 450.

```text
ce operator on the left side of an assignment can update multiple elements:
>>> t = ['a','b','c','d','e','f']
>>> t[1:3] = ['x','y']
>>> t
['a','x','y','d','e','f']
10.6 List methods
Python provides methods that operate on lists. For example,appendadds a new element
to the end of a list:
>>> t = ['a','b','c']
>>> t.append('d')
>>> t
['a','b','c','d']
extendtakes a list as an argument and appends all of the elements:
>>> t1 = ['a','b','c']
>>> t2 = ['d','e']
>>> t1.extend(t2)
>>> t1
['a','b','c',
```

Điểm: **1/2**. Lý do: Bắt đầu giữa từ slice ở ce operator và trộn phần gán slice với mục List methods. Ví dụ append hoàn chỉnh nhưng đầu ra ví dụ extend bị cắt giữa danh sách.

### B_p114

Chunk: `thinkpython2_B_p114_1_0`; bắt đầu ở ký tự 615.

```text
10.6 List methods
Python provides methods that operate on lists. For example,appendadds a new element
to the end of a list:
>>> t = ['a','b','c']
>>> t.append('d')
>>> t
['a','b','c','d']
extendtakes a list as an argument and appends all of the elements:
>>> t1 = ['a','b','c']
>>> t2 = ['d','e']
>>> t1.extend(t2)
>>> t1
['a','b','c','d','e']
This example leavest2unmodified.
sortarranges the elements of the list from low to high:
>>> t = ['d','c','e','b','a']
>>> t.sort()
>>> t
['a','b','c','d','e']
Most list methods are void; they modify the list and returnNone. If you accidentally write
t = t.sort(), you will be disappointed with the result.
```

Điểm: **2/2**. Lý do: Bắt đầu đúng tiêu đề List methods, giữ các ví dụ append, extend, sort với kết quả và cảnh báo trả về None. Có thể đọc riêng để hiểu nội dung mục.

### C_p114

Chunk: `thinkpython2_B_p114_1_0`; bắt đầu ở ký tự 615.

```text
10.6 List methods
Python provides methods that operate on lists. For example,appendadds a new element
to the end of a list:
>>> t = ['a','b','c']
>>> t.append('d')
>>> t
['a','b','c','d']
extendtakes a list as an argument and appends all of the elements:
>>> t1 = ['a','b','c']
>>> t2 = ['d','e']
>>> t1.extend(t2)
>>> t1
['a','b','c','d','e']
This example leavest2unmodified.
sortarranges the elements of the list from low to high:
>>> t = ['d','c','e','b','a']
>>> t.sort()
>>> t
['a','b','c','d','e']
Most list methods are void; they modify the list and returnNone. If you accidentally write
t = t.sort(), you will be disappointed with the result.
```

Điểm: **2/2**. Lý do: Bắt đầu đúng tiêu đề List methods, giữ các ví dụ append, extend, sort với kết quả và cảnh báo trả về None. Có thể đọc riêng để hiểu nội dung mục. C dùng đúng cùng chunk với B tại vị trí này; filter truy xuất không thay đổi coherence của đoạn.

## Trang PDF 115 — mốc ký tự 818 (đếm từ 0)

### Nội dung trang nguồn để đối chiếu

```text
10.7. Map, filter and reduce 93
10.7 Map, filter and reduce
To add up all the numbers in a list, you can use a loop like this:
def add_all(t):
total = 0
for x in t:
total += x
return total
totalis initialized to 0. Each time through the loop,xgets one element from the list.
The+=operator provides a short way to update a variable. Thisaugmented assignment
statement,
total += x
is equivalent to
total = total + x
As the loop runs,totalaccumulates the sum of the elements; a variable used this way is
sometimes called anaccumulator.
Adding up the elements of a list is such a common operation that Python provides it as a
built-in function,sum:
>>> t = [1, 2, 3]
>>> sum(t)
6
An operation like this that combines a sequence of elements into a single value is some-
times calledreduce.
Sometimes you want to traverse one list while building another. For example, the following
function takes a list of strings and returns a new list that contains capitalized strings:
def capitalize_all(t):
res = []
for s in t:
res.append(s.capitalize())
return res
resis initialized with an empty list; each time through the loop, we append the next ele-
ment. Soresis another kind of accumulator.
An operation likecapitalize_allis sometimes called amapbecause it “maps” a function
(in this case the methodcapitalize) onto each of the elements in a sequence.
Another common operation is to select some of the elements from a list and return a sublist.
For example, the following function takes a list of strings and returns a list that contains
only the uppercase strings:
def only_upper(t):
res = []
for s in t:
if s.isupper():
res.append(s)
return res
```

### A_p115

Chunk: `thinkpython2_p115_450`; bắt đầu ở ký tự 450.

```text
e sum of the elements; a variable used this way is
sometimes called anaccumulator.
Adding up the elements of a list is such a common operation that Python provides it as a
built-in function,sum:
>>> t = [1, 2, 3]
>>> sum(t)
6
An operation like this that combines a sequence of elements into a single value is some-
times calledreduce.
Sometimes you want to traverse one list while building another. For example, the following
function takes a list of strings and returns a new list that contains capi
```

Điểm: **1/2**. Lý do: Mở đầu giữa câu nói về accumulator và kết thúc giữa từ capitalized. Có giải thích sum/reduce ở giữa, nhưng thiếu khởi tạo accumulator và ví dụ map tiếp theo.

### B_p115

Chunk: `thinkpython2_B_p115_1_0`; bắt đầu ở ký tự 32.

```text
10.7 Map, filter and reduce
To add up all the numbers in a list, you can use a loop like this:
def add_all(t):
total = 0
for x in t:
total += x
return total
totalis initialized to 0. Each time through the loop,xgets one element from the list.
The+=operator provides a short way to update a variable. Thisaugmented assignment
statement,
total += x
is equivalent to
total = total + x
As the loop runs,totalaccumulates the sum of the elements; a variable used this way is
sometimes called anaccumulator.
Adding up the elements of a list is such a common operation that Python provides it as a
built-in function,sum:
>>> t = [1, 2, 3]
>>> sum(t)
6
An operation like this that combines a sequence of elements into a single value is some-
times calledreduce.
Sometimes you want to traverse one list while building another. For example, the following
function takes a list of strings and returns a new list that contains capitalized strings:
def capitalize_all(t):
res = []
for s in t:
res.append(s.capitali
```

Điểm: **1/2**. Lý do: Có tiêu đề, hàm add_all, augmented assignment và giải thích accumulator/reduce. Phần capitalize_all bị cắt giữa lời gọi capitalize, nên thiếu phần kết của ví dụ code.

### C_p115

Chunk: `thinkpython2_B_p115_1_0`; bắt đầu ở ký tự 32.

```text
10.7 Map, filter and reduce
To add up all the numbers in a list, you can use a loop like this:
def add_all(t):
total = 0
for x in t:
total += x
return total
totalis initialized to 0. Each time through the loop,xgets one element from the list.
The+=operator provides a short way to update a variable. Thisaugmented assignment
statement,
total += x
is equivalent to
total = total + x
As the loop runs,totalaccumulates the sum of the elements; a variable used this way is
sometimes called anaccumulator.
Adding up the elements of a list is such a common operation that Python provides it as a
built-in function,sum:
>>> t = [1, 2, 3]
>>> sum(t)
6
An operation like this that combines a sequence of elements into a single value is some-
times calledreduce.
Sometimes you want to traverse one list while building another. For example, the following
function takes a list of strings and returns a new list that contains capitalized strings:
def capitalize_all(t):
res = []
for s in t:
res.append(s.capitali
```

Điểm: **1/2**. Lý do: Có tiêu đề, hàm add_all, augmented assignment và giải thích accumulator/reduce. Phần capitalize_all bị cắt giữa lời gọi capitalize, nên thiếu phần kết của ví dụ code. C dùng đúng cùng chunk với B tại vị trí này; filter truy xuất không thay đổi coherence của đoạn.

## Trang PDF 116 — mốc ký tự 716 (đếm từ 0)

### Nội dung trang nguồn để đối chiếu

```text
94 Chapter 10. Lists
isupperis a string method that returnsTrueif the string contains only upper case letters.
An operation likeonly_upperis called afilterbecause it selects some of the elements and
filters out the others.
Most common list operations can be expressed as a combination of map, filter and reduce.
10.8 Deleting elements
There are several ways to delete elements from a list. If you know the index of the element
you want, you can usepop:
>>> t = ['a','b','c']
>>> x = t.pop(1)
>>> t
['a','c']
>>> x
'b'
popmodifies the list and returns the element that was removed. If you don’t provide an
index, it deletes and returns the last element.
If you don’t need the removed value, you can use thedeloperator:
>>> t = ['a','b','c']
>>> del t[1]
>>> t
['a','c']
If you know the element you want to remove (but not the index), you can useremove:
>>> t = ['a','b','c']
>>> t.remove('b')
>>> t
['a','c']
The return value fromremoveisNone.
To remove more than one element, you can usedelwith a slice index:
>>> t = ['a','b','c','d','e','f']
>>> del t[1:5]
>>> t
['a','f']
As usual, the slice selects all the elements up to but not including the second index.
10.9 Lists and strings
A string is a sequence of characters and a list is a sequence of values, but a list of characters
is not the same as a string. To convert from a string to a list of characters, you can uselist:
>>> s ='spam'
>>> t = list(s)
>>> t
['s','p','a','m']
```

### A_p116

Chunk: `thinkpython2_p116_450`; bắt đầu ở ký tự 450.

```text
p:
>>> t = ['a','b','c']
>>> x = t.pop(1)
>>> t
['a','c']
>>> x
'b'
popmodifies the list and returns the element that was removed. If you don’t provide an
index, it deletes and returns the last element.
If you don’t need the removed value, you can use thedeloperator:
>>> t = ['a','b','c']
>>> del t[1]
>>> t
['a','c']
If you know the element you want to remove (but not the index), you can useremove:
>>> t = ['a','b','c']
>>> t.remove('b')
>>> t
['a','c']
The return value fromremoveisNone.
To remo
```

Điểm: **1/2**. Lý do: Mở đầu chỉ còn p: của phần dẫn về pop. Ví dụ pop, del và remove cùng giải thích chính vẫn đọc được, nhưng câu cuối To remo bị cắt trước nội dung xóa nhiều phần tử.

### B_p116

Chunk: `thinkpython2_B_p116_1_0`; bắt đầu ở ký tự 312.

```text
10.8 Deleting elements
There are several ways to delete elements from a list. If you know the index of the element
you want, you can usepop:
>>> t = ['a','b','c']
>>> x = t.pop(1)
>>> t
['a','c']
>>> x
'b'
popmodifies the list and returns the element that was removed. If you don’t provide an
index, it deletes and returns the last element.
If you don’t need the removed value, you can use thedeloperator:
>>> t = ['a','b','c']
>>> del t[1]
>>> t
['a','c']
If you know the element you want to remove (but not the index), you can useremove:
>>> t = ['a','b','c']
>>> t.remove('b')
>>> t
['a','c']
The return value fromremoveisNone.
To remove more than one element, you can usedelwith a slice index:
>>> t = ['a','b','c','d','e','f']
>>> del t[1:5]
>>> t
['a','f']
As usual, the slice selects all the elements up to but not including the second index.
```

Điểm: **2/2**. Lý do: Toàn bộ mục Deleting elements được giữ: có điều kiện chọn pop/del/remove, ví dụ và đầu ra, xóa bằng slice và giải thích cận cuối. Đủ ngữ cảnh để tự hiểu.

### C_p116

Chunk: `thinkpython2_B_p116_1_0`; bắt đầu ở ký tự 312.

```text
10.8 Deleting elements
There are several ways to delete elements from a list. If you know the index of the element
you want, you can usepop:
>>> t = ['a','b','c']
>>> x = t.pop(1)
>>> t
['a','c']
>>> x
'b'
popmodifies the list and returns the element that was removed. If you don’t provide an
index, it deletes and returns the last element.
If you don’t need the removed value, you can use thedeloperator:
>>> t = ['a','b','c']
>>> del t[1]
>>> t
['a','c']
If you know the element you want to remove (but not the index), you can useremove:
>>> t = ['a','b','c']
>>> t.remove('b')
>>> t
['a','c']
The return value fromremoveisNone.
To remove more than one element, you can usedelwith a slice index:
>>> t = ['a','b','c','d','e','f']
>>> del t[1:5]
>>> t
['a','f']
As usual, the slice selects all the elements up to but not including the second index.
```

Điểm: **2/2**. Lý do: Toàn bộ mục Deleting elements được giữ: có điều kiện chọn pop/del/remove, ví dụ và đầu ra, xóa bằng slice và giải thích cận cuối. Đủ ngữ cảnh để tự hiểu. C dùng đúng cùng chunk với B tại vị trí này; filter truy xuất không thay đổi coherence của đoạn.

## Trang PDF 117 — mốc ký tự 814 (đếm từ 0)

### Nội dung trang nguồn để đối chiếu

```text
10.10. Objects and values 95
a
b
’banana’
a
b
’banana’
’banana’
Figure 10.2: State diagram.
Becauselistis the name of a built-in function, you should avoid using it as a variable
name. I also avoidlbecause it looks too much like1. So that’s why I uset.
Thelistfunction breaks a string into individual letters. If you want to break a string into
words, you can use thesplitmethod:
>>> s ='pining for the fjords'
>>> t = s.split()
>>> t
['pining','for','the','fjords']
An optional argument called adelimiterspecifies which characters to use as word bound-
aries. The following example uses a hyphen as a delimiter:
>>> s ='spam-spam-spam'
>>> delimiter ='-'
>>> t = s.split(delimiter)
>>> t
['spam','spam','spam']
joinis the inverse ofsplit. It takes a list of strings and concatenates the elements.joinis
a string method, so you have to invoke it on the delimiter and pass the list as a parameter:
>>> t = ['pining','for','the','fjords']
>>> delimiter =' '
>>> s = delimiter.join(t)
>>> s
'pining for the fjords'
In this case the delimiter is a space character, sojoinputs a space between words. To
concatenate strings without spaces, you can use the empty string,'', as a delimiter.
10.10 Objects and values
If we run these assignment statements:
a ='banana'
b ='banana'
We know thataandbboth refer to a string, but we don’t know whether they refer to the
samestring. There are two possible states, shown in Figure 10.2.
In one case,aandbrefer to two different objects that have the same value. In the second
case, they refer to the same object.
To check whether two variables refer to the same object, you can use theisoperator.
```

### A_p117

Chunk: `thinkpython2_p117_450`; bắt đầu ở ký tự 450.

```text
,'the','fjords']
An optional argument called adelimiterspecifies which characters to use as word bound-
aries. The following example uses a hyphen as a delimiter:
>>> s ='spam-spam-spam'
>>> delimiter ='-'
>>> t = s.split(delimiter)
>>> t
['spam','spam','spam']
joinis the inverse ofsplit. It takes a list of strings and concatenates the elements.joinis
a string method, so you have to invoke it on the delimiter and pass the list as a parameter:
>>> t = ['pining','for','the','fjords']
>>> delimiter
```

Điểm: **1/2**. Lý do: Đầu đoạn là phần đuôi kết quả split từ chunk trước. Có ví dụ delimiter dùng dấu gạch nối, nhưng ví dụ join cuối đoạn bị cắt ở khai báo delimiter, nên chỉ hiểu một phần.

### B_p117

Chunk: `thinkpython2_B_p117_0_0`; bắt đầu ở ký tự 0.

```text
10.10. Objects and values 95
a
b
’banana’
a
b
’banana’
’banana’
Figure 10.2: State diagram.
Becauselistis the name of a built-in function, you should avoid using it as a variable
name. I also avoidlbecause it looks too much like1. So that’s why I uset.
Thelistfunction breaks a string into individual letters. If you want to break a string into
words, you can use thesplitmethod:
>>> s ='pining for the fjords'
>>> t = s.split()
>>> t
['pining','for','the','fjords']
An optional argument called adelimiterspecifies which characters to use as word bound-
aries. The following example uses a hyphen as a delimiter:
>>> s ='spam-spam-spam'
>>> delimiter ='-'
>>> t = s.split(delimiter)
>>> t
['spam','spam','spam']
joinis the inverse ofsplit. It takes a list of strings and concatenates the elements.joinis
a string method, so you have to invoke it on the delimiter and pass the list as a parameter:
>>> t = ['pining','for','the','fjords']
>>> delimiter =' '
>>> s = delimiter.join(t)
>>> s
'pining for
```

Điểm: **1/2**. Lý do: Giữ giải thích và ví dụ split, delimiter, join nên có ngữ cảnh. Phần sơ đồ bị trải phẳng thành chữ rời và đầu ra join cuối đoạn bị cắt ở pining for, làm đoạn chưa hoàn chỉnh.

### C_p117

Chunk: `thinkpython2_B_p117_0_0`; bắt đầu ở ký tự 0.

```text
10.10. Objects and values 95
a
b
’banana’
a
b
’banana’
’banana’
Figure 10.2: State diagram.
Becauselistis the name of a built-in function, you should avoid using it as a variable
name. I also avoidlbecause it looks too much like1. So that’s why I uset.
Thelistfunction breaks a string into individual letters. If you want to break a string into
words, you can use thesplitmethod:
>>> s ='pining for the fjords'
>>> t = s.split()
>>> t
['pining','for','the','fjords']
An optional argument called adelimiterspecifies which characters to use as word bound-
aries. The following example uses a hyphen as a delimiter:
>>> s ='spam-spam-spam'
>>> delimiter ='-'
>>> t = s.split(delimiter)
>>> t
['spam','spam','spam']
joinis the inverse ofsplit. It takes a list of strings and concatenates the elements.joinis
a string method, so you have to invoke it on the delimiter and pass the list as a parameter:
>>> t = ['pining','for','the','fjords']
>>> delimiter =' '
>>> s = delimiter.join(t)
>>> s
'pining for
```

Điểm: **1/2**. Lý do: Giữ giải thích và ví dụ split, delimiter, join nên có ngữ cảnh. Phần sơ đồ bị trải phẳng thành chữ rời và đầu ra join cuối đoạn bị cắt ở pining for, làm đoạn chưa hoàn chỉnh. C dùng đúng cùng chunk với B tại vị trí này; filter truy xuất không thay đổi coherence của đoạn.

## Trang PDF 118 — mốc ký tự 744 (đếm từ 0)

### Nội dung trang nguồn để đối chiếu

```text
96 Chapter 10. Lists
a
b
[ 1, 2, 3 ]
[ 1, 2, 3 ]
Figure 10.3: State diagram.
a
b
[ 1, 2, 3 ]
Figure 10.4: State diagram.
>>> a ='banana'
>>> b ='banana'
>>> a is b
True
In this example, Python only created one string object, and bothaandbrefer to it. But
when you create two lists, you get two objects:
>>> a = [1, 2, 3]
>>> b = [1, 2, 3]
>>> a is b
False
So the state diagram looks like Figure 10.3.
In this case we would say that the two lists areequivalent, because they have the same el-
ements, but notidentical, because they are not the same object. If two objects are identical,
they are also equivalent, but if they are equivalent, they are not necessarily identical.
Until now, we have been using “object” and “value” interchangeably, but it is more precise
to say that an object has a value. If you evaluate[1, 2, 3], you get a list object whose
value is a sequence of integers. If another list has the same elements, we say it has the
same value, but it is not the same object.
10.11 Aliasing
Ifarefers to an object and you assignb = a, then both variables refer to the same object:
>>> a = [1, 2, 3]
>>> b = a
>>> b is a
True
The state diagram looks like Figure 10.4.
The association of a variable with an object is called areference. In this example, there are
two references to the same object.
An object with more than one reference has more than one name, so we say that the object
isaliased.
If the aliased object is mutable, changes made with one alias affect the other:
```

### A_p118

Chunk: `thinkpython2_p118_450`; bắt đầu ở ký tự 450.

```text
quivalent, because they have the same el-
ements, but notidentical, because they are not the same object. If two objects are identical,
they are also equivalent, but if they are equivalent, they are not necessarily identical.
Until now, we have been using “object” and “value” interchangeably, but it is more precise
to say that an object has a value. If you evaluate[1, 2, 3], you get a list object whose
value is a sequence of integers. If another list has the same elements, we say it has the
same
```

Điểm: **1/2**. Lý do: Bắt đầu giữa từ equivalent, thiếu hai list đang được so sánh. Phần phân biệt identity/value vẫn có thể hiểu một phần, nhưng câu cuối dừng ở same và chưa nêu hết kết luận.

### B_p118

Chunk: `thinkpython2_B_p118_0_0`; bắt đầu ở ký tự 0.

```text
96 Chapter 10. Lists
a
b
[ 1, 2, 3 ]
[ 1, 2, 3 ]
Figure 10.3: State diagram.
a
b
[ 1, 2, 3 ]
Figure 10.4: State diagram.
>>> a ='banana'
>>> b ='banana'
>>> a is b
True
In this example, Python only created one string object, and bothaandbrefer to it. But
when you create two lists, you get two objects:
>>> a = [1, 2, 3]
>>> b = [1, 2, 3]
>>> a is b
False
So the state diagram looks like Figure 10.3.
In this case we would say that the two lists areequivalent, because they have the same el-
ements, but notidentical, because they are not the same object. If two objects are identical,
they are also equivalent, but if they are equivalent, they are not necessarily identical.
Until now, we have been using “object” and “value” interchangeably, but it is more precise
to say that an object has a value. If you evaluate[1, 2, 3], you get a list object whose
value is a sequence of integers. If another list has the same elements, we say it has the
same value, but it is not the same object.
```

Điểm: **2/2**. Lý do: Giữ cả hai ví dụ identity của string/list và phần phân biệt equivalent với identical. Kết luận về cùng giá trị nhưng khác đối tượng hoàn chỉnh; chữ sơ đồ rời đầu đoạn gây nhiễu nhưng không làm mất ngữ cảnh chính.

### C_p118

Chunk: `thinkpython2_B_p118_0_0`; bắt đầu ở ký tự 0.

```text
96 Chapter 10. Lists
a
b
[ 1, 2, 3 ]
[ 1, 2, 3 ]
Figure 10.3: State diagram.
a
b
[ 1, 2, 3 ]
Figure 10.4: State diagram.
>>> a ='banana'
>>> b ='banana'
>>> a is b
True
In this example, Python only created one string object, and bothaandbrefer to it. But
when you create two lists, you get two objects:
>>> a = [1, 2, 3]
>>> b = [1, 2, 3]
>>> a is b
False
So the state diagram looks like Figure 10.3.
In this case we would say that the two lists areequivalent, because they have the same el-
ements, but notidentical, because they are not the same object. If two objects are identical,
they are also equivalent, but if they are equivalent, they are not necessarily identical.
Until now, we have been using “object” and “value” interchangeably, but it is more precise
to say that an object has a value. If you evaluate[1, 2, 3], you get a list object whose
value is a sequence of integers. If another list has the same elements, we say it has the
same value, but it is not the same object.
```

Điểm: **2/2**. Lý do: Giữ cả hai ví dụ identity của string/list và phần phân biệt equivalent với identical. Kết luận về cùng giá trị nhưng khác đối tượng hoàn chỉnh; chữ sơ đồ rời đầu đoạn gây nhiễu nhưng không làm mất ngữ cảnh chính. C dùng đúng cùng chunk với B tại vị trí này; filter truy xuất không thay đổi coherence của đoạn.

## Trang PDF 119 — mốc ký tự 645 (đếm từ 0)

### Nội dung trang nguồn để đối chiếu

```text
10.12. List arguments 97
0
1
2
’a’
’b’
’c’
list
t
letters
delete_head
__main__
Figure 10.5: Stack diagram.
>>> b[0] = 42
>>> a
[42, 2, 3]
Although this behavior can be useful, it is error-prone. In general, it is safer to avoid
aliasing when you are working with mutable objects.
For immutable objects like strings, aliasing is not as much of a problem. In this example:
a ='banana'
b ='banana'
It almost never makes a difference whetheraandbrefer to the same string or not.
10.12 List arguments
When you pass a list to a function, the function gets a reference to the list. If the function
modifies the list, the caller sees the change. For example,delete_headremoves the first
element from a list:
def delete_head(t):
del t[0]
Here’s how it is used:
>>> letters = ['a','b','c']
>>> delete_head(letters)
>>> letters
['b','c']
The parametertand the variablelettersare aliases for the same object. The stack diagram
looks like Figure 10.5.
Since the list is shared by two frames, I drew it between them.
It is important to distinguish between operations that modify lists and operations that cre-
ate new lists. For example, theappendmethod modifies a list, but the+operator creates a
new list.
Here’s an example usingappend:
>>> t1 = [1, 2]
>>> t2 = t1.append(3)
>>> t1
[1, 2, 3]
>>> t2
None
```

### A_p119

Chunk: `thinkpython2_p119_450`; bắt đầu ở ký tự 450.

```text
 the same string or not.
10.12 List arguments
When you pass a list to a function, the function gets a reference to the list. If the function
modifies the list, the caller sees the change. For example,delete_headremoves the first
element from a list:
def delete_head(t):
del t[0]
Here’s how it is used:
>>> letters = ['a','b','c']
>>> delete_head(letters)
>>> letters
['b','c']
The parametertand the variablelettersare aliases for the same object. The stack diagram
looks like Figure 10.5.
Since the l
```

Điểm: **1/2**. Lý do: Sau phần dư câu về string, mục List arguments có giải thích và ví dụ sửa list ở hàm. Cuối đoạn bị cắt giữa Since the l nên phần mô tả quan hệ chia sẻ đối tượng chưa hết.

### B_p119

Chunk: `thinkpython2_B_p119_1_0`; bắt đầu ở ký tự 475.

```text
10.12 List arguments
When you pass a list to a function, the function gets a reference to the list. If the function
modifies the list, the caller sees the change. For example,delete_headremoves the first
element from a list:
def delete_head(t):
del t[0]
Here’s how it is used:
>>> letters = ['a','b','c']
>>> delete_head(letters)
>>> letters
['b','c']
The parametertand the variablelettersare aliases for the same object. The stack diagram
looks like Figure 10.5.
Since the list is shared by two frames, I drew it between them.
It is important to distinguish between operations that modify lists and operations that cre-
ate new lists. For example, theappendmethod modifies a list, but the+operator creates a
new list.
Here’s an example usingappend:
>>> t1 = [1, 2]
>>> t2 = t1.append(3)
>>> t1
[1, 2, 3]
>>> t2
None
```

Điểm: **2/2**. Lý do: Bắt đầu tại List arguments, có ví dụ delete_head với đầu vào/đầu ra, giải thích alias và phân biệt sửa list với tạo list mới. Ví dụ append cuối đoạn có đầy đủ kết quả None.

### C_p119

Chunk: `thinkpython2_B_p119_1_0`; bắt đầu ở ký tự 475.

```text
10.12 List arguments
When you pass a list to a function, the function gets a reference to the list. If the function
modifies the list, the caller sees the change. For example,delete_headremoves the first
element from a list:
def delete_head(t):
del t[0]
Here’s how it is used:
>>> letters = ['a','b','c']
>>> delete_head(letters)
>>> letters
['b','c']
The parametertand the variablelettersare aliases for the same object. The stack diagram
looks like Figure 10.5.
Since the list is shared by two frames, I drew it between them.
It is important to distinguish between operations that modify lists and operations that cre-
ate new lists. For example, theappendmethod modifies a list, but the+operator creates a
new list.
Here’s an example usingappend:
>>> t1 = [1, 2]
>>> t2 = t1.append(3)
>>> t1
[1, 2, 3]
>>> t2
None
```

Điểm: **2/2**. Lý do: Bắt đầu tại List arguments, có ví dụ delete_head với đầu vào/đầu ra, giải thích alias và phân biệt sửa list với tạo list mới. Ví dụ append cuối đoạn có đầy đủ kết quả None. C dùng đúng cùng chunk với B tại vị trí này; filter truy xuất không thay đổi coherence của đoạn.

## Trang PDF 120 — mốc ký tự 740 (đếm từ 0)

### Nội dung trang nguồn để đối chiếu

```text
98 Chapter 10. Lists
The return value fromappendisNone.
Here’s an example using the+operator:
>>> t3 = t1 + [4]
>>> t1
[1, 2, 3]
>>> t3
[1, 2, 3, 4]
The result of the operator is a new list, and the original list is unchanged.
This difference is important when you write functions that are supposed to modify lists.
For example, this functiondoes notdelete the head of a list:
def bad_delete_head(t):
t = t[1:] # WRONG!
The slice operator creates a new list and the assignment makestrefer to it, but that doesn’t
affect the caller.
>>> t4 = [1, 2, 3]
>>> bad_delete_head(t4)
>>> t4
[1, 2, 3]
At the beginning ofbad_delete_head,tandt4refer to the same list. At the end,trefers
to a new list, butt4still refers to the original, unmodified list.
An alternative is to write a function that creates and returns a new list. For example,tail
returns all but the first element of a list:
def tail(t):
return t[1:]
This function leaves the original list unmodified. Here’s how it is used:
>>> letters = ['a','b','c']
>>> rest = tail(letters)
>>> rest
['b','c']
10.13 Debugging
Careless use of lists (and other mutable objects) can lead to long hours of debugging. Here
are some common pitfalls and ways to avoid them:
1. Most list methods modify the argument and returnNone. This is the opposite of the
string methods, which return a new string and leave the original alone.
If you are used to writing string code like this:
word = word.strip()
It is tempting to write list code like this:
```

### A_p120

Chunk: `thinkpython2_p120_450`; bắt đầu ở ký tự 450.

```text
ew list and the assignment makestrefer to it, but that doesn’t
affect the caller.
>>> t4 = [1, 2, 3]
>>> bad_delete_head(t4)
>>> t4
[1, 2, 3]
At the beginning ofbad_delete_head,tandt4refer to the same list. At the end,trefers
to a new list, butt4still refers to the original, unmodified list.
An alternative is to write a function that creates and returns a new list. For example,tail
returns all but the first element of a list:
def tail(t):
return t[1:]
This function leaves the original list unmod
```

Điểm: **1/2**. Lý do: Đầu đoạn mất một phần câu giải thích tạo list mới và thiếu định nghĩa bad_delete_head ở trước. Có định nghĩa tail nhưng câu giải thích cuối bị cắt giữa unmodified, nên ngữ cảnh chưa đầy đủ.

### B_p120

Chunk: `thinkpython2_B_p120_0_0`; bắt đầu ở ký tự 0.

```text
98 Chapter 10. Lists
The return value fromappendisNone.
Here’s an example using the+operator:
>>> t3 = t1 + [4]
>>> t1
[1, 2, 3]
>>> t3
[1, 2, 3, 4]
The result of the operator is a new list, and the original list is unchanged.
This difference is important when you write functions that are supposed to modify lists.
For example, this functiondoes notdelete the head of a list:
def bad_delete_head(t):
t = t[1:] # WRONG!
The slice operator creates a new list and the assignment makestrefer to it, but that doesn’t
affect the caller.
>>> t4 = [1, 2, 3]
>>> bad_delete_head(t4)
>>> t4
[1, 2, 3]
At the beginning ofbad_delete_head,tandt4refer to the same list. At the end,trefers
to a new list, butt4still refers to the original, unmodified list.
An alternative is to write a function that creates and returns a new list. For example,tail
returns all but the first element of a list:
def tail(t):
return t[1:]
This function leaves the original list unmodified. Here’s how it is used:
>>> letters = ['a','
```

Điểm: **1/2**. Lý do: Phần bad_delete_head có định nghĩa, ví dụ và giải thích vì sao không sửa list của người gọi. Tuy nhiên ví dụ nối từ trang trước dùng t1 chưa định nghĩa tại đây và ví dụ tail cuối đoạn bị cắt giữa khai báo letters.

### C_p120

Chunk: `thinkpython2_B_p120_0_0`; bắt đầu ở ký tự 0.

```text
98 Chapter 10. Lists
The return value fromappendisNone.
Here’s an example using the+operator:
>>> t3 = t1 + [4]
>>> t1
[1, 2, 3]
>>> t3
[1, 2, 3, 4]
The result of the operator is a new list, and the original list is unchanged.
This difference is important when you write functions that are supposed to modify lists.
For example, this functiondoes notdelete the head of a list:
def bad_delete_head(t):
t = t[1:] # WRONG!
The slice operator creates a new list and the assignment makestrefer to it, but that doesn’t
affect the caller.
>>> t4 = [1, 2, 3]
>>> bad_delete_head(t4)
>>> t4
[1, 2, 3]
At the beginning ofbad_delete_head,tandt4refer to the same list. At the end,trefers
to a new list, butt4still refers to the original, unmodified list.
An alternative is to write a function that creates and returns a new list. For example,tail
returns all but the first element of a list:
def tail(t):
return t[1:]
This function leaves the original list unmodified. Here’s how it is used:
>>> letters = ['a','
```

Điểm: **1/2**. Lý do: Phần bad_delete_head có định nghĩa, ví dụ và giải thích vì sao không sửa list của người gọi. Tuy nhiên ví dụ nối từ trang trước dùng t1 chưa định nghĩa tại đây và ví dụ tail cuối đoạn bị cắt giữa khai báo letters. C dùng đúng cùng chunk với B tại vị trí này; filter truy xuất không thay đổi coherence của đoạn.

