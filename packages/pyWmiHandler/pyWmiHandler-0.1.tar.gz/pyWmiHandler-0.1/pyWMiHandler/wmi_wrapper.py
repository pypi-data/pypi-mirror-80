from wmi import WMI, x_wmi_timed_out
import pythoncom
import threading
import time
from win32api import GetFileVersionInfo, LOWORD, HIWORD

try:
    from .helpers import convert_to_human_readable
except ModuleNotFoundError:
    from pyWmiHandler.helpers import convert_to_human_readable
except ImportError:
    from pyWmiHandler.helpers import convert_to_human_readable


def get_version_number(filename):
    if not threading.current_thread() is threading.main_thread():
        pythoncom.CoInitialize()
    try:
        info = GetFileVersionInfo(filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls)
    except Exception as e:
        return 0, 0, 0, 0
    finally:
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoUninitialize()


class WmiHandler():

    @staticmethod
    def get_serial_number():
        """Thread Safe WMI Query for Serial Number in Win32_Bios Class"""
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        w = WMI()
        try:
            for sn in w.Win32_Bios(["SerialNumber"]):
                return sn.SerialNumber
        except Exception as e:
            print(e)
            return None
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()


    @staticmethod
    def get_video_cards():
        """Thread Safe WMI Query for Video Cards in Win32_VideoController Class"""
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        w = WMI()
        video_cards = []
        try:
            for v in w.Win32_VideoController(["Caption", "Status"]):
                video_cards.append({'Caption': v.Caption, 'Status': v.Status})
            return video_cards
        except Exception as e:
            print(e)
            return []
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()


    @staticmethod
    def get_operating_system_info():
        """Thread Safe WMI Query for Caption, build, arch, systemDrive in Win32_OperatingSystem Class"""
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        w = WMI()
        try:
            for os in w.Win32_OperatingSystem(["Caption", "OSArchitecture", "MUILanguages", "Version", "SystemDrive"]):
                return {
                    "name": os.Caption,
                    "arch": os.OSArchitecture,
                    "languages": os.MUILanguages,
                    'build': os.Version,
                    'system_drive': os.SystemDrive
                }
        except Exception as e:
            print(e)
            return None
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

    @staticmethod
    def get_model():
        """Thread Safe WMI Query for Serial Number in Win32_Bios Class"""
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        w = WMI()
        try:
            for m in w.Win32_ComputerSystem(["Model"]):
                return m.Model
        except Exception as e:
            print(e)
            return None
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

    @staticmethod
    def get_manufacturer():
        """Thread Safe WMI Query for Serial Number in Win32_Bios Class"""
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        w = WMI()
        try:
            for m in w.Win32_ComputerSystem(["Manufacturer"]):
                return m.Manufacturer
        except Exception as e:
            print(e)
            return None
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

    @staticmethod
    def get_processors():
        """Thread Safe WMI Query for Processors info in Win32_Processor Class"""
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        w = WMI()
        processors = []
        try:
            for p in w.Win32_Processor(["Name"]):
                processors.append(p.Name)
            return processors
        except Exception as e:
            print(e)
            return None
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

    @staticmethod
    def is_computer_on_AC_power():
        """Thread Safe WMI Query return True if AC adapter is connected"""
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        w = WMI()
        try:
            for bat in w.Win32_Battery(["BatteryStatus"]):
                return bat.BatteryStatus in [2, 3, 6, 7, 8, 9, 11]
        except Exception as e:
            print(e)
            return None
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

    @staticmethod
    def is_windows_activated():
        """Thread Safe WMI Query return True if windows is activated"""
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        w = WMI()
        try:
            for win in w.SoftwareLicensingProduct(["LicenseStatus"],
                                                  ApplicationID='55c92734-d682-4d71-983e-d6ec3f16059f'):
                if win.LicenseStatus == 1:
                    return True
            return False
        except Exception as e:
            print(e)
            return False
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

    @staticmethod
    def get_estimated_battery_level():
        batteries = []
        """Thread Safe WMI Query for remaining battery level"""
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        w = WMI()
        try:
            for bat in w.Win32_Battery(["EstimatedChargeRemaining"]):
                batteries.append(bat.EstimatedChargeRemaining)
        except Exception as e:
            print(e)
            batteries.append(-1)
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()
            return batteries

    @staticmethod
    def set_display_brightness(brightness):
        """Thread Safe WMI Query for setting display brightness"""
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        w = WMI(namespace="WMI")
        try:
            for mon in w.WmiMonitorBrightnessMethods():
                mon.WmiSetBrightness(brightness, 0)
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

    @staticmethod
    def get_total_memory_amount(get_human_readable_value=False):
        """Thread Safe WMI Query for setting display brightness"""
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        w = WMI()
        try:
            total_amount = 0
            for mem in w.Win32_PhysicalMemory(['Capacity']):
                total_amount += int(mem.Capacity)
            if get_human_readable_value:
                return convert_to_human_readable(total_amount, use_exact_size=True)
            return total_amount
        except Exception as e:
            print(e)
            return 0
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

    @staticmethod
    def get_pnp_devices():
        """Thread Safe WMI Query for list of system devices"""
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        w = WMI()
        try:
            devices = []
            for dev in w.Win32_PnPEntity():
                try:
                    devices.append({'caption': dev.Caption,
                                    'hw_id': dev.HardwareID[0],
                                    'name': dev.Name,
                                    'status': dev.Status
                                    })
                except Exception as ex:
                    pass
            return devices
        except Exception as e:
            print(e)
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

    @staticmethod
    def get_pnp_devices_with_drivers():
        """Thread Safe WMI Query for list of system devices and installed drivers"""
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        w = WMI()
        try:
            devices = []
            for dev in w.Win32_PnPEntity():
                for driver in dev.associators(wmi_result_class='Win32_SystemDriver'):
                    try:
                        devices.append({'caption': dev.Caption,
                                        'hw_id': dev.HardwareID[0],
                                        'name': dev.Name,
                                        'status': dev.Status,
                                        'driverName': driver.Caption,
                                        'driverFile': driver.PathName,
                                        'version': '.'.join([str(x) for x in get_version_number(driver.PathName)])
                                        })
                    except Exception as ex:
                        print(ex)
                        pass
            return devices
        except Exception as e:
            print(e)
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

    @staticmethod
    def get_disks_drives(internal_only=True):
        """Thread Safe WMI Query for Disk drives in Win32_DiskDrive Class
        Returns: array of Dictionary: {index, model, serial_number, capacity, human_capacity
        """
        disks = []
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        w = WMI()
        wql = 'SELECT * FROM Win32_DiskDrive'
        if internal_only:
            wql += ' WHERE InterfaceType <> "USB"'
        try:
            for dd in w.query(wql):
                d = {}
                d['index'] = dd.Index
                d['model'] = dd.Caption
                d['serial_number'] = dd.SerialNumber
                d['capacity'] = dd.Size
                d['human_capacity'] = convert_to_human_readable(dd.Size)
                disks.append(d)
            return disks
        except Exception as e:
            print(e)
            return None
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

    @staticmethod
    def get_system_sku(manufacturer=None):
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        try:
            my_sku = None
            w = WMI(namespace='WMI')
            for sku in w.MS_SystemInformation(["SystemSKU"]):
                my_sku = sku.SystemSKU
            if my_sku == None or my_sku == '':
                w = WMI()
                for sk2 in w.Win32_ComputerSystem(['OEMStringArray']):
                    my_sku = sk2.OEMStringArray[1][2:6]
            if manufacturer and ("dell" in manufacturer.lower() or 'alienware' in manufacturer.lower()) and str(
                    my_sku).strip() == 'None' or len(str(my_sku).strip()) != 4:
                print('Possibly wrong SKU on dell unit!')
            return my_sku
        except Exception as e:
            print(e)
            return None
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

    @staticmethod
    def get_IP():
        """Thread Safe WMI Query for get primary IP address"""
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()

        try:
            w = WMI()
            for m in w.Win32_NetworkAdapterConfiguration(["IPAddress"], IPEnabled=True):
                return m.IPAddress[0]
        except Exception as e:
            print(e)
            return None
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

    @staticmethod
    def is_ssd_drive(disk_id):
        """Thread Safe WMI Query for checking if disk drive is SSD  in MSFT_PhysicalDisk class"""
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()

        try:
            w = WMI(namespace='Microsoft\Windows\Storage')
            for m in w.MSFT_PhysicalDisk(["MediaType"], DeviceId=disk_id):
                return int(m.MediaType) == 4
        except Exception as e:
            print(e)
            return None
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

    @staticmethod
    def kill_process_by_name(name):
        """Thread Safe WMI Methods Execution for killing process by name using Win32_Process class"""
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        try:
            w = WMI()
            wql = 'SELECT * FROM Win32_Process WHERE Name LIKE "%{}%"'.format(name)
            success = True
            for process in w.query(wql):
                try:
                    process.Terminate()
                except Exception as e:
                    pass
            time.sleep(1)
            for p in w.query(wql):
                success=False
            return success
        except Exception as e:
            print(e)
            return False
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

    @staticmethod
    def get_batteries_info():
        batteries = []
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        try:
            w = WMI(namespace='WMI')
            for battery in w.BatteryStaticData(
                    ["Active", "DeviceName", "DesignedCapacity", "ManufactureName", "SerialNumber", "InstanceName"]):
                batt = {"DeviceName": battery.DeviceName,
                        "ManufactureName": battery.ManufactureName,
                        "SerialNumber": battery.SerialNumber,
                        "DesignedCapacity": battery.DesignedCapacity,
                        "InstanceName": battery.InstanceName}
                for capacity in w.BatteryFullChargedCapacity():
                    if batt['InstanceName'] == capacity.InstanceName:
                        batt['FullChargedCapacity'] = capacity.FullChargedCapacity
                for cycle_count in w.BatteryCycleCount():
                    if batt['InstanceName'] == cycle_count.InstanceName:
                        batt['CycleCount'] = cycle_count.CycleCount
                for details in w.BatteryStatus():
                    if batt['InstanceName'] == details.InstanceName:
                        batt['Status'] = {
                            'Active': details.Active,
                            'ChargeRate': details.ChargeRate,
                            'Charging': details.Charging,
                            'Discharging': details.Discharging,
                            'DischargeRate': details.DischargeRate,
                            'PowerOnline': details.PowerOnline,
                            'Voltage': details.Voltage,
                            'RemainingCapacity': details.RemainingCapacity

                        }
                batteries.append(batt)
            return batteries
        except Exception as e:
            print(e)
            return None
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

    @staticmethod
    def get_current_batteries_info(batteries: list):
        result = {}
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()
        try:
            w = WMI(namespace='WMI')
            for details in w.BatteryStatus():
                for battery in batteries:
                    result[battery] = None
                    if battery == details.InstanceName:
                        result[battery] = {
                            'Active': details.Active,
                            'ChargeRate': details.ChargeRate,
                            'Charging': details.Charging,
                            'Discharging': details.Discharging,
                            'DischargeRate': details.DischargeRate,
                            'PowerOnline': details.PowerOnline,
                            'Voltage': details.Voltage,
                            'RemainingCapacity': details.RemainingCapacity

                        }
            return result
        except Exception as e:
            print(e)
            return None
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()


class UsbInsertWatcher:
    def __init__(self):
        self.stop_wanted = False

    def stop(self):
        self.stop_wanted = True

    def watch_for_events(self):
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()

        try:
            w = WMI()
            # WqlEventQuery insertQuery = new WqlEventQuery("SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA 'Win32_USBHub'")
            watcher = w.Win32_USBHub.watch_for('creation')
            while not self.stop_wanted:
                try:
                    event = watcher(timeout_ms=1000)
                except x_wmi_timed_out:
                    pass
                else:
                    print(event)
        except Exception as e:
            print(e)
            return None
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()


class VolumeCreationWatcher:
    def __init__(self, callback=None):
        self.stop_wanted = False
        self.callback = callback

    def stop(self):
        self.stop_wanted = True

    def watch_for_events(self):
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()

        try:
            w = WMI()
            # WqlEventQuery insertQuery = new WqlEventQuery("SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA 'Win32_USBHub'")
            watcher = w.Win32_VolumeChangeEvent.watch_for(EventType=2)
            while not self.stop_wanted:
                try:
                    event = watcher(timeout_ms=1000)
                except x_wmi_timed_out:
                    pass
                else:
                    print(event.DriveName)
                    if self.callback is not None:
                        self.callback(event.DriveName)
        except Exception as e:
            print(e)
            return None
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()


class VolumeRemovalWatcher:
    def __init__(self, callback=None):
        self.stop_wanted = False
        self.callback = callback

    def stop(self):
        self.stop_wanted = True

    def watch_for_events(self):
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()

        try:
            w = WMI()
            watcher = w.Win32_VolumeChangeEvent.watch_for(EventType=3)
            while not self.stop_wanted:
                try:
                    event = watcher(timeout_ms=1000)
                except x_wmi_timed_out:
                    pass
                else:
                    # print(event.DriveName)
                    if self.callback is not None:
                        self.callback(event.DriveName)
        except Exception as e:
            print(e)
            return None
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()


class PowerEventsWatcher:
    """
    Class that watches for power supply state change (ex. computer is on Ac, switch to battery etc. )
    And calls calback funtion with event paramters if passed.
    Event: EventType, TIME_CREATED
    """
    def __init__(self, callback=None):
        self.stop_wanted = False
        self.callback = callback

    def stop(self):
        self.stop_wanted = True

    def watch_for_events(self):
        if not threading.current_thread() is threading.main_thread():
            pythoncom.CoInitialize()

        try:
            w = WMI()
            watcher = w.Win32_PowerManagementEvent.watch_for(EventType=10)
            while not self.stop_wanted:
                try:
                    event = watcher(timeout_ms=1000)
                except x_wmi_timed_out:
                    pass
                else:
                    if self.callback is not None:
                        self.callback(event)
        except Exception as e:
            print(e)
            return None
        finally:
            if not threading.current_thread() is threading.main_thread():
                pythoncom.CoUninitialize()

if __name__ == "__main__":
    #print(WmiHandler.kill_process_by_name('doom3'))
    p = PowerEventsWatcher()
    p.watch_for_events()
    input('end?')
    #print(WmiHandler.get_video_cards())
