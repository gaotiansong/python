import configparser
def cread_ini(path,data):
    #生成或者修改配置文件
    config = configparser.ConfigParser()
    try:
        config.add_section("Seting")
        config.set("Seting","driver",data[0])
        config.set("Seting","asins",data[1])
        config.set("Seting","procsv",data[2])
    except Exception as e:
        print(e)
        config.set("Seting","driver",data[0])
        config.set("Seting","asins",data[1])
        config.set("Seting","procsv",data[2])
    config.write(open(path, "w"))

def read_ini(path):
    #读取配置文件
    data=[]
    config = configparser.ConfigParser()
    config.read(path)
    data.append(config.get("Seting","driver"))
    data.append(config.get("Seting","asins"))
    data.append(config.get("Seting","procsv"))
    return data
