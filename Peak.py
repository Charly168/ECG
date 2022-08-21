# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 12:29:59 2022

@author: HP
"""

"""
定义一个class，采用迭代和自适应阈值的方法来寻找Peak
这个找peak的方法虽然简单，但是却有一个最大的缺点，对于心率不稳的情况没法正确识别Peak
不过在我们的专业实验课中，不会有这种情况，比较理想。但是实际klinisch里面不会是稳定的心率
另外有个小缺点，实验人员需要肉眼观测心率，设定合理的timeSipmle
"""
class Peak(object):
    
    def __init__(self,thresholdFaktor = 0.7,deadZone = 4,timeSimple = 200):
        # 最大心率为250bmp，对应频率为4hz，大概是0.2s，采样频率为1000，因此相应采样点数为200
        self.num = 0 # 用于储存循环次数，每循环一次代表数组不同的片段
        self.lstPeak = [] # 记录的是Peak对应在数组中的index
        self.thresholdFaktor = thresholdFaktor
        self.Maximun = 0
        self.threashold = thresholdFaktor * self.Maximun 
        self.deadZone = deadZone
        self.timeSimple = timeSimple
        
    def findPeak(self,lstg):
        
        for i in self.__iter__(lstg,self.timeSimple):
            
            idN = i.index(max(i))+self.num*self.timeSimple  # 计算后一个最大值对应的index
            
            """
            此处用三个判断
            1. 用于初始化num=0，即第一个i时，计算最大值，并储存其index
            2. num大于0且前后两个最大值对应的index间距大于timeSimple时，存储其值
            3. 如果2. 为否， 则进入下一个for循环，num自动加1
            值得注意的是，idN只存储真正的最大值，idV存储上一个最大值
            """
            if max(i) > self.threashold:
                if self.num == 0:
                    self.Maximun = max(i)
                    self.threshold = self.Maximun * self.thresholdFaktor
                    self.lstPeak.append(i.index(max(i)))
                    idV = i.index(max(i)) # 计算前一个最大值对应的index
                    self.num += 1
                    
                                   
                elif (self.num > 0 
                      and self.cheakDisdance(idV,idN) 
                      and abs(lstg[idV]-lstg[idN])<0.5*lstg[idV]):
                    self.Maximun = max(i)
                    self.threshold = self.Maximun * self.thresholdFaktor
                    self.lstPeak.append(idN)
                    idV = idN # 存储当前最大值的index
                    self.num += 1
            
                else:
                    self.num += 1
                                   
                    
        return self.lstPeak
                
    def cheakDisdance(self,maxVor,maxNach):
        
        if maxNach - maxVor > self.timeSimple:
            return True
        
    def __iter__(self,lst,size):
        """
        用于返回一个生成器，将列表切片
        """
        for i in range(0,len(lst),size):    
            yield lst[i:i+size]
            
   