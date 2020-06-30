from RobotRaconteur.Client import *
import time
import numpy

def joystick(data):
    print("Joystick event!!!!")
    

def setf_pixels_test(sense_hat):
    colorRGB=RRN.GetNamedArrayDType("com.robotraconteur.color.ColorRGBAu",sense_hat)
    vector2=numpy.zeros((64,),dtype=colorRGB)
    for i in range(64):
        vals=i*4-1
        if(vals<0):
            vals=0
        
        vector2[i]['r']=vals
        vector2[i]['g']=vals
        vector2[i]['b']=vals
        vector2[i]['a']=0
    
    #c.setf_pixel(1,1,vector2)
    sense_hat.setf_pixels(vector2)

def clear_test(sense_hat):
    colorRGB=RRN.GetNamedArrayDType("com.robotraconteur.color.ColorRGBAu",sense_hat)
    vector2=numpy.zeros((1,),dtype=colorRGB)
    vector2[0]['r']=0
    vector2[0]['g']=0
    vector2[0]['b']=0
    vector2[0]['a']=0
    sense_hat.Clear(vector2)
    
def setf_pixel_test(sense_hat):
    colorRGB=RRN.GetNamedArrayDType("com.robotraconteur.color.ColorRGBAu",sense_hat)
    vector2=numpy.zeros((1,),dtype=colorRGB)
    vector2[0]['r']=180
    vector2[0]['g']=180
    vector2[0]['b']=180
    vector2[0]['a']=0
    sense_hat.setf_pixel(4,4,vector2)
    
def set_rotation_test(sense_hat):
    sense_hat.setf_rotation(90)

def flip_v_test(sense_hat):
    sense_hat.Flip_v()

def flip_h_test(sense_hat):
    sense_hat.Flip_h()
    
def show_letter_test(sense_hat):
    colorRGB=RRN.GetNamedArrayDType("com.robotraconteur.color.ColorRGBAu",sense_hat)
    vector2=numpy.zeros((1,),dtype=colorRGB)
    vector2[0]['r']=255
    vector2[0]['g']=70
    vector2[0]['b']=255
    vector2[0]['a']=0
    
    vector3=numpy.zeros((1,),dtype=colorRGB)
    vector3[0]['r']=90
    vector3[0]['g']=90
    vector3[0]['b']=0
    vector3[0]['a']=0
    sense_hat.Show_letter("s",vector2,vector3)
    
def show_message_test(sense_hat):
    colorRGB=RRN.GetNamedArrayDType("com.robotraconteur.color.ColorRGBAu",sense_hat)
    vector2=numpy.zeros((1,),dtype=colorRGB)
    vector2[0]['r']=255
    vector2[0]['g']=255
    vector2[0]['b']=255
    vector2[0]['a']=0
    
    vector3=numpy.zeros((1,),dtype=colorRGB)
    vector3[0]['r']=180
    vector3[0]['g']=180
    vector3[0]['b']=180
    vector3[0]['a']=0
    sense_hat.Show_message("Hello!",vector2,vector3,0.5)

def pressure_wire_changed(w,value,time):
    val=w.InValue
    print("Pressure=="+val+"/n")

def temperature_wire_changed(w,value,time):
    val=w.InValue
    print("Temperature=="+val+"/n")
    
def humidity_wire_changed(w,value,time):
    val=w.InValue
    print("Humidity==   "+val+"/n")
    
def imu_wire_changed(w,value,time):
    val=w.InValue
    print("Accelerometer updated/n")
    print("Angular Velocity== "+val.angular_velocity+"/n")


def main():

    url='rr+tcp://localhost:2354?service=SensorHat'
    imu_url='rr+tcp://localhost:2354?service=SensorHatIMU'
    c=RRN.ConnectService(url)
    imu=RRN.ConnectService(imu_url)
    c.joystick_move+=joystick
    temp_wire=c.Temperature.Connect()
    temp_wire.WireValueChanged+=temperature_wire_changed
    pressure_wire=c.Pressure.Connect()
    pressure_wire.WireValueChanged+=pressure_wire_changed
    hum_wire=c.Humidity.Connect()
    hum_wire.WireValueChanged+=humidity_wire_changed
    imu_wire=imu.imu_state.Connect()
    
    c.Start_streaming()
    
    setf_pixels_test(c)
    time.sleep(1)
    
    clear_test(c)
    time.sleep(1)
    setf_pixel_test(c)
    time.sleep(1)
    print("show letters")
    show_letter_test(c)
    time.sleep(3)
    flip_h_test(c)
    time.sleep(1)
    flip_v_test(c)
    time.sleep(1)
    set_rotation_test(c)
    time.sleep(1)
    show_message_test(c)
    
    
    #c.setf_pixel(1,1,vector2)
    
    s=input("press enter to exit")


    

if __name__== '__main__':
    main()
