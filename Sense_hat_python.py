from sense_hat import SenseHat
import RobotRaconteur as RR
import threading
from general_robotics_toolbox import *
import numpy
import traceback
import argparse
import sys

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
        angular_velocity=self.Sense_hat.get_gyroscope_raw()
        vector3=numpy.zeros((1,),dtype=vector3type)
        vector3[0]['x']=angular_velocity['x']
        vector3[0]['y']=angular_velocity['y']
        vector3[0]['z']=angular_velocity['z']
        state.angular_velocity=vector3	
        self.imu_state.OutValue=state
        
        

class Sense_hat(object):
    def __init__(self,sense_hat,imu_interface):
        self.Sense_hat=sense_hat
        self.Sense_hat.stick.direction_any=self.joystick_event
        self.IMU_interface=imu_interface
        self.joystick_move=RR.EventHook()
        self.sensor_streaming=False
        self._lock=threading.RLock()
        self.interface_imu=imu_interface
        self.up_state=False
        self.down_state=False
        self.right_state=False
        self.left_state=False
        self.middle_state=False
        self.joystick_thread=threading.Thread(target=self._read_joystick)
        self.Sense_hat.clear()
        
        
        
    def Show_message(self,message,text_color,back_color,scroll_speed=1.0):
        
        text_color_tuple=(text_color['r'][0],text_color['g'][0],text_color['b'][0])
        back_color_tuple=(back_color['r'][0],back_color['g'][0],back_color['b'][0])
        #try:
        self.Sense_hat.show_message(message,text_colour=text_color_tuple,back_colour=back_color_tuple,scroll_speed=scroll_speed)
        #except:
        #    traceback.print_exc()
        
    
    def Clear(self, color):
        color_tuple=(color['r'][0],color['g'][0],color['b'][0])
        print(color_tuple)
        try:
            self.Sense_hat.clear(color_tuple)
        except:
            traceback.print_exc()
            
            
    def Show_letter(self, letter,text_color,back_color):
        text_color_tuple=(text_color['r'][0],text_color['g'][0],text_color['b'][0])
        back_color_tuple=(back_color['r'][0],back_color['g'][0],back_color['b'][0])
        try:
            self.Sense_hat.show_letter(letter,text_color_tuple,back_color_tuple)
        
        except:
            traceback.print_exc()
        
            
            
    def setf_pixel(self, x, y, color):
        
        color_tuple=(color['r'][0],color['g'][0],color['b'][0])
        try:
            self.Sense_hat.set_pixel(x,y,color_tuple)
        except:
            traceback.print_exc()
        
            
    def setf_pixels(self, color_array):
    
        color_array_tuple=[]
        try:
            
            for item in color_array:
                color_array_item_tuple=(item['r'],item['g'],item['b'])
                color_array_tuple.append(color_array_item_tuple)
                
                
           
            if( len(color_array_tuple)==64):
                self.Sense_hat.set_pixels(color_array_tuple)
            else:
                raise Exception("Cannot set pixels, you need to define colors for all 64 pixels")
                
        except:
            traceback.print_exc()
        
            
    def setf_rotation(self, rotation):
        #if(type(rotation) is int):
        self.Sense_hat.set_rotation(rotation)
        #else:
        #    raise Exception("Cannot set rotation")
    
    def Flip_v(self):
        self.Sense_hat.flip_v()
    
    def Flip_h(self):
        self.Sense_hat.flip_h()
        
    def Start_streaming(self):
        with self._lock:
            if(not self.sensor_streaming):
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
        self.Pressure.OutValue=pressure
        temperature=self.Sense_hat.get_temperature()
        self.Temperature.OutValue=temperature
        humidity=self.Sense_hat.get_humidity()
        self.Humidity.OutValue=humidity
        self.IMU_interface.send_data()
    
    def _read_joystick(self):
        while(True):
            output=[0.0,0.0]
            if self.up_state:
                output[1]=1
            if self.down_state:
                output[1]=-1
            if self.left_state:
                output[0]=-1
            if self.right_state:
                output[0]=1
            if self.middle_state:
                output=[2.0,2.0]
            vector2type=RRN.GetNamedArrayDType("com.robotraconteur.geometry.Vector2")
            vector2=numpy.zeros((1,),dtype=vector2type)
            vector2[0]['x']=output[0]
            vector2[0]['y']=output[1]
            #outputnamed=RRN.ArrayToNamedArray(output,"com.robotraconteur.geometry.Vector2")
            self.joystick_state.OutValue=vector2
    
    def _fire_joystick_move(self,data):
        self.joystick_move.fire(data)

    def joystick_event(self, event):
        if event.action=='pressed':
            output=[0.0,0.0]
            if event.direction == 'up':
                output[1]=1
                self.up_state=True
            if event.direction == 'down':
                output[1]=-1
                self.down_state=True
            if event.direction == 'left':
                output[0]=-1
                self.left_state=True
            if event.direction == 'right':
                output[0]=1
                self.right_state=True
            if event.direction == 'middle':
                output=[2.0,2.0]
                self.middle_state=True
            
            vector2type=RRN.GetNamedArrayDType("com.robotraconteur.geometry.Vector2")
            vector2=numpy.zeros((1,),dtype=vector2type)
            vector2[0]['x']=output[0]
            vector2[0]['y']=output[1]
            #outputnamed=RRN.ArrayToNamedArray(output,"com.robotraconteur.geometry.Vector2")
            #self.joystick_move.fire(vector2)
            self._fire_joystick_move(vector2)

        if event.action=='released':
            if event.direction == 'up':
                
                self.up_state=False
            if event.direction == 'down':
                
                self.down_state=False
            if event.direction == 'left':
                
                self.left_state=False
            if event.direction == 'right':
                
                self.right_state=False
            if event.direction == 'middle':
                
                self.middle_state=False

            
def main():
    parser = argparse.ArgumentParser(description="Example Robot Raconteur iRobot Create service")    
    parser.add_argument("--nodename",type=str,default="sense_hat.SenseHat",help="The NodeName to use")
    parser.add_argument("--tcp-port",type=int,default=2354,help="The listen TCP port")
    parser.add_argument("--wait-signal",action='store_const',const=True,default=False)
    args = parser.parse_args()
    sense = SenseHat()
    imu_service=Sense_hat_IMU(sense)
    sensor_hat_service=Sense_hat(sense,imu_service)

    
    with RR.ServerNodeSetup(args.nodename,args.tcp_port) as node_setup:
        RRN.RegisterServiceTypeFromFile("com.robotraconteur.uuid")
        RRN.RegisterServiceTypeFromFile("com.robotraconteur.identifier")
        RRN.RegisterServiceTypeFromFile("com.robotraconteur.geometry")
        
        RRN.RegisterServiceTypeFromFile("com.robotraconteur.color")
        RRN.RegisterServiceTypeFromFile("com.robotraconteur.datetime")
        RRN.RegisterServiceTypeFromFile("com.robotraconteur.sensordata")
        RRN.RegisterServiceTypeFromFile("com.robotraconteur.resource")
        RRN.RegisterServiceTypeFromFile("com.robotraconteur.device")
        RRN.RegisterServiceTypeFromFile("com.robotraconteur.datatype")
        RRN.RegisterServiceTypeFromFile("com.robotraconteur.param")
        RRN.RegisterServiceTypeFromFile("com.robotraconteur.units")
        
        RRN.RegisterServiceTypeFromFile("com.robotraconteur.sensor")
        RRN.RegisterServiceTypeFromFile("com.robotraconteur.imu")
        RRN.RegisterServiceTypeFromFile("experimental.sensehat")
        RRN.RegisterService("SensorHat","experimental.sensehat.SenseHat",sensor_hat_service)
        RRN.RegisterService("SensorHatIMU","com.robotraconteur.imu.ImuSensor",imu_service)
        sensor_hat_service.joystick_thread.start()
    
        if args.wait_signal:  
            #Wait for shutdown signal if running in service mode          
            print("Press Ctrl-C to quit...")
            import signal
            signal.sigwait([signal.SIGTERM,signal.SIGINT])
        else:
            #Wait for the user to shutdown the service
            if (sys.version_info > (3, 0)):
                input("Server started, press enter to quit...")
            else:
                raw_input("Server started, press enter to quit...")
    


if __name__ == '__main__':
    main()
