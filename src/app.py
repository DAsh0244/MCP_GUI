import sys
# import psu_control
# import scope_control
from psu_control import Keithley2220G1
from scope_control import TekScope
from PyQt5.QtCore import Qt,QTimer,QCoreApplication
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget
from uic.MainWindow import Ui_MainWindow as MainWindow
from uic.about_dialog import Ui_Dialog as AboutDialog
from uic.set_devices_dialog import Ui_Dialog as SetDevicesDialog 
import numpy as np

from enum import Enum, auto
# from collections import deque
from PyQt5 import QtTest

__version_info = (0,0,1)
__version__ = '.'.join(map(str,__version_info))

# wait a second before taking measurement
STABILIZE_TIME = 1000

class MCP_GUI_MODE(Enum):
    NORMAL = auto()
    LIVE = auto()
    ERROR = auto()


class MCP_GUI_OP(Enum):
    NOP = 'NOP'
    SWEEP = 'Sweep'
    SAVING = 'Saving Data'
    CAPTURE = 'Capturing Waveform'

# todo: implement this shit
def scan_ports():
    return ['Not','Implemented','YET']

def close_app():
    print('closing')
    QCoreApplication.quit()

class MCP_GUI(QMainWindow, MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('MCP Control Panel v{}'.format(__version__))
        self.config = {}
        self.premateure = False
        self._operations = []
        self.live_rail = False
        self.live_capture = False
        self.halt_operation = False
        self.op = [MCP_GUI_OP.NOP,0]  # stack of currently queued operations (sweep->Measure->Capture)
        self.mode = MCP_GUI_MODE.NORMAL
        self.actionAbout.triggered.connect(self.open_about_dialog)
        self.actionSpecify_GPIB_Addresses.triggered.connect(lambda x :self.open_set_devies_dialog(self.config))
        self.actionExit.triggered.connect(self.close)
        self.live_rails.stateChanged.connect(self.rail_checkbox_handler)
        self.live_measure.stateChanged.connect(self.measure_checkbox_handler)
        self.rail_settings_push_button.clicked.connect(self.update_rails)
        self.measure_button.clicked.connect(self.make_measurement)
        self.sweep_button.clicked.connect(self.sweep_rails)
        self.halt_button.clicked.connect(self.halt_sweep)
        self.show()
        self.open_set_devies_dialog()
        if not self.config:
            self.premateure = True
            self.close()
        # self.termination()
        else:
            print(self.config)
        self.psu = Keithley2220G1(port=self.config['prologix_port'],addr=self.config['psu_addr'])
        self.psu_reset_channel = 1
        self.psu_bias_channel = 2 
        self.scope = TekScope(port=self.psu._ser,addr=self.config['scope_addr'])
        self.scope_input_channel = 1


        self.mcp_params = {
            'v_bias':self.vbias_box.value(),
            'v_reset':self.vreset_box.value(),
            'i_bias': self.ibias_box.value(),
            'i_reset': self.ireset_box.value(),
        }
        self.sweep_params = {
            'v_bias_min':self.sweep_bias_min.value(),
            'v_bias_max':self.sweep_bias_max.value(),
            'v_bias_step':self.sweep_bias_step.value(),
            'v_reset_min':self.sweep_reset_min.value(),
            'v_reset_max':self.sweep_reset_max.value(),
            'v_reset_step':self.sweep_reset_step.value(),
        }
        self.measurements = {
            'wave_pre':None,
            'wave_data':None,
            'meas_min':None,
            'meas_max':None,
        }
        # print(self.mcp_params)
        # print(self.sweep_params)

    def measure_checkbox_handler(self,state):
        if state == Qt.Checked:
            self.live_capture = True
            self.measure_button.setEnabled(False)
            self.make_measurement()
        else:
            self.live_capture = False
            self.measure_button.setEnabled(True)

    def rail_checkbox_handler(self,state):      
        if state == Qt.Checked:
            self.live_rail = True
            self.rail_settings_push_button.setEnabled(False)
            self.update_rails()
            self.vbias_box.valueChanged.connect(self.update_rails)
            self.vreset_box.valueChanged.connect(self.update_rails)
            self.ibias_box.valueChanged.connect(self.update_rails)
            self.ireset_box.valueChanged.connect(self.update_rails)
        else:
            self.live_rail = True
            self.rail_settings_push_button.setEnabled(True)
            self.vbias_box.valueChanged.disconnect(self.update_rails)
            self.vreset_box.valueChanged.disconnect(self.update_rails)
            self.ibias_box.valueChanged.disconnect(self.update_rails)
            self.ireset_box.valueChanged.disconnect(self.update_rails)

    def update_rails(self):
        self.mcp_params = {
            'v_bias':self.vbias_box.value(),
            'v_reset':self.vreset_box.value(),
            'i_bias': self.ibias_box.value(),
            'i_reset': self.ireset_box.value(),
        }
        # self.psu.set_voltage(self.psu_bias_channel,self.mcp_params['v_bias'])
        # self.psu.set_voltage(self.psu_reset_channel,self.mcp_params['v_reset'])
        # self.psu.set_current(self.psu_bias_channel,self.mcp_params['i_bias'])
        # self.psu.set_current(self.psu_bias_channel,self.mcp_params['i_reset'])

    def capture_waveform(self):
        print('capturing')
        preamble,data = self.scope.capture_waveform()
        times, voltages = self.scope.convert_raw_samples(data, preamble)
        return times, voltages

    def make_measurement(self,save=False):
        times, voltages = self.capture_waveform()
        self.MplWidget.update(times,voltages)
        print('measuring')



    def sweep_rails(self):
        self.sweep_params = {
            'v_bias_min':self.sweep_bias_min.value(),
            'v_bias_max':self.sweep_bias_max.value(),
            'v_bias_step':self.sweep_bias_step.value(),
            'v_reset_min':self.sweep_reset_min.value(),
            'v_reset_max':self.sweep_reset_max.value(),
            'v_reset_step':self.sweep_reset_step.value(),
        }
        self.live_rails.setChecked(True)
        self.live_rails.setEnabled(False)
        self.vreset_box.setEnabled(False)
        self.vbias_box.setEnabled(False)
        self.ibias_box.setEnabled(False)
        self.ireset_box.setEnabled(False)
        reset_range = np.arange(self.sweep_params['v_reset_min'], self.sweep_params['v_reset_max'],self.sweep_params['v_reset_step']) 
        bias_range = np.arange(self.sweep_params['v_bias_min'],self.sweep_params['v_bias_max'],self.sweep_params['v_bias_step'])
        total_iterations = reset_range.size * bias_range.size
        iterations = 0 
        old_mcp_params = self.mcp_params.copy()
        self.op = [MCP_GUI_OP.SWEEP,0]
        for reset_voltage in reset_range:
            for bias_voltage in bias_range:
                print(reset_voltage, bias_voltage)
                if self.halt_operation:
                    self.halt_operation = False
                    self.vreset_box.setValue(old_mcp_params['v_reset'])
                    self.vbias_box.setValue(old_mcp_params['v_bias'])
                    self.live_rails.setChecked(False)
                    self.live_rails.setEnabled(True)
                    self.vreset_box.setEnabled(True)
                    self.vbias_box.setEnabled(True)
                    self.ibias_box.setEnabled(True)
                    self.ireset_box.setEnabled(True)
                    self.op_complete()
                    self.progressBar.setValue(0)
                    self.op = [MCP_GUI_OP.NOP,0]
                    return   
                # self.psu.set_voltage(self.psu_reset_channel, -reset_voltage)
                # self.psu.set_voltage(self.psu_bias_channel, bias_voltage)
                self.vbias_box.setValue(bias_voltage)
                self.vreset_box.setValue(reset_voltage)
                # wait for a voltages to stabilize
                QtTest.QTest.qWait(STABILIZE_TIME)
                self.make_measurement(save=True)
                iterations += 1
                self.update_progress_bar(round(iterations/total_iterations*100))
        self.vreset_box.setValue(old_mcp_params['v_reset'])
        self.vbias_box.setValue(old_mcp_params['v_bias'])
        self.live_rails.setChecked(False)
        self.live_rails.setEnabled(True)
        self.vreset_box.setEnabled(True)
        self.vbias_box.setEnabled(True)
        self.ibias_box.setEnabled(True)
        self.ireset_box.setEnabled(True)
        self.op_complete()

    def update_progress_bar(self,progress):
        self.progressBar.setValue(progress)
        self._operations[-1][1] = progress

    def halt_sweep(self):
        self.halt_operation = True

    @property
    def op(self):
        return self._operations[-1]

    @op.setter
    def op(self,operation):
        self._operations.append(operation)
        self.operation_label.setText(self._operations[-1][0].value)
        self.update_progress_bar(self._operations[-1][1])

    def op_complete(self):
        self._operations.pop()
        self.operation_label.setText(self._operations[-1][0].value)
        self.progressBar.setValue(self._operations[-1][1])   

    def _launch_dialog(self, Form):
        dialog = QDialog()
        dialog.ui = Form()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()

    def open_about_dialog(self):
        dialog = QDialog()
        dialog.ui = AboutDialog()
        dialog.ui.setupUi(dialog)
        dialog.exec()
        dialog.show()

    def open_set_devies_dialog(self, start_params=None):
        # dialog = QDialog()
        # dialog.ui = SetDevicesDialog()
        # dialog.ui.setupUi(dialog)
        dialog = MCPGUIDeviceDialog(parent=self, start_params=start_params)
        dialog.exec()
        dialog.show()

class MCPGUIDeviceDialog(QDialog,SetDevicesDialog):
    def __init__(self, start_params=None, parent=None):
        super().__init__(parent=parent)
        self.parent=parent
        self.setupUi(self)
        self.setWindowTitle('Device Configuration')
        self.buttonBox.accepted.connect(self.pass_configuration)
        # self.buttonBox.rejected.connect(self.close)
        # self.buttonBox.rejected.connect(parent.close)
        self.scan_button.clicked.connect(self.port_scan)
        if start_params is not None:
            print('populating fields')
            self.psu_addr_box.setValue(start_params['psu_addr'])
            self.scope_addr_box.setValue(start_params['scope_addr'])
            self.prologix_port_box.clear()
            if start_params['prologix_port']:
                self.prologix_port_box.addItem(start_params['prologix_port'])
            else:
                self.prologix_port_box.addItems(scan_ports())

    def port_scan(self):
        ports = scan_ports()
        self.prologix_port_box.clear()
        self.prologix_port_box.addItems(ports)

    def pass_configuration(self):
        self.parent.config = {
            'psu_addr':self.psu_addr_box.value(),
            'scope_addr':self.scope_addr_box.value(),
            'prologix_port':self.prologix_port_box.currentText(),
        }

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MCP_GUI()
    if not w.premateure:
        sys.exit(app.exec_())