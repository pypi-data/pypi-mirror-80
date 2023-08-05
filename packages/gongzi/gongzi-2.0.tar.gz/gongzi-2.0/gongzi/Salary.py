#coding=utf-8
'''
          用于计算公司员工工资
'''

company='海龙集团'

def Yearsalary(Monthsalary):
    '''
    用于计算公司员工年薪，计算方法为：Mothsalary*12
    '''
    return Monthsalary*12
def Daysalary(Monthsalary):
    '''
    用于计算公司员工日薪，计算方法为：Mothsalary/22.5，其中22.5天为国家规定一个月工作时间
    '''
    return Monthsalary/22.5


#测试模块时

if __name__=='__main__':
    print(Yearsalary(5000))