import libximc.highlevel as ximc

# Motor setup and control

class Motor:

    def __init__(self,
                 Motor_X = r"xi-com:///dev/ttyACM2",
                 Motor_Y = r"xi-com:///dev/ttyACM0",
                 Motor_Z = r"xi-com:///dev/ttyACM1",
                 ):
        self.axis_x = ximc.Axis(Motor_X)
        self.axis_y = ximc.Axis(Motor_Y)
        self.axis_z = ximc.Axis(Motor_Z)


    def initialize_devices(self, step_to_um_conversion_coeff = 2.5):
        self.axis_x.open_device()
        self.axis_y.open_device()
        self.axis_z.open_device()

        engine_settings_x = self.axis_x.get_engine_settings()
        engine_settings_y = self.axis_y.get_engine_settings()
        engine_settings_z = self.axis_z.get_engine_settings()

        self.axis_x.set_calb(step_to_um_conversion_coeff, engine_settings_x.MicrostepMode)
        self.axis_y.set_calb(step_to_um_conversion_coeff, engine_settings_y.MicrostepMode)
        self.axis_z.set_calb(step_to_um_conversion_coeff, engine_settings_z.MicrostepMode)

    def close_devices(self):
        print("Stop movement")
        self.axis_x.command_stop()
        self.axis_y.command_stop()
        self.axis_z.command_stop()

        print("Disconnect device")
        self.axis_x.close_device()  # It's also called automatically by the garbage collector, so explicit closing is optional
        self.axis_y.close_device()
        self.axis_z.close_device()
    
    def get_calb(self):
        position_calb_x = self.axis_x.get_position_calb()
        position_calb_y = self.axis_y.get_position_calb()
        position_calb_z = self.axis_z.get_position_calb()

        return position_calb_x, position_calb_y, position_calb_z

    def move_XYZ_R(self, dX=0, dY=0, dZ=0, wait_time=100, verbose=False):

        if dX: # Note 0 is False
            self.axis_x.command_movr_calb(dX)
            if verbose: print(f"Moving X by {dX} um")
            self.axis_x.command_wait_for_stop(wait_time)
        if dY: # Note 0 is False
            self.axis_y.command_movr_calb(dY)
            if verbose: print(f"Moving Y by {dY} um")
            self.axis_y.command_wait_for_stop(wait_time)
        if dZ: # Note 0 is False
            self.axis_z.command_movr_calb(dZ)
            if verbose: print(f"Moving Z by {dZ} um")
            self.axis_z.command_wait_for_stop(wait_time)
    
    def move_XYZ(self, X=0, Y=0, Z=0, wait_time=100, verbose=False):

        if X: # Note 0 is False
            self.axis_x.command_move_calb(X)
            if verbose: print(f"Moving X to {X} um")
            self.axis_x.command_wait_for_stop(wait_time)
        if Y: # Note 0 is False
            self.axis_y.command_move_calb(Y)
            if verbose: print(f"Moving Y to {X} um")
            self.axis_y.command_wait_for_stop(wait_time)
        if Z: # Note 0 is False
            self.axis_z.command_move_calb(Z)
            if verbose: print(f"Moving Z to {X} um")
            self.axis_z.command_wait_for_stop(wait_time)


