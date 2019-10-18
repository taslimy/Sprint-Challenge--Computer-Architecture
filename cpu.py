"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
CMP = 0b10100111
CALL = 0b01010000
JMP = 0b01010100
JNE = 0b01010110
JEQ = 0b01010101


class CPU:
    """Main CPU class."""

    def __init__(self, filename):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.filename = filename
        self.sp = 7
        self.reg[self.sp] = 244
        self.e = 7
        self.fl = [0] * 8

    def __repr__(self):
        return f"ram: {self.ram} \n reg: {self.reg}"

    def ram_read(self, addy):
        return self.ram[addy]

    def ram_write(self, value, addy):
        self.ram[addy] = value

    def load(self):
        """Load a program into memory."""
        try:
            addy = 0

            with open(self.filename) as x:
                for line in x:
                    comment_split = line.split("#")

                    num = comment_split[0].strip()
                    try:
                        val = int(num, 2)
                    except ValueError:
                        continue

                    self.ram[addy] = val
                    addy += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

# create a property in the construtor which is self.sp
# hexadecmal F4
        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        # print(self.ram)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc

        elif op == "MUL":
            self.reg[reg_a] = (self.reg[reg_a]) * (self.reg[reg_b])

        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl[self.e] = 1

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()

    def run(self):
        """Run the CPU."""

        # print(f"opp_a: {opp_a} opp_b: {opp_b}")

        while self.pc < len(self.ram):
            #print(f"ir: {IR}, pc: {self.pc}")

            command = self.ram[self.pc]
            num_ops = (command & 0b11000000) >> 6

            if num_ops == 1:
                opp_a = self.ram_read(self.pc + 1)

            elif num_ops == 2:
                opp_a = self.ram_read(self.pc + 1)
                opp_b = self.ram_read(self.pc + 2)

            if command == HLT:
                sys.exit(1)

            elif command == LDI:
                self.reg[opp_a] = opp_b

            elif command == PRN:
                print(self.reg[opp_a])

            elif command == MUL:
                self.alu("MUL", opp_a, opp_b)
                print(self.reg[opp_a])

            elif command == CMP:
                self.alu("CMP", opp_a, opp_b)

            if command == CALL:
                return_addr = self.pc + 2
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = return_addr
                regnum = self.ram[self.pc + 1]
                subroutine_addr = self.reg[regnum]
                self.pc = subroutine_addr

            elif command == JMP:
                self.pc = self.reg[opp_a]

            elif command == JNE:
                if self.fl[self.e] == 0:
                    self.pc = self.reg[opp_a]
                else:
                    self.pc += num_ops + 1

            elif command == JEQ:
                if self.fl[self.e] == 1:
                    self.pc = self.reg[opp_a]
                else:
                    self.pc += num_ops + 1
            else:
                self.pc += num_ops + 1
