HackRFWebtools(to be continued)
==============
a Web Framework for HackRF. <br>

##  Introduction 
The project is based on [webradio's front-end](https://github.com/mikestir/webradio "webradio") and complete [wf4hf's](https://github.com/aguardar/wf4hf "wf4hf") unfinished work.
It can be used to control  HackRF from a browser.<br>
The application is built on [py-hackrf-ctypes](https://github.com/wzyy2/py-hackrf-ctypes "py-hackrf-ctypes")
 rather than GNU Radio  , which make  it possible for software  to use less space, so that I can run it  in a embedded platform(such as  Raspberry Pi) .<br>

## Features 
* You can find in the picture

##  Dependencies 
Install python,django

        sudo apt-get install python-pip python-dev
        sudo pip install Django==1.6.6

Install libhackrf

        git clone --progress http://github.com/mossmann/hackrf.git
        cd hackrf/host
        mkdir build
        cd build
        cmake ../ -DINSTALL_UDEV_RULES=ON
        make
        sudo make install
        sudo ldconfig

    
##  Usage 
        python manage.py runserver 0.0.0.0:9999
    
##  我是中文 
poor English......<br>
这就是一个HackRF的基于浏览器的信号解调前端, 让使用者在远程通过浏览器就可以直接对常见的信号进行观察,并能完成简单的WBFM NBFM AM解调的功能.出于在Raspberry Pi等嵌入式计算机上运行的目的,尽可能少的使用外部依赖库,所以代码直接通过PYUSB完成和HackRF的联系,并不依赖GNU RADIO.这样用户就可以方便地部署天线架设更容易的场合.然后拿出手机观察拉.


![image](http://www.iotwrt.com/jpg/hackrf-webtools.png)

