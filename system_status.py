import psutil

class SystemStatus():

    @staticmethod
    def get_cpu_temperature():
        result = 0
        mypath = "/sys/class/thermal/thermal_zone0/temp"
        with open(mypath, 'r') as mytmpfile:
            for line in mytmpfile:
                result = line

        result = float(result) / 1000
        result = round(result, 1)
        return str(result)

    @staticmethod
    def get_cpu_usage():
        return psutil.cpu_percent()

    @staticmethod
    def get_ram_usage():
        ram_info = psutil.virtual_memory()
        return ram_info.percent

