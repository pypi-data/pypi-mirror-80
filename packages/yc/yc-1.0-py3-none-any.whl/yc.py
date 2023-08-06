# coding=utf-8

class yc():
    def fun(self):
        print('\n'.join([' '.join(['%s*%s=%s '%(j,i,j*i) if j==1 else '%s*%s=%-2s '%(j,i,j*i)  for j in range(1,i+1)])for i in range(1,10)]))

print('###########################################################################')
print('#                                                                         #')
print('#                                 hi, 瓜三娃.                              #')
print('#                                                                         #')
print('###########################################################################')