# coding=utf-8
class computerfactory:
    __obj = None
    __init_flag = True

    def __new__(cls, *args, **kwargs):
        if cls.__obj == None:
            cls.__obj = object.__new__(cls)

        return cls.__obj

    def __init__(self):
        if computerfactory.__init_flag:
            print("init....")
            computerfactory.__init_flag = False  # 以上单例模式实现，只能有一个电脑工厂对象

    def creatcomputer(self,brand):  # 以下工厂模式
        if brand=='联想':
            print('产品联想电脑生产')
            return Lenove()
        if brand=='华硕':
            print('产品华硕电脑生产')
            return Asus()
        if brand=='神舟':
            print('产品神舟电脑生产')
            return Shenzhou()
        else:
           return '产品无法生产'

class computer:
    def caculate(self):
        print('请输入一个超级计算数值')
class Lenove(computer):
    def caculate(self):
        print('这是联想电脑的计算')
class Asus(computer):
    def caculate(self):
        print('这是华硕电脑的计算')
class Shenzhou(computer):
    def caculate(self):
        print('这是神舟电脑的计算')

f=computerfactory()
c1=f.creatcomputer('联想')
c2=f.creatcomputer('华硕')
c3=f.creatcomputer('神舟')
c4=f.creatcomputer('华为')
print(c1)
print(c2)
print(c3)
print(c4)
print('############################')
f2=computerfactory()
print(f)
print(f2)  # 新实例对象地址也是f，说明只能生成一个单例对象，节约内存
c1=f2.creatcomputer('联想')
c2=f2.creatcomputer('华硕')
c3=f2.creatcomputer('神舟')
c4=f2.creatcomputer('华为')
print(c1)
print(c2)
print(c3)
print(c4)