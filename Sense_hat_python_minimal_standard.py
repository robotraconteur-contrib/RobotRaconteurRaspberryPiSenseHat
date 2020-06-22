from sense_hat import SenseHat
import RobotRaconteur as RR
import threading
from general_robotics_toolbox import *
import numpy

RRN=RR.RobotRaconteurNode.s

class Sense_hat_IMU(object):
    def __init__(self,sense_hat):
        self.Sense_hat=sense_hat
    
    def send_data(self):
        state=RRN.NewStructure("com.robotraconteur.imu.ImuState")
        quaterniontype=RRN.GetNamedArrayDType("com.robotraconteur.geometry.Quaternion")
        quaternion=numpy.zeros((1,),dtype=quaterniontype)
        orientation=self.Sense_hat.get_orientation()
        rpy=[0.0,0.0,0.0]
        rpy[0]=orientation["roll"]
        rpy[1]=orientation["pitch"]
        rpy[2]=orientation["yaw"]
        r_matrix=rpy2R(rpy)
        quat=R2q(r_matrix) 
        quaternion[0]['w']=quat[0]
        quaternion[0]['x']=quat[1]
        quaternion[0]['y']=quat[2]
        quaternion[0]['z']=quat[3]
        state.orientation=quaternion
        acceleration=self.Sense_hat.get_accelerometer_raw()
        vector3type=RRN.GetNamedArrayDType("com.robotraconteur.geometry.Vector3")
        vector3=numpy.zeros((1,),dtype=vector3type)
        vector3[0]['x']=acceleration['x']
        vector3[0]['y']=acceleration['y']
        vector3[0]['z']=acceleration['z']
        state.linear_acceleration=vector3
        self.imu_state.OutValue=state
        
        

class Sense_hat(object):
    def __init__(self,sense_hat,imu_interface):
        self.Sense_hat=sense_hat
        self.Sense_hat.stick.direction_any=joystick_event
        self.IMU_interface=imu_interface
        self.Bump=RR.EventHook()
        self.sensor_streaming=False
        self._lock=threading.RLock()
        self.interface_imu=imu_interface
        self.joystick_thread=threading.Thread(target=self._read_joystick)
        self.joystick_thread.start()
        
        
    def Show_message(self,message,text_color=[0,0,0],back_color=[255,255,255],scroll_speed=1.0):
        try:
            text_color=tuple(text_color)
            back_color=tuple(back_color)
        except:
            pass
        if((type(message) is str) and (type(scroll_speed) is float) and (type(text_color) is tuple) and len(text_color)==3 and (type(back_color) is tuple) and len(back_color)==3):
            self.Sense_hat.show_message(message,text_color,back_color,scroll_speed)
        else:
            raise Exception("Format of Message is incorrect, cannot display")
    
    def Clear(self, color):
        try:
            color=tuple(color)
            
        except:
            pass
        if((type(color) is tuple) and len(color)==3):
            self.Sense_hat.clear(color)
        else:
            raise Exception("Cannot set color/clear")
            
            
    def Show_letter(self, letter,text_color=(0,0,0),back_color=(255,255,255)):
        try:
            text_color=tuple(text_color)
            back_color=tuple(back_color)
        except:
            pass
        if((type(letter) is str) and (type(text_color) is tuple) and len(text_color)==3 and (type(back_color) is tuple) and len(back_color)==3):
            self.Sense_hat.show_letter(letter,text_color,back_color)
        else:
            raise Exception("Format of letter to show is incorrect, cannot display")
            
            
    def Set_pixel(self, x, y, color):
        try:
            color=tuple(color)
        except:
            pass
        if((type(x) is int) and (type(y) is int) and (type(color) is tuple) and len(color)==3):
            self.Sense_hat.set_pixel(x,y,color)
        else:
            raise Exception("Cannot set pixel")
            
    def Set_pixels(self, color_array):
        try:
            for item in color_array:
                item=tuple(item)
        except:
            pass
        if(isinstance(color_array,list) and (type(color_array[0]) is tuple) and len(color_array[0])==3 and len(color_array)==64):
            self.Sense_hat.set_pixels(color_array)
        else:
            raise Exception("Cannot set pixels")
            
    def Set_rotation(self, rotation):
        if(type(rotation) is int):
            self.Sense_hat.set_rotation(rotation)
        else:
            raise Exception("Cannot set rotation")
    
    def Flip_v(self):
        self.Sense_hat.flip_v()
    
    def Flip_h(self):
        self.Sense_hat.flip_h()
        
    def Start_streaming(self):
        with self._lock:
            if(!self.sensor_streaming):
                self.sensor_streaming=True
                t=threading.Thread(target=self._recv_thread)
                t.start()
            else:
                raise Exception("Already streaming")
    
    def Stop_streaming(self):
        with self._lock:
            if(self.sensor_streaming):
                self.sensor_streaming=False
    
    def _recv_thread(self):
        try:
            while self.sensor_streaming:
                if (not self.sensor_streaming): return
                self._Read_Sensors()
        except:
            
            if (self.sensor_streaming):

                traceback.print_exc()
            pass
    
    def _Read_Sensors(self):
        
        pressure=self.Sense_hat.get_pressure()
        self.pressure.OutValue=pressure
        temperature=self.Sense_hat.get_temperature()
        self.temperature.OutValue=temperature
        humidity=self.Sense_hat.get_humidity()
        self.humidity.OutValue=humidity
        self.IMU_interface.send_data()
    
    def _read_joystick(self):
        while(True):
            output=[0.0,0.0]
            if event.direction == 'up':
                output[1]=1
            if event.direction == 'down':
                output[1]=-1
            if event.direction == 'left':
                output[0]=-1
            if event.direction == 'right':
                output[0]=1
            if event.direction == 'middle':
                output=[2.0,2.0]
            outputnamed=RRN.ArrayToNamedArray(output,"com.robotraconteur.geometry.Vector2")
            self.joystick_state.OutValue=outputnamed
        
    def joystick_event(self, event):
        if event.action=='pressed':
            output=[0.0,0.0]
            if event.direction == 'up':
                output[1]=1
            if event.direction == 'down':
                output[1]=-1
            if event.direction == 'left':
                output[0]=-1
            if event.direction == 'right':
                output[0]=1
            if event.direction == 'middle':
                output=[2.0,2.0]
            outputnamed=RRN.ArrayToNamedArray(output,"com.robotraconteur.geometry.Vector2")
            self.joystick_move.fire(outputnamed)
            
            
def main():

    

    
    with RR.ServerNodeSetup(nodename,port) as node_setup:
        RRN.RegisterServiceTypeFromFile("com.robotraconteur.geometry")
        RRN.RegisterServiceTypeFromFile("com.robotraconteur.color")
        RRN.RegisterServiceTypeFromFile("com.robotraconteur.imu")



if __name__ == '__main__':
    main()