from RobotRaconteur.Client import *
import time
import numpy

def joystick(data):
    print("Joystick event!!!!"+data)
    

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
    vector2[i]['r']=0
    vector2[i]['g']=0
    vector2[i]['b']=0
    vector2[i]['a']=0
    sense_hat.clear(vector2)
    
def setf_pixel_test(sense_hat):
    colorRGB=RRN.GetNamedArrayDType("com.robotraconteur.color.ColorRGBAu",sense_hat)
    vector2=numpy.zeros((1,),dtype=colorRGB)
    vector2[i]['r']=180
    vector2[i]['g']=180
    vector2[i]['b']=180
    vector2[i]['a']=0
    sense_hat.setf_pixel(4,4,vector2)
    
def set_rotation_test(sense_hat):
    sense_hat.setf_rotation(40)

def flip_v_test(sense_hat):
    sense_hat.Flip_v()

def flip_h_test(sense_hat):
    sense_hat.Flip_h()
    
def show_letter_test(sense_hat):
    colorRGB=RRN.GetNamedArrayDType("com.robotraconteur.color.ColorRGBAu",sense_hat)
    vector2=numpy.zeros((1,),dtype=colorRGB)
    vector2[i]['r']=255
    vector2[i]['g']=255
    vector2[i]['b']=255
    vector2[i]['a']=0
    
    vector3=numpy.zeros((1,),dtype=colorRGB)
    vector3[i]['r']=180
    vector3[i]['g']=180
    vector3[i]['b']=180
    vector3[i]['a']=0
    sense_hat.Show_letter("s",vector2,vector3)
    
def show_message_test(sense_hat):
    colorRGB=RRN.GetNamedArrayDType("com.robotraconteur.color.ColorRGBAu",sense_hat)
    vector2=numpy.zeros((1,),dtype=colorRGB)
    vector2[i]['r']=255
    vector2[i]['g']=255
    vector2[i]['b']=255
    vector2[i]['a']=0
    
    vector3=numpy.zeros((1,),dtype=colorRGB)
    vector3[i]['r']=180
    vector3[i]['g']=180
    vector3[i]['b']=180
    vector3[i]['a']=0
    sense_hat.Show_message("Hello!",vector2,vector3,0.5)


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
    show_letter_test(c)
    time.sleep(1)
    flip_h_test(c)
    time.sleep(1)
    flip_v_test(c)
    time.sleep(1)
    set_rotation_test(c)
    time.sleep(1)
    set_message_test(c)
    
    
    #c.setf_pixel(1,1,vector2)
    
    time.sleep(1)

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
    

if __name__== '__main__':
    main()
