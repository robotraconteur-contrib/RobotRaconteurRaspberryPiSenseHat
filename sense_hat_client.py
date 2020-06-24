from RobotRaconteur.Client import *
import time
import numpy

def joystick(data):
    print("hello")

def main():

    url='rr+tcp://localhost:2354?service=SensorHat'
    c=RRN.ConnectService(url)
    c.joystick_move+=joystick
    wire=c.Temperature.Connect()
    wire.WireValueChanged+=wire_changed
    
    c.Start_streaming()
    colorRGB=RRN.GetNamedArrayDType("com.robotraconteur.color.ColorRGBAu",c)
    vector2=numpy.zeros((1,),dtype=colorRGB)
    vector2[0]['r']=255
    vector2[0]['g']=102
    vector2[0]['b']=255
    vector2[0]['a']=0
    #c.setf_pixel(1,1,vector2)
    c.Clear(vector2)
    time.sleep(1)

def wire_changed(w,value,time):
    val=w.InValue
    print(val)

if __name__== '__main__':
    main()
