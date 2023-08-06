def binary_conv(inarg):
    def conv_str(arg1):
        return ''.join(format(i, 'b') for i in bytearray(arg1, encoding ='utf-8')) 
    def conv_int(arg1):
        return bin(arg1).replace("0b", "")
    
    if isinstance(inarg,str):
        return conv_str(inarg)
    if isinstance(inarg,list) or isinstance(inarg,tuple):
        new_list = []
        for num in inarg:
            if isinstance(num,int):
                new_list.append(conv_int(num))
            elif isinstance(num,str):
                new_list.append(conv_str(num))
        return new_list
