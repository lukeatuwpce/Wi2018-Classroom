import logging
import time

format1 = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
format2 = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter = logging.Formatter(format1)
formatter2 = logging.Formatter(format2)

# print date of file in MM-DD-YYYY format
file_handler = logging.FileHandler(f'{time.strftime("%m_%d_%Y")}.log')
file_handler.setLevel(logging.WARNING)           
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()        
console_handler.setLevel(logging.DEBUG)          
console_handler.setFormatter(formatter)          

# Send to localhost port 514 using format without date
datagram_handler = logging.DatagramHandler('127.0.0.1', 514)
datagram_handler.setLevel(logging.ERROR)
datagram_handler.setFormatter(formatter2)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)                   
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(datagram_handler)              

def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            i / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))

if __name__ == "__main__":
    my_fun(100)