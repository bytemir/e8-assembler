import time

register_index = {"A": "0x01","B": "0x02","C": "0x03","D": "0x04","E": "0x05"}
file_name = "example"
path = f"tests/{file_name}.asm"
out = f"out/{file_name}.bin"

open(out, "w").close()
bin_file = open(out, "a")
with open(path) as file: lines = [line.split(" ") for line in file]

start_time = time.perf_counter()
for index in range(len(lines)):
    line = lines[index]
    size = len(line)
    if size != 3:  
        print(f"Expected: An Opcode and 2 Operands for line {index} instead only found {size}.\nTerminating...")
        bin_file.close()
        break
    opcode, operand1, operand2 = line[0], line[1], line[2]
    conversion = []
    match opcode:
        case "MOV": 
            conversion.append("0x00")
            conversion.append(register_index[operand1])
            conversion.append("0x"+hex(int(operand2))[2:].zfill(2))
        case "JMP": 
            conversion.append("0x01")
            conversion.append("0x"+hex(int(operand1))[2:].zfill(2))
            conversion.append("0x00")
        case "JMPG": 
            conversion.append("0x08")
            conversion.append("0x"+hex(int(operand1))[2:].zfill(2))
            conversion.append("0x00")
        case "JMPZ": 
            conversion.append("0x09")
            conversion.append("0x"+hex(int(operand1))[2:].zfill(2))
            conversion.append("0x00")
        case "ADD": 
            conversion.append("0x02")
            conversion.append(register_index[operand1])
            conversion.append("0x"+hex(int(operand2))[2:].zfill(2))
        case "SUB": 
            conversion.append("0x03")
            conversion.append(register_index[operand1])
            conversion.append("0x"+hex(int(operand2))[2:].zfill(2))
        case "MUL": 
            conversion.append("0x04")
            conversion.append(register_index[operand1])
            conversion.append("0x"+hex(int(operand2))[2:].zfill(2))
        case "DIV": 
            conversion.append("0x05")
            conversion.append(register_index[operand1])
            conversion.append("0x"+hex(int(operand2))[2:].zfill(2))
        case "LOAD": 
            conversion.append("0x06")
            conversion.append("0x"+hex(int(operand1))[2:].zfill(2))
            conversion.append("0x00")
        case "STORE": 
            conversion.append("0x07")
            conversion.append("0x"+hex(int(operand1))[2:].zfill(2))
            conversion.append("0x00")
        case "RAM_WRITE": 
            conversion.append("0x0A")
            conversion.append("0x"+hex(int(operand1))[2:].zfill(2))
            conversion.append("0x"+hex(int(operand2))[2:].zfill(2))
        case "RAM_READ": 
            conversion.append("0x0B") 
            conversion.append("0x"+hex(int(operand1))[2:].zfill(2))
            conversion.append("0x"+hex(int(operand2))[2:].zfill(2))
        case "SCREEN_CLEAR": 
            conversion.append("0x0C")
            conversion.append("0x00")
            conversion.append("0x00")
        case "SCREEN_DRAW": 
            conversion.append("0x0D")
            conversion.append("0x00")
            conversion.append("0x00")         
    binary = " ".join(conversion)
    bin_file.writelines(f"{binary}\n")

end_time = time.perf_counter()
print(f"Finished Assembling in: {end_time - start_time:.6f}s, saved to \"{out}\".")
bin_file.close()