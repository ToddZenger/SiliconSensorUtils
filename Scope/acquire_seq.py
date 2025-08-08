
import argparse
import time
import datetime
import visa

"""#################SEARCH/CONNECT#################"""
# establish communication with scope
initial = time.time()
rm = visa.ResourceManager("@py")
lecroy = rm.open_resource('TCPIP0::192.168.24.102::INSTR')
lecroy.timeout = 3000000
lecroy.encoding = 'latin_1'
lecroy.clear()
BASE_PATH = "/home/daq/2025_08_SNSPD/ScopeHandler/"
run_log_path = BASE_PATH + "/Lecroy/Acquisition/RunLog.txt"


def GetNextNumber():
    run_num_file = BASE_PATH + "/Lecroy/Acquisition/next_run_number.txt"
    FileHandle = open(run_num_file)
    nextNumber = int(FileHandle.read().strip())
    FileHandle.close()
    FileHandle = open(run_num_file,"w")
    FileHandle.write(str(nextNumber+1)+"\n") 
    FileHandle.close()
    return nextNumber

nchan=8

parser = argparse.ArgumentParser(description='Run info.')

parser.add_argument('--numEvents',metavar='Events', type=str,default = 500, help='numEvents (default 500)',required=False)
parser.add_argument('--runNumber',metavar='runNumber', type=str,default = -1, help='runNumber (default -1)',required=False)
parser.add_argument('--sampleRate',metavar='sampleRate', type=str,default = 10, help='Sampling rate (default 20)',required=False)
parser.add_argument('--horizontalWindow',metavar='horizontalWindow', type=str,default = 50, help='horizontal Window (default 125)',required=False)
# parser.add_argument('--numPoints',metavar='Points', type=str,default = 500, help='numPoints (default 500)',required=True)
parser.add_argument('--trigCh',metavar='trigCh', type=str, default='EX',help='trigger Channel (EX, or CN',required=False)
parser.add_argument('--trig',metavar='trig', type=float, default= 0.150, help='trigger value in V',required=False)
parser.add_argument('--trigSlope',metavar='trigSlope', type=str, default= 'NEGative', help='trigger slope; positive(rise) or negative(fall)',required=False)

parser.add_argument('--display',metavar='display', type=int, default= 0, help='enable display',required=False)


parser.add_argument('--timeoffset',metavar='timeoffset', type=float, default=0, help='Offset to compensate for trigger delay. This is the delta T between the center of the acquisition window and the trigger. (default for NimPlusX: -160 ns)',required=False)
parser.add_argument('--holdoff',metavar='holdoff', type=float, default=0, help='trigger hold off time in units of ns, default is 0',required=False)
parser.add_argument('--auxOutPulseWidth',metavar='args.auxOutPulseWidth', type=float, default=0, help='Aux Output Pulse Width',required=False)

# parser.add_argument('--save',metavar='save', type=int, default= 1, help='Save waveforms',required=False)
# parser.add_argument('--timeout',metavar='timeout', type=float, default= -1, help='Max run duration [s]',required=False)

args = parser.parse_args()
trigCh = str(args.trigCh) 
runNumber = int(args.runNumber) 
if trigCh != "AUX": trigCh = 'CHANnel'+trigCh
trigLevel = float(args.trig)
triggerSlope = args.trigSlope
timeoffset = float(args.timeoffset)*1e-9
# print "timeoffset is ",timeoffset
date = datetime.datetime.now()
# savewaves = int(args.save)
# timeout = float(args.timeout)
# print savewaves
# print "timeout is ",timeout

if runNumber==-1:
	runNumber=GetNextNumber()
      
lecroy.write('STOP')
lecroy.write("*CLS")
lecroy.write("COMM_HEADER OFF")
if args.display == 0: lecroy.write("DISPLAY OFF")
else: lecroy.write("DISPLAY ON")

lecroy.write("*TRG")

lecroy.write("WAIT")

lecroy.query("ALST?")

lecroy.write(r"""vbs 'app.SaveRecall.Waveform.TraceTitle="Trace%i" ' """%(runNumber))
lecroy.write(r"""vbs 'app.SaveRecall.Waveform.SaveFile' """)
lecroy.query("ALST?")

lecroy.close()
rm.close()