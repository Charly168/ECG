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
        # 最大心率为250bmp，对应频率为4hz，大概是0.2s实验室的采样频率为2000，因此相应采样点数为200
        self.num = 0 # 用于储存循环次数，每循环一次代表数组不同的片段
        self.lstPeak = [] # 记录的是Peak对应在数组中的index
        self.thresholdFaktor = thresholdFaktor
        self.Maximun = 0
        self.threashold = thresholdFaktor * self.Maximun 
        # self.deadZone = deadZone
        self.timeSimple = timeSimple
        self.MaxDistance = 2800
        self.minFre = 500 # 正常的心率变化范围为30~250 bmp,也就是0.5~4 Hz, 两个最小RR间距为1/4*2000
        self.RQS = 200 # 一般情况下QRS的间距为0.1s，也就是200个采样点
        
    def findPeak(self,lstg):
        
        for i in self.__iter__(lstg,self.timeSimple):
            
            idN = i.index(max(i))+self.num*self.timeSimple  # 计算后一个最大值(当前最大值)对应的index
            
            """
            此处用三个判断
            1. 用于初始化num=0，即第一个i时，计算最大值，并储存其index
            2. num大于0且前后两个最大值对应的index间距大于timeSimple且前后最大值差的占比
            为前者的50%时，存储其值
                这里考虑了还另一种，切片问题会导致可能恰好在QRS左右进行了切片，这样的切片
                会导致相邻出现两个最大值；如果出现这种情况，则删除前者，保留后者
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
                    
                                   
                elif self.num > 0:
                    if self.cheakQRSDisdance(idV,idN):
                        self.Maximun = max(i)
                        self.threshold = self.Maximun * self.thresholdFaktor
                        self.lstPeak.pop()
                        self.lstPeak.append(idN)
                        idV = idN
                        self.num += 1
                    
                    elif (self.cheakDisdance(idV,idN) 
                          and self.cheakMaxDisdance(idV, idN)
                          and abs(lstg[idV]-lstg[idN]) < 0.5*lstg[idV]):   
                        self.Maximun = max(i)
                        self.threshold = self.Maximun * self.thresholdFaktor
                        self.lstPeak.append(idN)
                        idV = idN # 存储当前最大值的index
                        self.num += 1
                    
                        
                    else :
                        """
                        此处这个判断方法，修正了以下两点错误
                        1. 当前片段内出现两个真峰值（后者大于前者），由于max（）只能取一个，
                        导致小的那个被删除，然后导致idV跟idN的间距大于self.MaxDistance = 2800
                        
                        2. 上一个片段出现两个最大值（前者大于后者），理由同上
                        
                        为了判断究竟是是上面哪种情况，我这里在当前片段内采用
                        max(i[0:int(len(i)/2)])/max(i)<0.5 来判断
                        也就是说，如果是假峰的话，该值将会小于0.5
                        
                        虽然这种方法已经极大程度地避免了错误情况，但根据实验结果来看依旧有
                        错误的Peak被标记，然而这个Peak它既不是真峰也不是假峰
                        
                        我尝试过从主函数中删除这些异常的点，比如删除ecg所有implitude小于0.5值
                        但是结果更加混乱。而且就但从这个有缺陷的结果来看，这些异常点也绝不是
                        我此前考虑的任何一种，不知道是什么原因导致的，也就没法将其归类
                        暂且归于系统错误吧
                        """
                        
                        if i.index(max(i)) / self.timeSimple > 0.5 and max(i[0:int(len(i)/2)])/max(i)<0.5:
                            a = lstg[(self.num-1)*self.timeSimple:self.num*self.timeSimple]
                            
                            for i in self.__iter__(a,int(0.5*self.timeSimple)):
                                idNN = i.index(max(i))
                                self.Maximun = max(i)
                                self.threshold = self.Maximun * self.thresholdFaktor

                            idNN = int(idNN + 0.5*self.timeSimple + (self.num-1)*self.timeSimple)
                            self.lstPeak.append(idNN)
                            self.lstPeak.append(idN)
                            idV = idN
                            self.num += 1
                            
                            
                            
                        else:
                            
                            a = lstg[(self.num)*self.timeSimple:(self.num+1)*self.timeSimple]
                            
                            for i in self.__iter__(a,int(0.5*self.timeSimple)):
                                idVV = i.index(max(i))
                                self.Maximun = max(i)
                                self.threshold = self.Maximun * self.thresholdFaktor
                                # self.lstPeak.append(idN)
                                # idV = idN # 存储当前最大值的index
                                # self.num += 1
                                idVV = (idVV + self.num*self.timeSimple)
                                self.lstPeak.append(idVV)
                            idV = idVV
                            self.num += 1

            
                else:
                    self.num += 1
                                   
                    
        return self.lstPeak
                
    def cheakDisdance(self,maxVor,maxNach):
        """
        计算前后两个最大值之间的距离
        """
        if maxNach - maxVor > self.minFre:
            return True
        
    def cheakMaxDisdance(self,maxVor,maxNach):
        """
        计算前后两个最大值之间的距离
        """
        if maxNach - maxVor < self.MaxDistance:
            return True
    
    def cheakQRSDisdance(self,maxVor,maxNach):
        """
        排除RQS的情况
        """
        if abs(maxNach - maxVor) < self.RQS:
            return True
        
    def __iter__(self,lst,size):
        """
        返回一个生成器，将列表切片
        细心的人可以发现，我这里采用的是固定的切片，也就导致了实验人员只能肉眼观察，
        大概的频率范围，再设定合理的timesimple
        """
        for i in range(0,len(lst),size):    
            yield lst[i:i+size]
            
            
            
def iter(lst,size):
    """
    返回一个生成器，将列表切片
    细心的人可以发现，我这里采用的是固定的切片，也就导致了实验人员只能肉眼观察，
    大概的频率范围，再设定合理的timesimple
    """
    for i in range(0,len(lst),size):    
        yield lst[i:i+size]

lst = [1,2,3,4,5,6,7,8,9]
size = 3
for i in iter(lst,size):

    print(i)
    

               
            
            
            
            
            
            
   