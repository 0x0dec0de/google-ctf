import re
with open('encoder.c') as file:
    data = file.read()

pattern = re.compile(r"/\*([\s\S]*?)\*/\s*", re.MULTILINE)
code = {}
order = lambda com: int(com.split('\n')[0].split(":")[1])

for comment in pattern.findall(data):
    if 'encoder.py' in comment:
        comment_order = order(comment)
        if comment_order in code:
            assert code[comment_order]==comment, "same comment number different value"
        code[order(comment)] = comment
code = [code[index] for index in sorted(code.keys())]
print(''.join(code))
