# Đánh giá metadata và grounding của kết quả test



Phương pháp: đọc và đối chiếu bằng chứng; nguồn, trang, chương được kiểm tra thêm trực tiếp bằng PDF.

## Tiêu chí đánh giá

- grounding_score: 0 = không có bằng chứng; 1 = có nhưng thiếu điều kiện/ngữ cảnh; 2 = đủ trả lời và truy nguồn.
- grounding_reason: giải thích vì sao top-3 đủ hoặc thiếu bằng chứng; ghi chunk/trang liên quan.
- metadata_correct: true/false cho mỗi hit sau khi đối chiếu source, page, chapter với trang nguồn.
- metadata_reason: ghi điều đã đối chiếu hoặc lỗi tìm thấy.
- filter_compliant: true/false cho mỗi hit nếu requested_filter không rỗng; nếu không yêu cầu filter thì giữ null (N/A).

Grounding xét tổng hợp cả 3 đoạn, khác với metric exact-quote trong một chunk. Không tự đổi evidence_hit thành điểm grounding. A/B không áp dụng filter nhưng vẫn có thể kiểm tra phạm vi kết quả khi câu hỏi yêu cầu.

## Kết quả tổng hợp

| Cấu hình | Grounding trung bình /2 | Metadata đúng | Top-3 đúng phạm vi câu yêu cầu lọc |
|---|---:|---:|---:|
| A | 1.6 | 15/15 | 1/1 |
| B | 1.6 | 15/15 | 1/1 |
| C | 1.6 | 15/15 | 1/1 |

Metadata đúng ở cả 45 kết quả. Điều đó giúp tìm lại trang gốc, nhưng không bảo đảm kết quả chứa câu trả lời. Ví dụ A_Q18 đúng nguồn và chương mà vẫn thiếu bằng chứng về toán tử in.

Câu Q19 yêu cầu chương 12. C có áp dụng bộ lọc; A/B không lọc nhưng lần này vẫn trả về các đoạn thuộc chương 12. Với một câu filter, chưa thấy mức cải thiện của C trên test.

Các câu thiếu bằng chứng: A_Q18, B_Q16 và C_Q16. Những câu còn lại có đủ thông tin để trả lời. Việc chunk bị cắt ở chỗ khác không tự động làm mất bằng chứng cần cho một câu hỏi cụ thể.

Giới hạn: tập test chỉ có 5 câu. Đây là đánh giá bằng chứng truy xuất, không phải độ chính xác câu trả lời do LLM tạo ra.

## A_Q16

**Câu hỏi:** Does a nested list count as one element when measuring the length of the outer list?

**Đáp án mong đợi:** Yes. A nested list counts as a single element.

Filter yêu cầu: `{}`; filter thực sự áp dụng: `{}`.

### Bằng chứng nguồn đã ghi trong benchmark

Trang PDF 113 — thinkpython2:

> Although a list can contain another list, the nested list still counts as a single element.

### Kết quả 1: thinkpython2_p113_900

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 113; chương: 10.

```text
pens.')
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
The first example repeats[0]four times. The second examp
```

### Kết quả 2: thinkpython2_p141_1350

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 141; chương: 12.

```text
eturn True
return False
If you need to traverse the elements of a sequence and their indices, you can use the built-in
functionenumerate:
for index, element in enumerate('abc'):
print(index, element)
The result fromenumerateis an enumerate object, which iterates a sequence of pairs; each
pair contains an index (starting from 0) and an element from the given sequence. In this
example, the output is
0 a
1 b
2 c
Again.
```

### Kết quả 3: thinkpython2_p143_1800

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 143; chương: 12.

```text
eversed,
which takes a sequence and returns an iterator that traverses the list in reverse order.
```

**Grounding: 2/2.** Đoạn đầu ở trang 113 nói rõ list lồng vẫn được tính là một phần tử. Có ví dụ nên đủ trả lời.

**Kiểm tra metadata:**

- Kết quả 1: Đã đối chiếu PDF: nội dung nằm ở trang 113, chương 10, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 2: Đã đối chiếu PDF: nội dung nằm ở trang 141, chương 12, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 3: Đã đối chiếu PDF: nội dung nằm ở trang 143, chương 12, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.

## A_Q17

**Câu hỏi:** Can a function change the caller’s list when that list is passed as an argument?

**Đáp án mong đợi:** Yes. The function receives a reference to the list, and its modifications are visible to the caller.

Filter yêu cầu: `{}`; filter thực sự áp dụng: `{}`.

### Bằng chứng nguồn đã ghi trong benchmark

Trang PDF 119 — thinkpython2:

> When you pass a list to a function, the function gets a reference to the list. If the function modifies the list, the caller sees the change.

### Kết quả 1: thinkpython2_p119_450

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 119; chương: 10.

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

### Kết quả 2: thinkpython2_p143_1350

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 143; chương: 12.

```text
 key, you have to use an immutable type
like a tuple or string.
3. If you are passing a sequence as an argument to a function, using tuples reduces the
potential for unexpected behavior due to aliasing.
Because tuples are immutable, they don’t provide methods likesortandreverse, which
modify existing lists. But Python provides the built-in functionsorted, which takes any
sequence and returns a new list with the same elements in sorted order, andreversed,
which takes a sequence and returns an ite
```

### Kết quả 3: thinkpython2_p120_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 120; chương: 10.

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
The slice operator creates a new list and the assignment makestrefer to it, but 
```

**Grounding: 2/2.** Đoạn đầu ở trang 119 nói hàm nhận tham chiếu đến list. Ví dụ delete_head cho thấy list của người gọi bị thay đổi.

**Kiểm tra metadata:**

- Kết quả 1: Đã đối chiếu PDF: nội dung nằm ở trang 119, chương 10, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 2: Đã đối chiếu PDF: nội dung nằm ở trang 143, chương 12, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 3: Đã đối chiếu PDF: nội dung nằm ở trang 120, chương 10, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.

## A_Q18

**Câu hỏi:** Does the in operator on a dictionary check values as well as keys?

**Đáp án mong đợi:** No. It checks keys; appearing as a value is not enough.

Filter yêu cầu: `{}`; filter thực sự áp dụng: `{}`.

### Bằng chứng nguồn đã ghi trong benchmark

Trang PDF 126 — thinkpython2:

> Theinoperator works on dictionaries, too; it tells you whether something appears as akey in the dictionary (appearing as a value is not good enough).

### Kết quả 1: thinkpython2_p130_1350

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 130; chương: 11.

```text
 a function that takes a value (of any kind) and returns an integer. Dictionaries
use these integers, called hash values, to store and look up key-value pairs.
This system works fine if the keys are immutable. But if the keys are mutable, like lists,
bad things happen. For example, when you create a key-value pair, Python hashes the key
and stores it in the corresponding location. If you modify the key and then hash it again, it
would go to a different location. In that case you might have two e
```

### Kết quả 2: thinkpython2_p125_450

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 125; chương: 11.

```text
a collection of
values. Each key is associated with a single value. The association of a key and a value is
called akey-value pairor sometimes anitem.
In mathematical language, a dictionary represents amappingfrom keys to values, so you
can also say that each key “maps to” a value. As an example, we’ll build a dictionary that
maps from English to Spanish words, so the keys and the values are all strings.
The functiondictcreates a new dictionary with no items. Becausedictis the name of a
built-in
```

### Kết quả 3: thinkpython2_p125_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 125; chương: 11.

```text
Chapter 11
Dictionaries
This chapter presents another built-in type called a dictionary. Dictionaries are one of
Python’s best features; they are the building blocks of many efficient and elegant algo-
rithms.
11.1 A dictionary is a mapping
Adictionaryis like a list, but more general. In a list, the indices have to be integers; in a
dictionary they can be (almost) any type.
A dictionary contains a collection of indices, which are calledkeys, and a collection of
values. Each key is associated wit
```

**Grounding: 0/2.** Các đoạn tìm được nói về key, value và hash. Không đoạn nào giải thích toán tử in kiểm tra key hay value nên chưa trả lời được.

**Kiểm tra metadata:**

- Kết quả 1: Đã đối chiếu PDF: nội dung nằm ở trang 130, chương 11, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 2: Đã đối chiếu PDF: nội dung nằm ở trang 125, chương 11, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 3: Đã đối chiếu PDF: nội dung nằm ở trang 125, chương 11, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.

## A_Q19

**Câu hỏi:** In Chapter 12 (Tuples), what is the important difference between tuples and lists?

**Đáp án mong đợi:** Tuples are immutable, whereas lists are mutable.

Filter yêu cầu: `{"chapter": 12}`; filter thực sự áp dụng: `{}`.

### Bằng chứng nguồn đã ghi trong benchmark

Trang PDF 137 — thinkpython2:

> A tuple is a sequence of values. The values can be any type, and they are indexed by integers, so in that respect tuples are a lot like lists. The important difference is that tuples are immutable.

### Kết quả 1: thinkpython2_p137_450

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 137; chương: 12.

```text
ple”.
12.1 T uples are immutable
A tuple is a sequence of values. The values can be any type, and they are indexed by
integers, so in that respect tuples are a lot like lists. The important difference is that tuples
are immutable.
Syntactically, a tuple is a comma-separated list of values:
>>> t ='a','b','c','d','e'
Although it is not necessary, it is common to enclose tuples in parentheses:
>>> t = ('a','b','c','d','e')
To create a tuple with a single element, you have to include a final comma:
```

### Kết quả 2: thinkpython2_p137_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 137; chương: 12.

```text
Chapter 12
T uples
This chapter presents one more built-in type, the tuple, and then shows how lists, dictionar-
ies, and tuples work together. I also present a useful feature for variable-length argument
lists, the gather and scatter operators.
One note: there is no consensus on how to pronounce “tuple”. Some people say “tuh-
ple”, which rhymes with “supple”. But in the context of programming, most people say
“too-ple”, which rhymes with “quadruple”.
12.1 T uples are immutable
A tuple is a sequ
```

### Kết quả 3: thinkpython2_p144_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 144; chương: 12.

```text
122 Chapter 12. T uples
12.8 Debugging
Lists, dictionaries and tuples are examples ofdata structures; in this chapter we are starting
to see compound data structures, like lists of tuples, or dictionaries that contain tuples as
keys and lists as values. Compound data structures are useful, but they are prone to what
I callshape errors; that is, errors caused when a data structure has the wrong type, size, or
structure. For example, if you are expecting a list with one integer and I give you a pl
```

**Grounding: 2/2.** Đoạn đầu ở trang 137 so sánh tuple với list và nêu khác biệt là tuple không thay đổi được. Đủ thông tin cho ý chính của câu hỏi.

**Kiểm tra metadata:**

- Kết quả 1: Đã đối chiếu PDF: nội dung nằm ở trang 137, chương 12, đúng nguồn Think Python. Kết quả thuộc chương 12, khớp chương 12 được yêu cầu.
- Kết quả 2: Đã đối chiếu PDF: nội dung nằm ở trang 137, chương 12, đúng nguồn Think Python. Kết quả thuộc chương 12, khớp chương 12 được yêu cầu.
- Kết quả 3: Đã đối chiếu PDF: nội dung nằm ở trang 144, chương 12, đúng nguồn Think Python. Kết quả thuộc chương 12, khớp chương 12 được yêu cầu.

## A_Q20

**Câu hỏi:** How can a tuple of values be passed to a function as multiple arguments?

**Đáp án mong đợi:** Use the * operator to unpack, or scatter, the tuple.

Filter yêu cầu: `{}`; filter thực sự áp dụng: `{}`.

### Bằng chứng nguồn đã ghi trong benchmark

Trang PDF 140 — thinkpython2:

> If you have a sequence of values and you want to pass it to a function as multiple arguments, you can use the*operator.

### Kết quả 1: thinkpython2_p140_450

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 140; chương: 12.

```text
tter. If you have a sequence of values and you want to pass
it to a function as multiple arguments, you can use the*operator. For example,divmod
takes exactly two arguments; it doesn’t work with a tuple:
>>> t = (7, 3)
>>> divmod(t)
TypeError: divmod expected 2 arguments, got 1
But if you scatter the tuple, it works:
>>> divmod(*t)
(2, 1)
Many of the built-in functions use variable-length argument tuples. For example,maxand
mincan take any number of arguments:
>>> max(1, 2, 3)
3
Butsumdoes not.

```

### Kết quả 2: thinkpython2_p140_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 140; chương: 12.

```text
118 Chapter 12. T uples
12.4 Variable-length argument tuples
Functions can take a variable number of arguments. A parameter name that begins with
*gathersarguments into a tuple. For example,printalltakes any number of arguments
and prints them:
def printall(*args):
print(args)
The gather parameter can have any name you like, butargsis conventional. Here’s how
the function works:
>>> printall(1, 2.0,'3')
(1, 2.0,'3')
The complement of gather isscatter. If you have a sequence of values and you wan
```

### Kết quả 3: thinkpython2_p137_900

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 137; chương: 12.

```text
single element, you have to include a final comma:
>>> t1 ='a',
>>> type(t1)
<class'tuple'>
A value in parentheses is not a tuple:
>>> t2 = ('a')
>>> type(t2)
<class'str'>
Another way to create a tuple is the built-in functiontuple. With no argument, it creates
an empty tuple:
>>> t = tuple()
>>> t
()
```

**Grounding: 2/2.** Đoạn đầu ở trang 140 nói dùng dấu * để truyền các phần tử thành nhiều đối số. Có ví dụ divmod(*t) nên đủ trả lời.

**Kiểm tra metadata:**

- Kết quả 1: Đã đối chiếu PDF: nội dung nằm ở trang 140, chương 12, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 2: Đã đối chiếu PDF: nội dung nằm ở trang 140, chương 12, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 3: Đã đối chiếu PDF: nội dung nằm ở trang 137, chương 12, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.

## B_Q16

**Câu hỏi:** Does a nested list count as one element when measuring the length of the outer list?

**Đáp án mong đợi:** Yes. A nested list counts as a single element.

Filter yêu cầu: `{}`; filter thực sự áp dụng: `{}`.

### Bằng chứng nguồn đã ghi trong benchmark

Trang PDF 113 — thinkpython2:

> Although a list can contain another list, the nested list still counts as a single element.

### Kết quả 1: thinkpython2_B_p113_3_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 113; chương: 10.

```text
10.5 List slices
The slice operator also works on lists:
```

### Kết quả 2: thinkpython2_B_p141_0_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 141; chương: 12.

```text
12.5. Lists and tuples 119
>>> for pair in zip(s, t):
... print(pair)
...
('a', 0)
('b', 1)
('c', 2)
A zip object is a kind ofiterator, which is any object that iterates through a sequence.
Iterators are similar to lists in some ways, but unlike lists, you can’t use an index to select
an element from an iterator.
If you want to use list operators and methods, you can use a zip object to make a list:
>>> list(zip(s, t))
[('a', 0), ('b', 1), ('c', 2)]
The result is a list of tuples; in this example, each tuple contains a character from the string
and the corresponding element from the list.
If the sequences are not the same length, the result has the length of the shorter one.
>>> list(zip('Anne','Elk'))
[('A','E'), ('n','l'), ('n','k')]
You can use tuple assignment in aforloop to traverse a list of tuples:
t = [('a', 0), ('b', 1), ('c', 2)]
for letter, number in t:
print(number, letter)
Each time through the loop, Python selects the next tuple in the list and assigns the ele-
ments tole
```

### Kết quả 3: thinkpython2_B_p113_2_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 113; chương: 10.

```text
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
```

**Grounding: 0/2.** Kết quả nói về slice, zip và phép toán trên list. Không có đoạn giải thích list lồng được tính là một phần tử, dù hai đoạn nằm đúng trang 113.

**Kiểm tra metadata:**

- Kết quả 1: Đã đối chiếu PDF: nội dung nằm ở trang 113, chương 10, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 2: Đã đối chiếu PDF: nội dung nằm ở trang 141, chương 12, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 3: Đã đối chiếu PDF: nội dung nằm ở trang 113, chương 10, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.

## B_Q17

**Câu hỏi:** Can a function change the caller’s list when that list is passed as an argument?

**Đáp án mong đợi:** Yes. The function receives a reference to the list, and its modifications are visible to the caller.

Filter yêu cầu: `{}`; filter thực sự áp dụng: `{}`.

### Bằng chứng nguồn đã ghi trong benchmark

Trang PDF 119 — thinkpython2:

> When you pass a list to a function, the function gets a reference to the list. If the function modifies the list, the caller sees the change.

### Kết quả 1: thinkpython2_B_p119_1_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 119; chương: 10.

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

### Kết quả 2: thinkpython2_B_p120_0_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 120; chương: 10.

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

### Kết quả 3: thinkpython2_B_p143_1_1000

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 143; chương: 12.

```text
as a dictionary key, you have to use an immutable type
like a tuple or string.
3. If you are passing a sequence as an argument to a function, using tuples reduces the
potential for unexpected behavior due to aliasing.
Because tuples are immutable, they don’t provide methods likesortandreverse, which
modify existing lists. But Python provides the built-in functionsorted, which takes any
sequence and returns a new list with the same elements in sorted order, andreversed,
which takes a sequence and returns an iterator that traverses the list in reverse order.
```

**Grounding: 2/2.** Đoạn đầu ở trang 119 giải thích list được truyền bằng tham chiếu và có ví dụ sửa list. Đủ trả lời câu hỏi.

**Kiểm tra metadata:**

- Kết quả 1: Đã đối chiếu PDF: nội dung nằm ở trang 119, chương 10, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 2: Đã đối chiếu PDF: nội dung nằm ở trang 120, chương 10, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 3: Đã đối chiếu PDF: nội dung nằm ở trang 143, chương 12, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.

## B_Q18

**Câu hỏi:** Does the in operator on a dictionary check values as well as keys?

**Đáp án mong đợi:** No. It checks keys; appearing as a value is not enough.

Filter yêu cầu: `{}`; filter thực sự áp dụng: `{}`.

### Bằng chứng nguồn đã ghi trong benchmark

Trang PDF 126 — thinkpython2:

> Theinoperator works on dictionaries, too; it tells you whether something appears as akey in the dictionary (appearing as a value is not good enough).

### Kết quả 1: thinkpython2_B_p130_0_1000

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 130; chương: 11.

```text
ample shows, but they cannot be keys. Here’s
what happens if you try:
>>> t = [1, 2, 3]
>>> d = dict()
>>> d[t] ='oops'
Traceback (most recent call last):
File "<stdin>", line 1, in ?
TypeError: list objects are unhashable
I mentioned earlier that a dictionary is implemented using a hashtable and that means that
the keys have to behashable.
Ahashis a function that takes a value (of any kind) and returns an integer. Dictionaries
use these integers, called hash values, to store and look up key-value pairs.
This system works fine if the keys are immutable. But if the keys are mutable, like lists,
bad things happen. For example, when you create a key-value pair, Python hashes the key
and stores it in the corresponding location. If you modify the key and then hash it again, it
would go to a different location. In that case you might have two entries for the same key,
or you might not be able to find a key. Either way, the dictionary wouldn’t work correctly.
That’s why keys have to be hashab
```

### Kết quả 2: thinkpython2_B_p125_1_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 125; chương: 11.

```text
11.1 A dictionary is a mapping
Adictionaryis like a list, but more general. In a list, the indices have to be integers; in a
dictionary they can be (almost) any type.
A dictionary contains a collection of indices, which are calledkeys, and a collection of
values. Each key is associated with a single value. The association of a key and a value is
called akey-value pairor sometimes anitem.
In mathematical language, a dictionary represents amappingfrom keys to values, so you
can also say that each key “maps to” a value. As an example, we’ll build a dictionary that
maps from English to Spanish words, so the keys and the values are all strings.
The functiondictcreates a new dictionary with no items. Becausedictis the name of a
built-in function, you should avoid using it as a variable name.
>>> eng2sp = dict()
>>> eng2sp
{}
The squiggly-brackets,{}, represent an empty dictionary. To add items to the dictionary,
you can use square brackets:
>>> eng2sp['one'] ='uno'
This line creates an item
```

### Kết quả 3: thinkpython2_B_p126_0_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 126; chương: 11.

```text
104 Chapter 11. Dictionaries
>>> eng2sp = {'one':'uno','two':'dos','three':'tres'}
But if you printeng2sp, you might be surprised:
>>> eng2sp
{'one':'uno','three':'tres','two':'dos'}
The order of the key-value pairs might not be the same. If you type the same example
on your computer, you might get a different result. In general, the order of items in a
dictionary is unpredictable.
But that’s not a problem because the elements of a dictionary are never indexed with inte-
ger indices. Instead, you use the keys to look up the corresponding values:
>>> eng2sp['two']
'dos'
The key'two'always maps to the value'dos'so the order of the items doesn’t matter.
If the key isn’t in the dictionary, you get an exception:
>>> eng2sp['four']
KeyError:'four'
Thelenfunction works on dictionaries; it returns the number of key-value pairs:
>>> len(eng2sp)
3
Theinoperator works on dictionaries, too; it tells you whether something appears as akey
in the dictionary (appearing as a value is not good enough).
```

**Grounding: 2/2.** Đoạn thứ ba ở trang 126 nói rõ in kiểm tra key, chỉ xuất hiện ở value thì chưa đủ. Hai đoạn đầu không trả lời trực tiếp nhưng top-3 vẫn có đủ bằng chứng.

**Kiểm tra metadata:**

- Kết quả 1: Đã đối chiếu PDF: nội dung nằm ở trang 130, chương 11, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 2: Đã đối chiếu PDF: nội dung nằm ở trang 125, chương 11, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 3: Đã đối chiếu PDF: nội dung nằm ở trang 126, chương 11, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.

## B_Q19

**Câu hỏi:** In Chapter 12 (Tuples), what is the important difference between tuples and lists?

**Đáp án mong đợi:** Tuples are immutable, whereas lists are mutable.

Filter yêu cầu: `{"chapter": 12}`; filter thực sự áp dụng: `{}`.

### Bằng chứng nguồn đã ghi trong benchmark

Trang PDF 137 — thinkpython2:

> A tuple is a sequence of values. The values can be any type, and they are indexed by integers, so in that respect tuples are a lot like lists. The important difference is that tuples are immutable.

### Kết quả 1: thinkpython2_B_p137_1_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 137; chương: 12.

```text
12.1 T uples are immutable
A tuple is a sequence of values. The values can be any type, and they are indexed by
integers, so in that respect tuples are a lot like lists. The important difference is that tuples
are immutable.
Syntactically, a tuple is a comma-separated list of values:
>>> t ='a','b','c','d','e'
Although it is not necessary, it is common to enclose tuples in parentheses:
>>> t = ('a','b','c','d','e')
To create a tuple with a single element, you have to include a final comma:
>>> t1 ='a',
>>> type(t1)
<class'tuple'>
A value in parentheses is not a tuple:
>>> t2 = ('a')
>>> type(t2)
<class'str'>
Another way to create a tuple is the built-in functiontuple. With no argument, it creates
an empty tuple:
>>> t = tuple()
>>> t
()
```

### Kết quả 2: thinkpython2_B_p144_2_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 144; chương: 12.

```text
12.9 Glossary
tuple:An immutable sequence of elements.
tuple assignment:An assignment with a sequence on the right side and a tuple of vari-
ables on the left. The right side is evaluated and then its elements are assigned to the
variables on the left.
```

### Kết quả 3: thinkpython2_B_p143_1_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 143; chương: 12.

```text
12.7 Sequences of sequences
I have focused on lists of tuples, but almost all of the examples in this chapter also work
with lists of lists, tuples of tuples, and tuples of lists. To avoid enumerating the possible
combinations, it is sometimes easier to talk about sequences of sequences.
In many contexts, the different kinds of sequences (strings, lists and tuples) can be used
interchangeably. So how should you choose one over the others?
To start with the obvious, strings are more limited than other sequences because the ele-
ments have to be characters. They are also immutable. If you need the ability to change the
characters in a string (as opposed to creating a new string), you might want to use a list of
characters instead.
Lists are more common than tuples, mostly because they are mutable. But there are a few
cases where you might prefer tuples:
1. In some contexts, like areturnstatement, it is syntactically simpler to create a tuple
than a list.
2. If you want to use a sequence
```

**Grounding: 2/2.** Trang 137 nói tuple không thay đổi được. Đoạn ở trang 143 còn nói list có thể thay đổi, nên top-3 đủ để so sánh.

**Kiểm tra metadata:**

- Kết quả 1: Đã đối chiếu PDF: nội dung nằm ở trang 137, chương 12, đúng nguồn Think Python. Kết quả thuộc chương 12, khớp chương 12 được yêu cầu.
- Kết quả 2: Đã đối chiếu PDF: nội dung nằm ở trang 144, chương 12, đúng nguồn Think Python. Kết quả thuộc chương 12, khớp chương 12 được yêu cầu.
- Kết quả 3: Đã đối chiếu PDF: nội dung nằm ở trang 143, chương 12, đúng nguồn Think Python. Kết quả thuộc chương 12, khớp chương 12 được yêu cầu.

## B_Q20

**Câu hỏi:** How can a tuple of values be passed to a function as multiple arguments?

**Đáp án mong đợi:** Use the * operator to unpack, or scatter, the tuple.

Filter yêu cầu: `{}`; filter thực sự áp dụng: `{}`.

### Bằng chứng nguồn đã ghi trong benchmark

Trang PDF 140 — thinkpython2:

> If you have a sequence of values and you want to pass it to a function as multiple arguments, you can use the*operator.

### Kết quả 1: thinkpython2_B_p140_1_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 140; chương: 12.

```text
12.4 Variable-length argument tuples
Functions can take a variable number of arguments. A parameter name that begins with
*gathersarguments into a tuple. For example,printalltakes any number of arguments
and prints them:
def printall(*args):
print(args)
The gather parameter can have any name you like, butargsis conventional. Here’s how
the function works:
>>> printall(1, 2.0,'3')
(1, 2.0,'3')
The complement of gather isscatter. If you have a sequence of values and you want to pass
it to a function as multiple arguments, you can use the*operator. For example,divmod
takes exactly two arguments; it doesn’t work with a tuple:
>>> t = (7, 3)
>>> divmod(t)
TypeError: divmod expected 2 arguments, got 1
But if you scatter the tuple, it works:
>>> divmod(*t)
(2, 1)
Many of the built-in functions use variable-length argument tuples. For example,maxand
mincan take any number of arguments:
>>> max(1, 2, 3)
3
Butsumdoes not.
>>> sum(1, 2, 3)
TypeError: sum expected at most 2 arguments, got 3
As an
```

### Kết quả 2: thinkpython2_B_p137_1_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 137; chương: 12.

```text
12.1 T uples are immutable
A tuple is a sequence of values. The values can be any type, and they are indexed by
integers, so in that respect tuples are a lot like lists. The important difference is that tuples
are immutable.
Syntactically, a tuple is a comma-separated list of values:
>>> t ='a','b','c','d','e'
Although it is not necessary, it is common to enclose tuples in parentheses:
>>> t = ('a','b','c','d','e')
To create a tuple with a single element, you have to include a final comma:
>>> t1 ='a',
>>> type(t1)
<class'tuple'>
A value in parentheses is not a tuple:
>>> t2 = ('a')
>>> type(t2)
<class'str'>
Another way to create a tuple is the built-in functiontuple. With no argument, it creates
an empty tuple:
>>> t = tuple()
>>> t
()
```

### Kết quả 3: thinkpython2_B_p144_2_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 144; chương: 12.

```text
12.9 Glossary
tuple:An immutable sequence of elements.
tuple assignment:An assignment with a sequence on the right side and a tuple of vari-
ables on the left. The right side is evaluated and then its elements are assigned to the
variables on the left.
```

**Grounding: 2/2.** Đoạn đầu ở trang 140 giải thích cách dùng dấu * và có ví dụ divmod(*t). Đủ bằng chứng để trả lời.

**Kiểm tra metadata:**

- Kết quả 1: Đã đối chiếu PDF: nội dung nằm ở trang 140, chương 12, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 2: Đã đối chiếu PDF: nội dung nằm ở trang 137, chương 12, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 3: Đã đối chiếu PDF: nội dung nằm ở trang 144, chương 12, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.

## C_Q16

**Câu hỏi:** Does a nested list count as one element when measuring the length of the outer list?

**Đáp án mong đợi:** Yes. A nested list counts as a single element.

Filter yêu cầu: `{}`; filter thực sự áp dụng: `{}`.

### Bằng chứng nguồn đã ghi trong benchmark

Trang PDF 113 — thinkpython2:

> Although a list can contain another list, the nested list still counts as a single element.

### Kết quả 1: thinkpython2_B_p113_3_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 113; chương: 10.

```text
10.5 List slices
The slice operator also works on lists:
```

### Kết quả 2: thinkpython2_B_p141_0_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 141; chương: 12.

```text
12.5. Lists and tuples 119
>>> for pair in zip(s, t):
... print(pair)
...
('a', 0)
('b', 1)
('c', 2)
A zip object is a kind ofiterator, which is any object that iterates through a sequence.
Iterators are similar to lists in some ways, but unlike lists, you can’t use an index to select
an element from an iterator.
If you want to use list operators and methods, you can use a zip object to make a list:
>>> list(zip(s, t))
[('a', 0), ('b', 1), ('c', 2)]
The result is a list of tuples; in this example, each tuple contains a character from the string
and the corresponding element from the list.
If the sequences are not the same length, the result has the length of the shorter one.
>>> list(zip('Anne','Elk'))
[('A','E'), ('n','l'), ('n','k')]
You can use tuple assignment in aforloop to traverse a list of tuples:
t = [('a', 0), ('b', 1), ('c', 2)]
for letter, number in t:
print(number, letter)
Each time through the loop, Python selects the next tuple in the list and assigns the ele-
ments tole
```

### Kết quả 3: thinkpython2_B_p113_2_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 113; chương: 10.

```text
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
```

**Grounding: 0/2.** Kết quả nói về slice, zip và phép toán trên list. Không có đoạn giải thích list lồng được tính là một phần tử, dù hai đoạn nằm đúng trang 113. Kết quả C ở câu này giống B.

**Kiểm tra metadata:**

- Kết quả 1: Đã đối chiếu PDF: nội dung nằm ở trang 113, chương 10, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 2: Đã đối chiếu PDF: nội dung nằm ở trang 141, chương 12, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 3: Đã đối chiếu PDF: nội dung nằm ở trang 113, chương 10, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.

## C_Q17

**Câu hỏi:** Can a function change the caller’s list when that list is passed as an argument?

**Đáp án mong đợi:** Yes. The function receives a reference to the list, and its modifications are visible to the caller.

Filter yêu cầu: `{}`; filter thực sự áp dụng: `{}`.

### Bằng chứng nguồn đã ghi trong benchmark

Trang PDF 119 — thinkpython2:

> When you pass a list to a function, the function gets a reference to the list. If the function modifies the list, the caller sees the change.

### Kết quả 1: thinkpython2_B_p119_1_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 119; chương: 10.

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

### Kết quả 2: thinkpython2_B_p120_0_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 120; chương: 10.

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

### Kết quả 3: thinkpython2_B_p143_1_1000

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 143; chương: 12.

```text
as a dictionary key, you have to use an immutable type
like a tuple or string.
3. If you are passing a sequence as an argument to a function, using tuples reduces the
potential for unexpected behavior due to aliasing.
Because tuples are immutable, they don’t provide methods likesortandreverse, which
modify existing lists. But Python provides the built-in functionsorted, which takes any
sequence and returns a new list with the same elements in sorted order, andreversed,
which takes a sequence and returns an iterator that traverses the list in reverse order.
```

**Grounding: 2/2.** Đoạn đầu ở trang 119 giải thích list được truyền bằng tham chiếu và có ví dụ sửa list. Đủ trả lời câu hỏi. Kết quả C ở câu này giống B.

**Kiểm tra metadata:**

- Kết quả 1: Đã đối chiếu PDF: nội dung nằm ở trang 119, chương 10, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 2: Đã đối chiếu PDF: nội dung nằm ở trang 120, chương 10, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 3: Đã đối chiếu PDF: nội dung nằm ở trang 143, chương 12, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.

## C_Q18

**Câu hỏi:** Does the in operator on a dictionary check values as well as keys?

**Đáp án mong đợi:** No. It checks keys; appearing as a value is not enough.

Filter yêu cầu: `{}`; filter thực sự áp dụng: `{}`.

### Bằng chứng nguồn đã ghi trong benchmark

Trang PDF 126 — thinkpython2:

> Theinoperator works on dictionaries, too; it tells you whether something appears as akey in the dictionary (appearing as a value is not good enough).

### Kết quả 1: thinkpython2_B_p130_0_1000

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 130; chương: 11.

```text
ample shows, but they cannot be keys. Here’s
what happens if you try:
>>> t = [1, 2, 3]
>>> d = dict()
>>> d[t] ='oops'
Traceback (most recent call last):
File "<stdin>", line 1, in ?
TypeError: list objects are unhashable
I mentioned earlier that a dictionary is implemented using a hashtable and that means that
the keys have to behashable.
Ahashis a function that takes a value (of any kind) and returns an integer. Dictionaries
use these integers, called hash values, to store and look up key-value pairs.
This system works fine if the keys are immutable. But if the keys are mutable, like lists,
bad things happen. For example, when you create a key-value pair, Python hashes the key
and stores it in the corresponding location. If you modify the key and then hash it again, it
would go to a different location. In that case you might have two entries for the same key,
or you might not be able to find a key. Either way, the dictionary wouldn’t work correctly.
That’s why keys have to be hashab
```

### Kết quả 2: thinkpython2_B_p125_1_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 125; chương: 11.

```text
11.1 A dictionary is a mapping
Adictionaryis like a list, but more general. In a list, the indices have to be integers; in a
dictionary they can be (almost) any type.
A dictionary contains a collection of indices, which are calledkeys, and a collection of
values. Each key is associated with a single value. The association of a key and a value is
called akey-value pairor sometimes anitem.
In mathematical language, a dictionary represents amappingfrom keys to values, so you
can also say that each key “maps to” a value. As an example, we’ll build a dictionary that
maps from English to Spanish words, so the keys and the values are all strings.
The functiondictcreates a new dictionary with no items. Becausedictis the name of a
built-in function, you should avoid using it as a variable name.
>>> eng2sp = dict()
>>> eng2sp
{}
The squiggly-brackets,{}, represent an empty dictionary. To add items to the dictionary,
you can use square brackets:
>>> eng2sp['one'] ='uno'
This line creates an item
```

### Kết quả 3: thinkpython2_B_p126_0_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 126; chương: 11.

```text
104 Chapter 11. Dictionaries
>>> eng2sp = {'one':'uno','two':'dos','three':'tres'}
But if you printeng2sp, you might be surprised:
>>> eng2sp
{'one':'uno','three':'tres','two':'dos'}
The order of the key-value pairs might not be the same. If you type the same example
on your computer, you might get a different result. In general, the order of items in a
dictionary is unpredictable.
But that’s not a problem because the elements of a dictionary are never indexed with inte-
ger indices. Instead, you use the keys to look up the corresponding values:
>>> eng2sp['two']
'dos'
The key'two'always maps to the value'dos'so the order of the items doesn’t matter.
If the key isn’t in the dictionary, you get an exception:
>>> eng2sp['four']
KeyError:'four'
Thelenfunction works on dictionaries; it returns the number of key-value pairs:
>>> len(eng2sp)
3
Theinoperator works on dictionaries, too; it tells you whether something appears as akey
in the dictionary (appearing as a value is not good enough).
```

**Grounding: 2/2.** Đoạn thứ ba ở trang 126 nói rõ in kiểm tra key, chỉ xuất hiện ở value thì chưa đủ. Hai đoạn đầu không trả lời trực tiếp nhưng top-3 vẫn có đủ bằng chứng. Kết quả C ở câu này giống B.

**Kiểm tra metadata:**

- Kết quả 1: Đã đối chiếu PDF: nội dung nằm ở trang 130, chương 11, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 2: Đã đối chiếu PDF: nội dung nằm ở trang 125, chương 11, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 3: Đã đối chiếu PDF: nội dung nằm ở trang 126, chương 11, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.

## C_Q19

**Câu hỏi:** In Chapter 12 (Tuples), what is the important difference between tuples and lists?

**Đáp án mong đợi:** Tuples are immutable, whereas lists are mutable.

Filter yêu cầu: `{"chapter": 12}`; filter thực sự áp dụng: `{"chapter": 12}`.

### Bằng chứng nguồn đã ghi trong benchmark

Trang PDF 137 — thinkpython2:

> A tuple is a sequence of values. The values can be any type, and they are indexed by integers, so in that respect tuples are a lot like lists. The important difference is that tuples are immutable.

### Kết quả 1: thinkpython2_B_p137_1_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 137; chương: 12.

```text
12.1 T uples are immutable
A tuple is a sequence of values. The values can be any type, and they are indexed by
integers, so in that respect tuples are a lot like lists. The important difference is that tuples
are immutable.
Syntactically, a tuple is a comma-separated list of values:
>>> t ='a','b','c','d','e'
Although it is not necessary, it is common to enclose tuples in parentheses:
>>> t = ('a','b','c','d','e')
To create a tuple with a single element, you have to include a final comma:
>>> t1 ='a',
>>> type(t1)
<class'tuple'>
A value in parentheses is not a tuple:
>>> t2 = ('a')
>>> type(t2)
<class'str'>
Another way to create a tuple is the built-in functiontuple. With no argument, it creates
an empty tuple:
>>> t = tuple()
>>> t
()
```

### Kết quả 2: thinkpython2_B_p144_2_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 144; chương: 12.

```text
12.9 Glossary
tuple:An immutable sequence of elements.
tuple assignment:An assignment with a sequence on the right side and a tuple of vari-
ables on the left. The right side is evaluated and then its elements are assigned to the
variables on the left.
```

### Kết quả 3: thinkpython2_B_p143_1_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 143; chương: 12.

```text
12.7 Sequences of sequences
I have focused on lists of tuples, but almost all of the examples in this chapter also work
with lists of lists, tuples of tuples, and tuples of lists. To avoid enumerating the possible
combinations, it is sometimes easier to talk about sequences of sequences.
In many contexts, the different kinds of sequences (strings, lists and tuples) can be used
interchangeably. So how should you choose one over the others?
To start with the obvious, strings are more limited than other sequences because the ele-
ments have to be characters. They are also immutable. If you need the ability to change the
characters in a string (as opposed to creating a new string), you might want to use a list of
characters instead.
Lists are more common than tuples, mostly because they are mutable. But there are a few
cases where you might prefer tuples:
1. In some contexts, like areturnstatement, it is syntactically simpler to create a tuple
than a list.
2. If you want to use a sequence
```

**Grounding: 2/2.** Trang 137 nói tuple không thay đổi được. Đoạn ở trang 143 còn nói list có thể thay đổi, nên top-3 đủ để so sánh. Kết quả C ở câu này giống B.

**Kiểm tra metadata:**

- Kết quả 1: Đã đối chiếu PDF: nội dung nằm ở trang 137, chương 12, đúng nguồn Think Python. Kết quả thuộc chương 12, khớp chương 12 được yêu cầu.
- Kết quả 2: Đã đối chiếu PDF: nội dung nằm ở trang 144, chương 12, đúng nguồn Think Python. Kết quả thuộc chương 12, khớp chương 12 được yêu cầu.
- Kết quả 3: Đã đối chiếu PDF: nội dung nằm ở trang 143, chương 12, đúng nguồn Think Python. Kết quả thuộc chương 12, khớp chương 12 được yêu cầu.

## C_Q20

**Câu hỏi:** How can a tuple of values be passed to a function as multiple arguments?

**Đáp án mong đợi:** Use the * operator to unpack, or scatter, the tuple.

Filter yêu cầu: `{}`; filter thực sự áp dụng: `{}`.

### Bằng chứng nguồn đã ghi trong benchmark

Trang PDF 140 — thinkpython2:

> If you have a sequence of values and you want to pass it to a function as multiple arguments, you can use the*operator.

### Kết quả 1: thinkpython2_B_p140_1_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 140; chương: 12.

```text
12.4 Variable-length argument tuples
Functions can take a variable number of arguments. A parameter name that begins with
*gathersarguments into a tuple. For example,printalltakes any number of arguments
and prints them:
def printall(*args):
print(args)
The gather parameter can have any name you like, butargsis conventional. Here’s how
the function works:
>>> printall(1, 2.0,'3')
(1, 2.0,'3')
The complement of gather isscatter. If you have a sequence of values and you want to pass
it to a function as multiple arguments, you can use the*operator. For example,divmod
takes exactly two arguments; it doesn’t work with a tuple:
>>> t = (7, 3)
>>> divmod(t)
TypeError: divmod expected 2 arguments, got 1
But if you scatter the tuple, it works:
>>> divmod(*t)
(2, 1)
Many of the built-in functions use variable-length argument tuples. For example,maxand
mincan take any number of arguments:
>>> max(1, 2, 3)
3
Butsumdoes not.
>>> sum(1, 2, 3)
TypeError: sum expected at most 2 arguments, got 3
As an
```

### Kết quả 2: thinkpython2_B_p137_1_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 137; chương: 12.

```text
12.1 T uples are immutable
A tuple is a sequence of values. The values can be any type, and they are indexed by
integers, so in that respect tuples are a lot like lists. The important difference is that tuples
are immutable.
Syntactically, a tuple is a comma-separated list of values:
>>> t ='a','b','c','d','e'
Although it is not necessary, it is common to enclose tuples in parentheses:
>>> t = ('a','b','c','d','e')
To create a tuple with a single element, you have to include a final comma:
>>> t1 ='a',
>>> type(t1)
<class'tuple'>
A value in parentheses is not a tuple:
>>> t2 = ('a')
>>> type(t2)
<class'str'>
Another way to create a tuple is the built-in functiontuple. With no argument, it creates
an empty tuple:
>>> t = tuple()
>>> t
()
```

### Kết quả 3: thinkpython2_B_p144_2_0

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf
Trang PDF: 144; chương: 12.

```text
12.9 Glossary
tuple:An immutable sequence of elements.
tuple assignment:An assignment with a sequence on the right side and a tuple of vari-
ables on the left. The right side is evaluated and then its elements are assigned to the
variables on the left.
```

**Grounding: 2/2.** Đoạn đầu ở trang 140 giải thích cách dùng dấu * và có ví dụ divmod(*t). Đủ bằng chứng để trả lời. Kết quả C ở câu này giống B.

**Kiểm tra metadata:**

- Kết quả 1: Đã đối chiếu PDF: nội dung nằm ở trang 140, chương 12, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 2: Đã đối chiếu PDF: nội dung nằm ở trang 137, chương 12, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.
- Kết quả 3: Đã đối chiếu PDF: nội dung nằm ở trang 144, chương 12, đúng nguồn Think Python. Câu hỏi không yêu cầu lọc, nên không chấm mục này.

# Phụ lục: văn bản từng trang nguồn để đối chiếu

Số trang ở đây là trang vật lý trong file PDF. Metadata chương và bản trích xuất có thể kiểm tra lại bằng PDF gốc.

## Trang PDF 113 — chương 10

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf

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

## Trang PDF 119 — chương 10

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf

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

## Trang PDF 120 — chương 10

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf

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

## Trang PDF 125 — chương 11

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf

```text
Chapter 11
Dictionaries
This chapter presents another built-in type called a dictionary. Dictionaries are one of
Python’s best features; they are the building blocks of many efficient and elegant algo-
rithms.
11.1 A dictionary is a mapping
Adictionaryis like a list, but more general. In a list, the indices have to be integers; in a
dictionary they can be (almost) any type.
A dictionary contains a collection of indices, which are calledkeys, and a collection of
values. Each key is associated with a single value. The association of a key and a value is
called akey-value pairor sometimes anitem.
In mathematical language, a dictionary represents amappingfrom keys to values, so you
can also say that each key “maps to” a value. As an example, we’ll build a dictionary that
maps from English to Spanish words, so the keys and the values are all strings.
The functiondictcreates a new dictionary with no items. Becausedictis the name of a
built-in function, you should avoid using it as a variable name.
>>> eng2sp = dict()
>>> eng2sp
{}
The squiggly-brackets,{}, represent an empty dictionary. To add items to the dictionary,
you can use square brackets:
>>> eng2sp['one'] ='uno'
This line creates an item that maps from the key'one'to the value'uno'. If we print the
dictionary again, we see a key-value pair with a colon between the key and value:
>>> eng2sp
{'one':'uno'}
This output format is also an input format. For example, you can create a new dictionary
with three items:
```

## Trang PDF 126 — chương 11

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf

```text
104 Chapter 11. Dictionaries
>>> eng2sp = {'one':'uno','two':'dos','three':'tres'}
But if you printeng2sp, you might be surprised:
>>> eng2sp
{'one':'uno','three':'tres','two':'dos'}
The order of the key-value pairs might not be the same. If you type the same example
on your computer, you might get a different result. In general, the order of items in a
dictionary is unpredictable.
But that’s not a problem because the elements of a dictionary are never indexed with inte-
ger indices. Instead, you use the keys to look up the corresponding values:
>>> eng2sp['two']
'dos'
The key'two'always maps to the value'dos'so the order of the items doesn’t matter.
If the key isn’t in the dictionary, you get an exception:
>>> eng2sp['four']
KeyError:'four'
Thelenfunction works on dictionaries; it returns the number of key-value pairs:
>>> len(eng2sp)
3
Theinoperator works on dictionaries, too; it tells you whether something appears as akey
in the dictionary (appearing as a value is not good enough).
>>>'one'in eng2sp
True
>>>'uno'in eng2sp
False
To see whether something appears as a value in a dictionary, you can use the method
values, which returns a collection of values, and then use theinoperator:
>>> vals = eng2sp.values()
>>>'uno'in vals
True
Theinoperator uses different algorithms for lists and dictionaries. For lists, it searches the
elements of the list in order, as in Section 8.6. As the list gets longer, the search time gets
longer in direct proportion.
Python dictionaries use a data structure called ahashtablethat has a remarkable property:
theinoperator takes about the same amount of time no matter how many items are in the
dictionary. I explain how that’s possible in Section B.4, but the explanation might not make
sense until you’ve read a few more chapters.
11.2 Dictionary as a collection of counters
Suppose you are given a string and you want to count how many times each letter appears.
There are several ways you could do it:
```

## Trang PDF 130 — chương 11

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf

```text
108 Chapter 11. Dictionaries
’a’ 1
1
dict
hist
’p’
1
’o’ 1
’r’ 2
’t’
0
1
’a’
’p’
list
2 ’t’
’o’3
1
dict
inv
2 0
list
’r’
Figure 11.1: State diagram.
Each time through the loop,keygets a key fromdandvalgets the corresponding value.
Ifvalis not ininverse, that means we haven’t seen it before, so we create a new item and
initialize it with asingleton(a list that contains a single element). Otherwise we have seen
this value before, so we append the corresponding key to the list.
Here is an example:
>>> hist = histogram('parrot')
>>> hist
{'a': 1,'p': 1,'r': 2,'t': 1,'o': 1}
>>> inverse = invert_dict(hist)
>>> inverse
{1: ['a','p','t','o'], 2: ['r']}
Figure 11.1 is a state diagram showinghistandinverse. A dictionary is represented as a
box with the typedictabove it and the key-value pairs inside. If the values are integers,
floats or strings, I draw them inside the box, but I usually draw lists outside the box, just
to keep the diagram simple.
Lists can be values in a dictionary, as this example shows, but they cannot be keys. Here’s
what happens if you try:
>>> t = [1, 2, 3]
>>> d = dict()
>>> d[t] ='oops'
Traceback (most recent call last):
File "<stdin>", line 1, in ?
TypeError: list objects are unhashable
I mentioned earlier that a dictionary is implemented using a hashtable and that means that
the keys have to behashable.
Ahashis a function that takes a value (of any kind) and returns an integer. Dictionaries
use these integers, called hash values, to store and look up key-value pairs.
This system works fine if the keys are immutable. But if the keys are mutable, like lists,
bad things happen. For example, when you create a key-value pair, Python hashes the key
and stores it in the corresponding location. If you modify the key and then hash it again, it
would go to a different location. In that case you might have two entries for the same key,
or you might not be able to find a key. Either way, the dictionary wouldn’t work correctly.
That’s why keys have to be hashable, and why mutable types like lists aren’t. The simplest
way to get around this limitation is to use tuples, which we will see in the next chapter.
```

## Trang PDF 137 — chương 12

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf

```text
Chapter 12
T uples
This chapter presents one more built-in type, the tuple, and then shows how lists, dictionar-
ies, and tuples work together. I also present a useful feature for variable-length argument
lists, the gather and scatter operators.
One note: there is no consensus on how to pronounce “tuple”. Some people say “tuh-
ple”, which rhymes with “supple”. But in the context of programming, most people say
“too-ple”, which rhymes with “quadruple”.
12.1 T uples are immutable
A tuple is a sequence of values. The values can be any type, and they are indexed by
integers, so in that respect tuples are a lot like lists. The important difference is that tuples
are immutable.
Syntactically, a tuple is a comma-separated list of values:
>>> t ='a','b','c','d','e'
Although it is not necessary, it is common to enclose tuples in parentheses:
>>> t = ('a','b','c','d','e')
To create a tuple with a single element, you have to include a final comma:
>>> t1 ='a',
>>> type(t1)
<class'tuple'>
A value in parentheses is not a tuple:
>>> t2 = ('a')
>>> type(t2)
<class'str'>
Another way to create a tuple is the built-in functiontuple. With no argument, it creates
an empty tuple:
>>> t = tuple()
>>> t
()
```

## Trang PDF 140 — chương 12

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf

```text
118 Chapter 12. T uples
12.4 Variable-length argument tuples
Functions can take a variable number of arguments. A parameter name that begins with
*gathersarguments into a tuple. For example,printalltakes any number of arguments
and prints them:
def printall(*args):
print(args)
The gather parameter can have any name you like, butargsis conventional. Here’s how
the function works:
>>> printall(1, 2.0,'3')
(1, 2.0,'3')
The complement of gather isscatter. If you have a sequence of values and you want to pass
it to a function as multiple arguments, you can use the*operator. For example,divmod
takes exactly two arguments; it doesn’t work with a tuple:
>>> t = (7, 3)
>>> divmod(t)
TypeError: divmod expected 2 arguments, got 1
But if you scatter the tuple, it works:
>>> divmod(*t)
(2, 1)
Many of the built-in functions use variable-length argument tuples. For example,maxand
mincan take any number of arguments:
>>> max(1, 2, 3)
3
Butsumdoes not.
>>> sum(1, 2, 3)
TypeError: sum expected at most 2 arguments, got 3
As an exercise, write a function calledsum_allthat takes any number of arguments and
returns their sum.
12.5 Lists and tuples
zipis a built-in function that takes two or more sequences and interleaves them. The name
of the function refers to a zipper, which interleaves two rows of teeth.
This example zips a string and a list:
>>> s ='abc'
>>> t = [0, 1, 2]
>>> zip(s, t)
<zip object at 0x7f7d0a9e7c48>
The result is azip objectthat knows how to iterate through the pairs. The most common
use ofzipis in aforloop:
```

## Trang PDF 141 — chương 12

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf

```text
12.5. Lists and tuples 119
>>> for pair in zip(s, t):
... print(pair)
...
('a', 0)
('b', 1)
('c', 2)
A zip object is a kind ofiterator, which is any object that iterates through a sequence.
Iterators are similar to lists in some ways, but unlike lists, you can’t use an index to select
an element from an iterator.
If you want to use list operators and methods, you can use a zip object to make a list:
>>> list(zip(s, t))
[('a', 0), ('b', 1), ('c', 2)]
The result is a list of tuples; in this example, each tuple contains a character from the string
and the corresponding element from the list.
If the sequences are not the same length, the result has the length of the shorter one.
>>> list(zip('Anne','Elk'))
[('A','E'), ('n','l'), ('n','k')]
You can use tuple assignment in aforloop to traverse a list of tuples:
t = [('a', 0), ('b', 1), ('c', 2)]
for letter, number in t:
print(number, letter)
Each time through the loop, Python selects the next tuple in the list and assigns the ele-
ments toletterandnumber. The output of this loop is:
0 a
1 b
2 c
If you combinezip,forand tuple assignment, you get a useful idiom for traversing two
(or more) sequences at the same time. For example,has_matchtakes two sequences,t1
andt2, and returnsTrueif there is an indexisuch thatt1[i] == t2[i]:
def has_match(t1, t2):
for x, y in zip(t1, t2):
if x == y:
return True
return False
If you need to traverse the elements of a sequence and their indices, you can use the built-in
functionenumerate:
for index, element in enumerate('abc'):
print(index, element)
The result fromenumerateis an enumerate object, which iterates a sequence of pairs; each
pair contains an index (starting from 0) and an element from the given sequence. In this
example, the output is
0 a
1 b
2 c
Again.
```

## Trang PDF 143 — chương 12

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf

```text
12.7. Sequences of sequences 121
0
1
’Cleese’
’John’
tuple
Figure 12.1: State diagram.
(’Cleese’, ’John’) ’08700 100 222’
’08700 100 222’
’08700 100 222’
’08700 100 222’
’08700 100 222’
(’Chapman’, ’Graham’)
(’Idle’, ’Eric’)
(’Jones’, ’Terry’)
(’Gilliam’, ’Terry’)
(’Palin’, ’Michael’) ’08700 100 222’
dict
Figure 12.2: State diagram.
12.7 Sequences of sequences
I have focused on lists of tuples, but almost all of the examples in this chapter also work
with lists of lists, tuples of tuples, and tuples of lists. To avoid enumerating the possible
combinations, it is sometimes easier to talk about sequences of sequences.
In many contexts, the different kinds of sequences (strings, lists and tuples) can be used
interchangeably. So how should you choose one over the others?
To start with the obvious, strings are more limited than other sequences because the ele-
ments have to be characters. They are also immutable. If you need the ability to change the
characters in a string (as opposed to creating a new string), you might want to use a list of
characters instead.
Lists are more common than tuples, mostly because they are mutable. But there are a few
cases where you might prefer tuples:
1. In some contexts, like areturnstatement, it is syntactically simpler to create a tuple
than a list.
2. If you want to use a sequence as a dictionary key, you have to use an immutable type
like a tuple or string.
3. If you are passing a sequence as an argument to a function, using tuples reduces the
potential for unexpected behavior due to aliasing.
Because tuples are immutable, they don’t provide methods likesortandreverse, which
modify existing lists. But Python provides the built-in functionsorted, which takes any
sequence and returns a new list with the same elements in sorted order, andreversed,
which takes a sequence and returns an iterator that traverses the list in reverse order.
```

## Trang PDF 144 — chương 12

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf

```text
122 Chapter 12. T uples
12.8 Debugging
Lists, dictionaries and tuples are examples ofdata structures; in this chapter we are starting
to see compound data structures, like lists of tuples, or dictionaries that contain tuples as
keys and lists as values. Compound data structures are useful, but they are prone to what
I callshape errors; that is, errors caused when a data structure has the wrong type, size, or
structure. For example, if you are expecting a list with one integer and I give you a plain
old integer (not in a list), it won’t work.
To help debug these kinds of errors, I have written a module calledstructshapethat
provides a function, also calledstructshape, that takes any kind of data structure as
an argument and returns a string that summarizes its shape. You can download it from
https://thinkpython.com/code/structshape.py
Here’s the result for a simple list:
>>> from structshape import structshape
>>> t = [1, 2, 3]
>>> structshape(t)
'list of 3 int'
A fancier program might write “list of 3 ints”, but it was easier not to deal with plurals.
Here’s a list of lists:
>>> t2 = [[1,2], [3,4], [5,6]]
>>> structshape(t2)
'list of 3 list of 2 int'
If the elements of the list are not the same type,structshapegroups them, in order, by
type:
>>> t3 = [1, 2, 3, 4.0,'5','6', [7], [8], 9]
>>> structshape(t3)
'list of (3 int, float, 2 str, 2 list of int, int)'
Here’s a list of tuples:
>>> s ='abc'
>>> lt = list(zip(t, s))
>>> structshape(lt)
'list of 3 tuple of (int, str)'
And here’s a dictionary with 3 items that map integers to strings.
>>> d = dict(lt)
>>> structshape(d)
'dict of 3 int->str'
If you are having trouble keeping track of your data structures,structshapecan help.
12.9 Glossary
tuple:An immutable sequence of elements.
tuple assignment:An assignment with a sequence on the right side and a tuple of vari-
ables on the left. The right side is evaluated and then its elements are assigned to the
variables on the left.
```

