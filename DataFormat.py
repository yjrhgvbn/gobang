import os

import visdom
import torch
import numpy as np

class DataFormat:

    def __init__(self):
        self.cpuUsingRate = []
        self.cpuUsingRate = []
        self.gfxLossRate = []
        self.cpufilesname = []
        self.memfilesname = []
        self.gfxfilesname = []
        self.cpudirname = '/Users/haozeming/Desktop/AndroidRunningData/cpuinfo'
        self.memdirname = '/Users/haozeming/Desktop/AndroidRunningData/meminfo'
        self.gfxdirname = '/Users/haozeming/Desktop/AndroidRunningData/gfxinfo'


    #序列化文件顺序
    def formatFileName(self, dirname):

        date = []
        newfilename = []

        for filename in os.listdir(dirname):
            if filename!='.DS_Store':
                ymd=(filename.split(' '))[0]
                date_temp=(((filename.split(' '))[1]).rsplit('.',1))[0]
                date_temp=date_temp.split('.')
                date.append(date_temp)
        date.sort(key=lambda x: (int(x[0]), int(x[1]), int(x[2])))
        for new in date:
            temp_new=ymd+' '+new[0]+'.'+new[1]+'.'+new[2]+'.txt'
            #cpuUsingRate_x.append(new[0]+':'+new[1]+':'+new[2])
            newfilename.append(temp_new)
        return newfilename


    #判断时间先后顺序
    def isPioneer(self, string_1, string_2):
        if string_1 == 'default' or string_2 == 'default':
            return int(2)
        string_1 = (((string_1.split(' '))[1]).rsplit('.',1))[0]
        string_2 = (((string_2.split(' '))[1]).rsplit('.',1))[0]
        h_string_1 = int(string_1.split('.')[0])
        m_string_1 = int(string_1.split('.')[1])
        h_string_2 = int(string_2.split('.')[0])
        m_string_2 = int(string_2.split('.')[1])
        if h_string_1 == h_string_2 and m_string_1 == m_string_2:
            return int(2)
        else:
            if h_string_1 < h_string_2:
                return int(1)
            elif h_string_1 == h_string_2:
                if m_string_1 < m_string_2:
                    return int(1)
                else:
                    return int(0)
            else:
                return int(0)


    #自动补齐缺省文件
    def repairDefaultData(self):
        self.cpufilesname = self.formatFileName("/Users/haozeming/Desktop/AndroidRunningData/cpuinfo")
        self.memfilesname = self.formatFileName("/Users/haozeming/Desktop/AndroidRunningData/meminfo")
        self.gfxfilesname = self.formatFileName("/Users/haozeming/Desktop/AndroidRunningData/gfxinfo")
        c = 0
        m = 0
        g = 0
        while m<len(self.memfilesname):
            if self.isPioneer(self.cpufilesname[c], self.memfilesname[m]) != 2 or self.isPioneer(self.memfilesname[m], self.gfxfilesname[g]) != 2:
                if self.isPioneer(self.cpufilesname[c], self.memfilesname[m]) == 0:
                    self.cpufilesname.insert(c, 'default')
                elif self.isPioneer(self.cpufilesname[c], self.memfilesname[m]) == 1:
                    self.memfilesname.insert(m, 'default')
                if self.isPioneer(self.memfilesname[m], self.gfxfilesname[g]) == 1:
                    self.gfxfilesname.insert(g, 'default')
                elif self.isPioneer(self.memfilesname[m], self.gfxfilesname[g]) == 0:
                    self.memfilesname.insert(m, 'default')
            c = c + 1
            m = m + 1
            g = g + 1


    #提取CPU数据
    def formatCPUData(self):

        for filename in self.cpufilesname:
            try:
                file=open(self.cpudirname +"/"+ filename, "r", encoding="UTF-8")
                lines = file.readlines()
                cpuUsingRateItem = ((lines[-1].split(' '))[0]).rstrip('%')
                self.cpuUsingRate.append(float(cpuUsingRateItem)/100)
            except UnicodeDecodeError:
                continue
            except FileNotFoundError:
                self.cpuUsingRate.append(float(1))
                continue

        file.close()
        return self.cpuUsingRate

    #提取内存数据
    def formatMemData(self):

        memTotal=[]
        memFree=[]
        memAvailable=[]

        for filename in self.memfilesname:
            try:
                file=open(self.memdirname +"/"+ filename, "r", encoding="UTF-8")
                lines = file.readlines()
                memFreeItem=lines[1].split(' ')
                memAvailableItem=lines[2].split(' ')
                while '' in memFreeItem:
                    memFreeItem.remove('')
                while '' in memAvailableItem:
                    memAvailableItem.remove('')
                memTotal.append(3832304)
                memFree.append(memFreeItem[1])
                memAvailable.append(memAvailableItem[1])
            except UnicodeDecodeError:
                continue
            except FileNotFoundError:
                memTotal.append(3832304)
                memFree.append(0)
                memAvailable.append(0)
                continue


        file.close()

        memTotal = torch.tensor(list(map(float, memTotal)))
        #memFree = torch.tensor(list(map(float, memFree)))
        memAvailable = torch.tensor(list(map(float, memAvailable)))

        self.memUsingRate = ((memTotal-memAvailable)/memTotal).tolist()

        return self.memUsingRate

    #提取GPU数据
    def formatGFSData(self):

        for filename in self.gfxfilesname:
            try:
                file = open(self.gfxdirname + "/" + filename, "r", encoding="UTF-8")
                lines = file.readlines()
                gfxInfoItem = lines[7]
                if(gfxInfoItem.__eq__('\n')):
                    lossFPSRateItem=float(1)
                else:
                    lossFPSRateItem=float(gfxInfoItem.split(' ')[3].rstrip('\n').lstrip('(').rstrip(')').rstrip('%'))/100
                    if np.isnan(lossFPSRateItem):lossFPSRateItem=float(1)
            except UnicodeDecodeError:
                continue
            except IndexError:
                lossFPSRateItem = float(1)
                continue
            except FileNotFoundError:
                lossFPSRateItem = float(1)
                continue
            finally:
                self.gfxLossRate.append(lossFPSRateItem)

        file.close()
        return self.gfxLossRate


    #归一化处理
    def normalizationData(self):

        cpumean = np.mean(self.cpuUsingRate)
        memmean = np.mean(self.memUsingRate)
        gfxmean = np.mean(self.gfxLossRate)
        i=0
        while i<len(self.cpuUsingRate):
            if self.cpuUsingRate[i] == 1.00:
                self.cpuUsingRate[i] = cpumean
            if self.memUsingRate[i] == 1.00:
                self.memUsingRate[i] = memmean
            if self.gfxLossRate[i] == 1.00:
                self.gfxLossRate[i] = gfxmean
            i=i+1




if __name__=="__main__":
    df=DataFormat()
    df.repairDefaultData()
    #画图
    cpuUsingRate = df.formatCPUData()
    memUsingRate = df.formatMemData()
    gfxLossRate = df.formatGFSData()

    df.normalizationData()

    vis = visdom.Visdom(env='main')
    #print(len(cpuUsingRate), len(memUsingRate), len(gfxLossRate))
    
    vis.line(X=np.array(range(0,328,1)),
             Y=np.column_stack((np.array(cpuUsingRate), np.array(memUsingRate), np.array(gfxLossRate))),
             win='TimeSeries',
             opts={'title': 'TimeSeriesRunningData'})
    

