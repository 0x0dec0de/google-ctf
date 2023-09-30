from PIL import Image   
new_image = Image.open("./symatrix.png")
nx_len, y_len = new_image.size
x_len = (nx_len) // 2
new_matrix = new_image.load()
next_position = 0
nx_len -= 1
binstr = []
for i in range(0, y_len):
    for j in range(0, x_len):
        pixel = new_matrix[j, i]
        if new_matrix[nx_len - j, i] != pixel:
            binstr.append(new_matrix[nx_len - j, i][2]-pixel[2])
binstr = ''.join(map(str,binstr))
for i in range(0,len(binstr),8):
    print(chr(int(binstr[i:i+8],2)),end="")